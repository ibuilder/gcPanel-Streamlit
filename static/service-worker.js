// gcPanel Service Worker for PWA Support
const CACHE_NAME = 'gcpanel-cache-v1';
const OFFLINE_URL = '/offline.html';

// Resources to precache
const PRECACHE_RESOURCES = [
  '/',
  OFFLINE_URL,
  '/static/icon-192x192.png',
  '/static/icon-512x512.png',
];

// Install event - precache resources
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(PRECACHE_RESOURCES))
      .then(() => self.skipWaiting())
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.filter(cacheName => {
          return cacheName !== CACHE_NAME;
        }).map(cacheName => {
          return caches.delete(cacheName);
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch event - serve from cache or network
self.addEventListener('fetch', event => {
  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request)
        .catch(() => {
          return caches.open(CACHE_NAME)
            .then(cache => {
              return cache.match(OFFLINE_URL);
            });
        })
    );
    return;
  }

  event.respondWith(
    caches.match(event.request)
      .then(response => {
        if (response) {
          return response;
        }
        return fetch(event.request)
          .then(response => {
            // Cache important resources
            if (response && response.status === 200 &&
                (event.request.url.includes('/static/') || 
                 event.request.url.endsWith('.css') || 
                 event.request.url.endsWith('.js') ||
                 event.request.url.endsWith('.png') ||
                 event.request.url.endsWith('.jpg'))) {
              const responseToCache = response.clone();
              caches.open(CACHE_NAME)
                .then(cache => {
                  cache.put(event.request, responseToCache);
                });
            }
            return response;
          })
          .catch(() => {
            // For image requests, return a placeholder
            if (event.request.url.match(/\.(jpg|jpeg|png|gif|svg)$/)) {
              return caches.match('/static/placeholder.png');
            }
            return new Response('Network error', { status: 500 });
          });
      })
  );
});