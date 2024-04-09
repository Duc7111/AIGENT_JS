const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electron', {
    openPipeline: () => {
        console.log("openPipeline called");
        ipcRenderer.send('open-pipeline');
    },
    navigateBack: () => {
        console.log("navigateBack called");
        ipcRenderer.send('navigate-back');
    },
    savePipeline: () => {
        console.log("savePipeline called");
        ipcRenderer.send("save-pipeline-request", {
            request: "save_pipeline",
            inputs: {
              path: "path/to/save/pipeline_test.json",
            },
          });
    }
});

