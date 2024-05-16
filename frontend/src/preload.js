const { contextBridge, ipcRenderer, app } = require('electron');

// function saveJsonToFile(jsonData, folderPath, projectName) {

    

//     ipcRenderer.on("save-json-file-response", (event, success, error) => {
//       if (success) {
//         console.log("File saved successfully");
//       } else {
//         console.error("Error saving file:", error);
//       }
//     });
// };

contextBridge.exposeInMainWorld('electron', {
    // receivedParams: () => {
    //     return new Promise((resolve, reject) => {
    //         ipcRenderer.on('pass-params', (event, params) => {
    //             console.log('Received params from main process:', params);
    //             resolve(params);
    //         });
    //     });
    // },
    loadPipelineAsModule: (keyID, pathModule) => {
        console.log("loadPipelineAsModule called");
        ipcRenderer.send('load-pipeline-as-module', {
            request: "load_pipeline_as_module",
            inputs: {
                key: keyID,
                path: pathModule,
            },
        }); 
    },
    deleteDirFromHome: (dirFolder) => {
        return new Promise((resolve, reject) => {
            console.log("deleteDirFromHome called",dirFolder);
            ipcRenderer.send('delete-dir-from-home', dirFolder);
            ipcRenderer.on('delete-dir-from-home-response', (event, checkDeleteStatus) => {
                console.log('delete-dir-response:', checkDeleteStatus);
                resolve(checkDeleteStatus);
            });
        });
},

    importFileFromDialog: (importFile) => {
        return new Promise((resolve, reject) => {
            ipcRenderer.send('import-file-dialog', importFile);
            ipcRenderer.on('import-file-response', (event, data) => {
                console.log('import-file-response:', data);
                resolve(data);
            });
        });
    },

    exportToJsonl: (transferData)=>{
        console.log("ExportToJsonl called",transferData[0],transferData[1],transferData[2]);
        ipcRenderer.send('export-jsonl-file', transferData);
    },

    receivedListProjectName: () => {
        return new Promise((resolve, reject) => {
            ipcRenderer.send('list-available-project-name');
            ipcRenderer.on('received-list-project-name', (event, listProjectName) => {
                console.log('Received list project name:', listProjectName);
                resolve(listProjectName);
            });
        });
    },

    receivedData: () => {
        return new Promise((resolve, reject) => {
            ipcRenderer.on('received-data', (event, receivedData) => {
                resolve(receivedData);
            });
        });
    },

    sendListProjectName: (listProjectName) => {
        ipcRenderer.send('list-project-name', listProjectName);
    },

    readFileGivenName: (filePath) => {
        return new Promise((resolve, reject) => {
            ipcRenderer.send('read-file-given-name', filePath);
            ipcRenderer.on('read-file-response', (event, data) => {
                console.log('Received data from main process:', data);
                resolve(data);
            });
        });
    },
    sendParamsToNextPage: (params) => {
        console.log("sendParamsToNextPage called",params);
        ipcRenderer.send('send-params-to-next-page', params);
    },
    getListFileName: (folderPath) => {
        return new Promise((resolve, reject) => {
            ipcRenderer.send('get-list-file-name', folderPath);
            
            ipcRenderer.on('list-file-name', (event, files) => {
              console.log('Received file list from main process:', files);
              resolve(files);
            });
    
          });
    },
    saveJsonToFile: (transferData)=> {
        console.log("saveJsonToFile called",transferData[0],transferData[1],transferData[2]);
        ipcRenderer.send('save-json-file', transferData);
    },
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
    },
    addModule: (id_name,file_Python ,module_name) => {
        console.log("addModule called");
        ipcRenderer.send('add-module', {
            request: "add_module",
            inputs: {
                key: id_name,
                type: file_Python,
                module: module_name,
            },
        });
    },
    connectModule:(id1_name,id2_name,output1, input2) => {
       console.log("connectModule called",id1_name,id2_name,output1, input2);
        ipcRenderer.send('connect-module', {
            request: "connect_modules",
            inputs: {
                srcModuleKey: id1_name,
                tgtModuleKey: id2_name,
                srcKey: output1,
                tgtKey: input2,
            },
        }); 
    },
    setHyperparameters: (id_name,hyperparameters) => {
        console.log("set_hyperparameters called");
        ipcRenderer.send('set-module-hyperparameters', {
            request: "set_module_hyperparameters",
            inputs: {
                key: id_name,
                hyperparameters: hyperparameters,
            },
        });
    },
    outputRegister: (key, srcModuleKey, srcKey) => {
        console.log("outputRegister called");
        ipcRenderer.send('output_register', {
            request: "output_register",
            inputs: {
                key: key,
                srcModuleKey: srcModuleKey,
                srcKey: srcKey
            },
        });
    },
    removeModule: (id_name) => {
        console.log("removeModule called");
        ipcRenderer.send('remove-module', {
            request: "remove_module",
            inputs: {
                key: id_name,
            },
        });
    },
    disconnectModule: (id1_name,id2_name,output1, input2) => {
        console.log("disconnectModule called");
        ipcRenderer.send('disconnect-module', {
            request: "disconnect_modules",
            inputs: {
                srcModuleKey: id1_name,
                tgtModuleKey: id2_name,
                srcKey: output1,
                tgtKey: input2,
            },
        });
     },
    runPipeline: () => {
        console.log("runPipeline called");
        ipcRenderer.send('run',{
            request: "run",
            inputs:{},
        });
    },

});

