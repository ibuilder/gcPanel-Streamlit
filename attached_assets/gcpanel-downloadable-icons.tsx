import React from 'react';

const DownloadableIcons = () => {
  // Colors for the Two-tone Blue scheme
  const colors = {
    darkBlue: '#3367D6',
    lightBlue: '#8AB4F8',
    white: '#FFFFFF',
  };

  // Function to render the detailed hammerhead tower crane
  const renderDetailedCrane = (mainColor, secondaryColor, scale = 1, simplified = false) => {
    return (
      <g transform={`scale(${scale})`}>
        {/* Vertical mast */}
        <rect x="32" y="22" width="6" height="52" fill={mainColor} />
        
        {/* Diagonal supports for mast */}
        {!simplified && (
          <>
            <polygon points="30,50 27,58 32,58 35,50" fill={secondaryColor} />
            <polygon points="40,50 43,58 38,58 35,50" fill={secondaryColor} />
          </>
        )}
        
        {/* Operator cabin */}
        <rect x="29" y="18" width="12" height="7" fill={secondaryColor} />
        
        {/* Main jib (longer arm) with lattice structure */}
        <rect x="38" y="16" width="32" height="3" fill={mainColor} />
        {!simplified && (
          <>
            <line x1="40" y1="16" x2="40" y2="19" stroke={secondaryColor} strokeWidth="1" />
            <line x1="45" y1="16" x2="45" y2="19" stroke={secondaryColor} strokeWidth="1" />
            <line x1="50" y1="16" x2="50" y2="19" stroke={secondaryColor} strokeWidth="1" />
            <line x1="55" y1="16" x2="55" y2="19" stroke={secondaryColor} strokeWidth="1" />
            <line x1="60" y1="16" x2="60" y2="19" stroke={secondaryColor} strokeWidth="1" />
            <line x1="65" y1="16" x2="65" y2="19" stroke={secondaryColor} strokeWidth="1" />
          </>
        )}
        
        {/* Counter jib (shorter arm) with lattice */}
        <rect x="0" y="16" width="29" height="3" fill={mainColor} />
        {!simplified && (
          <>
            <line x1="5" y1="16" x2="5" y2="19" stroke={secondaryColor} strokeWidth="1" />
            <line x1="10" y1="16" x2="10" y2="19" stroke={secondaryColor} strokeWidth="1" />
            <line x1="15" y1="16" x2="15" y2="19" stroke={secondaryColor} strokeWidth="1" />
            <line x1="20" y1="16" x2="20" y2="19" stroke={secondaryColor} strokeWidth="1" />
            <line x1="25" y1="16" x2="25" y2="19" stroke={secondaryColor} strokeWidth="1" />
          </>
        )}
        
        {/* Counterweight on counter jib */}
        <rect x="2" y="11" width="12" height="5" fill={secondaryColor} />
        {!simplified && <rect x="4" y="8" width="8" height="3" fill={secondaryColor} />}
        
        {/* Trolley on main jib */}
        <rect x="55" y="14" width="4" height="6" fill={secondaryColor} />
        
        {/* Hook/cable */}
        {!simplified && (
          <>
            <line x1="57" y1="20" x2="57" y2="30" stroke={secondaryColor} strokeWidth="1" />
            <path d="M55 30 L59 30 L57 34 Z" fill={secondaryColor} />
          </>
        )}
        
        {/* Base/foundation */}
        <rect x="28" y="74" width="14" height="4" fill={secondaryColor} />
        {!simplified && <rect x="24" y="78" width="22" height="3" fill={secondaryColor} />}
      </g>
    );
  };

  return (
    <div className="p-6 bg-gray-100 rounded-lg">
      <h1 className="text-2xl font-bold mb-6 text-gray-800">gcPanel Two-tone Blue Icons</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        {/* Favicon Section */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4 text-gray-700">Favicons & Small Icons</h2>
          <p className="text-sm text-gray-600 mb-4">Web browser tabs and small app icons</p>
          
          <div className="flex flex-wrap gap-6 items-end">
            {/* 16x16 favicon */}
            <div className="flex flex-col items-center">
              <div className="border border-gray-300 p-1">
                <svg width="16" height="16" viewBox="0 0 16 16">
                  <rect width="16" height="16" fill={colors.darkBlue} />
                  <g transform="translate(0.5, 0.5) scale(0.15)">
                    {renderDetailedCrane(colors.lightBlue, colors.white, 1, true)}
                  </g>
                </svg>
              </div>
              <span className="text-xs mt-1 text-gray-500">16×16</span>
              <span className="text-xs text-blue-500 cursor-pointer">favicon.ico</span>
            </div>
            
            {/* 32x32 favicon */}
            <div className="flex flex-col items-center">
              <div className="border border-gray-300 p-1">
                <svg width="32" height="32" viewBox="0 0 32 32">
                  <rect width="32" height="32" fill={colors.darkBlue} />
                  <g transform="translate(1, 1) scale(0.3)">
                    {renderDetailedCrane(colors.lightBlue, colors.white, 1, true)}
                  </g>
                </svg>
              </div>
              <span className="text-xs mt-1 text-gray-500">32×32</span>
              <span className="text-xs text-blue-500 cursor-pointer">favicon-32.png</span>
            </div>
            
            {/* 48x48 favicon */}
            <div className="flex flex-col items-center">
              <div className="border border-gray-300 p-1">
                <svg width="48" height="48" viewBox="0 0 48 48">
                  <rect width="48" height="48" fill={colors.darkBlue} />
                  <g transform="translate(1, 1) scale(0.45)">
                    {renderDetailedCrane(colors.lightBlue, colors.white)}
                  </g>
                </svg>
              </div>
              <span className="text-xs mt-1 text-gray-500">48×48</span>
              <span className="text-xs text-blue-500 cursor-pointer">favicon-48.png</span>
            </div>
            
            {/* 64x64 favicon */}
            <div className="flex flex-col items-center">
              <div className="border border-gray-300 p-1">
                <svg width="64" height="64" viewBox="0 0 64 64">
                  <rect width="64" height="64" fill={colors.darkBlue} />
                  <g transform="translate(2, 2) scale(0.6)">
                    {renderDetailedCrane(colors.lightBlue, colors.white)}
                  </g>
                </svg>
              </div>
              <span className="text-xs mt-1 text-gray-500">64×64</span>
              <span className="text-xs text-blue-500 cursor-pointer">favicon-64.png</span>
            </div>
          </div>
        </div>
        
        {/* App Icons Section */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4 text-gray-700">Mobile App Icons</h2>
          <p className="text-sm text-gray-600 mb-4">Mobile device home screens</p>
          
          <div className="flex flex-wrap gap-6 items-end">
            {/* 120x120 iOS */}
            <div className="flex flex-col items-center">
              <div className="border border-gray-300 rounded-2xl overflow-hidden">
                <svg width="120" height="120" viewBox="0 0 120 120">
                  <rect width="120" height="120" fill={colors.darkBlue} />
                  <g transform="translate(10, 10) scale(1)">
                    {renderDetailedCrane(colors.lightBlue, colors.white)}
                  </g>
                </svg>
              </div>
              <span className="text-xs mt-1 text-gray-500">120×120</span>
              <span className="text-xs text-blue-500 cursor-pointer">ios-120.png</span>
            </div>
            
            {/* 180x180 iOS */}
            <div className="flex flex-col items-center">
              <div className="border border-gray-300 rounded-2xl overflow-hidden">
                <svg width="120" height="120" viewBox="0 0 180 180">
                  <rect width="180" height="180" fill={colors.darkBlue} />
                  <g transform="translate(15, 15) scale(1.5)">
                    {renderDetailedCrane(colors.lightBlue, colors.white)}
                  </g>
                </svg>
              </div>
              <span className="text-xs mt-1 text-gray-500">180×180</span>
              <span className="text-xs text-blue-500 cursor-pointer">ios-180.png</span>
            </div>
            
            {/* 192x192 Android */}
            <div className="flex flex-col items-center">
              <div className="border border-gray-300 rounded-2xl overflow-hidden">
                <svg width="120" height="120" viewBox="0 0 192 192">
                  <rect width="192" height="192" fill={colors.darkBlue} />
                  <g transform="translate(16, 16) scale(1.6)">
                    {renderDetailedCrane(colors.lightBlue, colors.white)}
                  </g>
                </svg>
              </div>
              <span className="text-xs mt-1 text-gray-500">192×192</span>
              <span className="text-xs text-blue-500 cursor-pointer">android-192.png</span>
            </div>
          </div>
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        {/* Full Logo Section */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4 text-gray-700">Full Logo</h2>
          <p className="text-sm text-gray-600 mb-4">Website header and marketing materials</p>
          
          <div className="flex flex-col gap-6 items-center">
            {/* Full logo */}
            <div>
              <svg width="240" height="60" viewBox="0 0 240 60">
                {/* Logo Icon */}
                <g transform="translate(0, 10)">
                  <rect x="2" y="2" width="36" height="36" rx="4" fill={colors.darkBlue} />
                  
                  {/* Detailed Crane */}
                  <g transform="translate(5, 5) scale(0.7)">
                    {renderDetailedCrane(colors.lightBlue, colors.white)}
                  </g>
                </g>
                
                {/* Text */}
                <g transform="translate(45, 32)">
                  <text fontFamily="Arial, sans-serif" fontSize="26" fontWeight="600">
                    <tspan fill="#4285F4">gc</tspan>
                    <tspan fill="#4285F4">Panel</tspan>
                  </text>
                </g>
              </svg>
            </div>
            <div className="flex gap-4">
              <span className="text-sm text-blue-500 cursor-pointer">gcpanel-logo.svg</span>
              <span className="text-sm text-blue-500 cursor-pointer">gcpanel-logo.png</span>
            </div>
          </div>
        </div>
        
        {/* Social Media Section */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4 text-gray-700">Social Media</h2>
          <p className="text-sm text-gray-600 mb-4">Social profile images</p>
          
          <div className="flex gap-6 items-center">
            {/* Square social media icon */}
            <div className="flex flex-col items-center">
              <div className="border border-gray-300">
                <svg width="100" height="100" viewBox="0 0 100 100">
                  <rect width="100" height="100" fill={colors.darkBlue} />
                  <g transform="translate(10, 10) scale(0.8)">
                    {renderDetailedCrane(colors.lightBlue, colors.white)}
                  </g>
                </svg>
              </div>
              <span className="text-xs mt-1 text-gray-500">Square</span>
              <span className="text-xs text-blue-500 cursor-pointer">social-square.png</span>
            </div>
            
            {/* Circle social media icon */}
            <div className="flex flex-col items-center">
              <div className="border border-gray-300 rounded-full overflow-hidden">
                <svg width="100" height="100" viewBox="0 0 100 100">
                  <circle cx="50" cy="50" r="50" fill={colors.darkBlue} />
                  <g transform="translate(10, 10) scale(0.8)">
                    {renderDetailedCrane(colors.lightBlue, colors.white)}
                  </g>
                </svg>
              </div>
              <span className="text-xs mt-1 text-gray-500">Circle</span>
              <span className="text-xs text-blue-500 cursor-pointer">social-circle.png</span>
            </div>
          </div>
        </div>
      </div>
      
      {/* High Resolution App Store Icon */}
      <div className="bg-white p-6 rounded-lg shadow mb-8">
        <h2 className="text-xl font-semibold mb-4 text-gray-700">App Store Icon</h2>
        <p className="text-sm text-gray-600 mb-4">High resolution for app stores (1024×1024)</p>
        
        <div className="flex justify-center">
          <div className="flex flex-col items-center">
            <div className="border border-gray-300 rounded-2xl overflow-hidden">
              <svg width="200" height="200" viewBox="0 0 1024 1024">
                <rect width="1024" height="1024" fill={colors.darkBlue} />
                <g transform="translate(100, 100) scale(8)">
                  {renderDetailedCrane(colors.lightBlue, colors.white)}
                </g>
              </svg>
            </div>
            <span className="text-xs mt-1 text-gray-500">1024×1024</span>
            <span className="text-xs text-blue-500 cursor-pointer">app-store-icon.png</span>
          </div>
        </div>
      </div>
      
      <div className="bg-blue-50 p-6 rounded-lg border border-blue-200">
        <h2 className="text-lg font-semibold mb-3 text-blue-800">Download Instructions</h2>
        <p className="text-sm text-blue-700 mb-3">
          In a real implementation, you would download these files in the following formats:
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <h3 className="font-semibold text-blue-800 mb-2">Favicon Package</h3>
            <ul className="list-disc pl-5 text-sm text-blue-700">
              <li><strong>favicon.ico</strong> - Multi-size ICO file (16×16, 32×32, 48×48)</li>
              <li><strong>favicon-16.png</strong> - 16×16 PNG for older browsers</li>
              <li><strong>favicon-32.png</strong> - 32×32 PNG for older browsers</li>
              <li><strong>favicon.svg</strong> - SVG version for modern browsers</li>
              <li><strong>site.webmanifest</strong> - Web app manifest file</li>
              <li><strong>browserconfig.xml</strong> - IE/Edge configuration</li>
            </ul>
          </div>
          
          <div>
            <h3 className="font-semibold text-blue-800 mb-2">App Icons</h3>
            <ul className="list-disc pl-5 text-sm text-blue-700">
              <li><strong>iOS:</strong> 120×120, 180×180 PNG files</li>
              <li><strong>Android:</strong> 192×192, 512×512 PNG files</li>
              <li><strong>App Store:</strong> 1024×1024 PNG</li>
              <li><strong>Windows:</strong> 70×70, 150×150, 310×310 PNG files</li>
            </ul>
          </div>
        </div>
        
        <div className="mt-4">
          <h3 className="font-semibold text-blue-800 mb-2">Logo Package</h3>
          <ul className="list-disc pl-5 text-sm text-blue-700">
            <li><strong>SVG:</strong> Vector format for web and print</li>
            <li><strong>PNG:</strong> Multiple sizes (200px, 500px, 1000px) with transparency</li>
            <li><strong>JPG:</strong> For situations where transparency isn't needed</li>
            <li><strong>Social Media:</strong> Square and circle formats (800×800, 1200×1200)</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default DownloadableIcons;