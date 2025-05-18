// IFC.js Viewer implementation
import { Color } from 'three';
import { IfcViewerAPI } from 'web-ifc-viewer';
import { createSideMenuButton } from './ifc-sidebar.js';

// Set up IFC viewer
const container = document.getElementById('ifc-viewer-container');
const viewer = new IfcViewerAPI({
    container,
    backgroundColor: new Color(0xf5f5f5)
});
viewer.grid.setGrid();
viewer.axes.setAxes();

// Setup scene
async function setupScene() {
    // Create the scene
    await viewer.IFC.setWasmPath('../wasm/');
    
    // Add event handlers
    setupEvents();
    
    // Add side menu items
    createSideMenuButton('visibility', 'Show all elements', async () => await viewer.IFC.loader.ifcManager.createSubset({
        modelID: 0,
        scene: viewer.context.getScene(),
        removePrevious: true,
    }));
    createSideMenuButton('camera', 'Focus view', () => viewer.context.fitToFrame());
    createSideMenuButton('invert_colors', 'Toggle edges', () => {
        viewer.context.renderer.toggleEdges();
    });
}

// Setup event handlers
function setupEvents() {
    // Handle model loading
    const loadModelButton = document.getElementById('load-model-button');
    if (loadModelButton) {
        loadModelButton.addEventListener('click', loadModel);
    }
    
    // Handle file input change
    const ifcFileInput = document.getElementById('ifc-file-input');
    if (ifcFileInput) {
        ifcFileInput.addEventListener('change', loadFromFile);
    }
}

// Load a model from a URL
async function loadModel() {
    const modelUrl = document.getElementById('model-url').value;
    if (modelUrl) {
        try {
            viewer.IFC.loader.ifcManager.applyWebIfcConfig({
                COORDINATE_TO_ORIGIN: true,
                USE_FAST_BOOLS: true
            });
            const model = await viewer.IFC.loadIfcUrl(modelUrl);
            viewer.shadowDropper.renderShadow(model.modelID);
        } catch (error) {
            console.error('Error loading IFC model:', error);
            alert('Failed to load IFC model. Check console for details.');
        }
    }
}

// Load a model from a file input
async function loadFromFile(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = async function () {
            try {
                viewer.IFC.loader.ifcManager.applyWebIfcConfig({
                    COORDINATE_TO_ORIGIN: true,
                    USE_FAST_BOOLS: true
                });
                const model = await viewer.IFC.loadIfc(file);
                viewer.shadowDropper.renderShadow(model.modelID);
            } catch (error) {
                console.error('Error loading IFC model:', error);
                alert('Failed to load IFC model. Check console for details.');
            }
        };
        reader.readAsArrayBuffer(file);
    }
}

// Initialize the viewer
setupScene();

// Export the viewer for external use
window.ifcViewer = viewer;