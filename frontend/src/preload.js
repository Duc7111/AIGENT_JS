const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electron', {
    openPipeline: () => {
        console.log("openPipeline called");
        ipcRenderer.send('open-pipeline');
    }
});

