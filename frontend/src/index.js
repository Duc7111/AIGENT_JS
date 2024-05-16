const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const net = require('net');
const HOST = '127.0.0.1';
const PORT = 7777;

var fsExtra = require('fs-extra');

let mainWindow;

const defaultDownloadsPath = app.getPath('downloads');

var uniqueName = [];

let uiJsonData = [];

let beJsonData = [];

let clientSocket = new net.Socket();

let combinedData = [];

const defaultProjectName = "Project Name";
let index =1;

let checkFileImport = false;

// Handle creating/removing shortcuts on Windows when installing/uninstalling.
if (require('electron-squirrel-startup')) {
  app.quit();
}

function saveJsonToFile(data) {
  const filePath = `${data[1]}/${data[2]}.ui.json`;
    console.log("saveJsonToFile called",data[0],filePath);
    const jsonStrings = data[0].map(item => JSON.stringify(item, null, 2));
    fsExtra.writeFile(filePath, `[${jsonStrings.join(',\n')}]`, (err) => {
      if (err) {
        console.error(err);
      } else {
        console.log('File saved successfully');
      }   
    });
};

async function openImportFileDialog(listUniqueProjectName, saveLocalPath) {
  try {
      const result = await dialog.showOpenDialog({
          properties: ['openFile'],
          filters: [
              { name: 'JSON Lines', extensions: ['jsonl'] },
              { name: 'All Files', extensions: ['*'] }
          ]
      });

      const filePath = result.filePaths[0];

      if (filePath) {
            //get file name
          const fileName = filePath.split('\\').pop();
          const fileContent = await fsExtra.readFile(filePath, 'utf8');
          const newProjectName = fileName.split('.')[0];
          while(listUniqueProjectName.includes(newProjectName)) {
            newProjectName = `${defaultProjectName}${index}`;
            index++;
          }
          const parsedData = JSON.parse(fileContent);

          const { ui, be } = parsedData;

          const uiFilePath = `${saveLocalPath}/${newProjectName}.ui.json`;
          const beFilePath = `${saveLocalPath}/${newProjectName}.json`;

          fsExtra.writeFile(uiFilePath, JSON.stringify(ui, null, 2), (err) => {
              if (err) {
                  console.error(`Error saving file from import ${uiFilePath}:`, err);
              } else {
                  console.log(`Successfully saved file from import ${uiFilePath}`);
              }
          });

          fsExtra.writeFile(beFilePath, JSON.stringify(be, null, 2), (err) => {
              if (err) {
                  console.error(`Error saving file from import ${beFilePath}:`, err);
              } else {
                  console.log(`Successfully saved file from import ${beFilePath}`);
                }
          });

          checkFileImport = true;
          
      }
  } catch (error) {
      console.error('Error open import file dialog:', error);
  }
}

function openSaveFileDialog() {
  dialog.showSaveDialog({
      title: 'Save JSONL File',
      buttonLabel: 'Save',
      defaultPath: defaultDownloadsPath,
      filters: [
          { name: 'JSON Lines', extensions: ['jsonl'] },
          { name: 'All Files', extensions: ['*'] }
      ]
  }).then((result) => {
      if (!result.canceled && result.filePath) {
          const filePath = result.filePath;
          console.log('Selected file path:', filePath);
 
          const fileName = filePath.split('\\').pop();
          console.log('Selected file name:', fileName);

          writeJsonlFile(filePath, combinedData);

      }
  }).catch((err) => {
      console.error('Error opening save dialog:', err);
  });
}

function writeJsonlFile(jsonlFilePath, jsonData) {
  try {
      const jsonlData = JSON.stringify(jsonData, null, 2);
      fsExtra.writeFileSync(jsonlFilePath, jsonlData);
      console.log(`Successfully created JSONL file: ${jsonlFilePath}`);
  } catch (err) {
      console.error(`Error writing JSONL file ${jsonlFilePath}:`, err);
  }
};

async function combinedToOneData(){
  console.log("uiJsonData, beJsonData called",uiJsonData,beJsonData);
  if (uiJsonData && beJsonData) {
    combinedData = {"ui": JSON.parse(uiJsonData), "be": JSON.parse(beJsonData)};
  } else if(uiJsonData){
    combinedData = {"ui": JSON.parse(uiJsonData), "be":{}};
  } else if(beJsonData){
    combinedData = {"ui":{},"be": JSON.parse(beJsonData)};
  }
}

async  function readJsonFile(uiPath, BePath) {
  try {
      uiJsonData = await fsExtra.readFile(uiPath, 'utf8');
      beJsonData = await fsExtra.readFile(BePath, 'utf8');
      await combinedToOneData();
  } catch (err) {
      console.error(`Error reading JSON file ${filePath}:`, err);
  }
}


const createWindow = () => {
  // Create the browser window.
  mainWindow = new BrowserWindow({
    width: 1920,
    height: 1080,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
    },
  });

  // and load the index.html of the app.
  mainWindow.loadFile(path.join(__dirname, 'index.html'));

  ipcMain.on('delete-dir-from-home', async (event, data) => {
    const uiPath = `${data[1]}/${data[0]}.ui.json`;
    const bePath = `${data[1]}/${data[0]}.json`;
    console.log("UI path delete-dir-from-home called",uiPath);
    console.log("BE path delete-dir-from-home called",bePath);
    let checkDeleteUiStatus = false;
    let checkDeleteBeStatus = false;
    if (fsExtra.existsSync(uiPath)) {
      await fsExtra.unlink(uiPath, (err) => {
        if (err) {
          console.error(err);
        } else {
          console.log('Directory ui removed successfully');
          checkDeleteUiStatus = true;
        }
      });
    }else{
      checkDeleteUiStatus = true;
    }


    if(fsExtra.existsSync(bePath)){
      await fsExtra.unlink(bePath, (err) => {
        if (err) {
          console.error(err);
        } else {
          console.log('Directory be removed successfully');
          checkDeleteBeStatus = true;
        }
      });
    }else{
      checkDeleteBeStatus = true;
    }

    await event.sender.send('delete-dir-from-home-response', checkDeleteBeStatus || checkDeleteUiStatus);

  });

  ipcMain.on('load-pipeline-as-module', (event, data) => {

  });
  
  ipcMain.on('import-file-dialog', async (event, data) => {
    await openImportFileDialog(data[0],data[1]);
    await event.sender.send('import-file-response', checkFileImport);
  });

  ipcMain.on('export-jsonl-file', (event, data) => {
    console.log("export-jsonl-file called initial",data);
    saveJsonToFile(data);
    const fileUiPath = `${data[1]}/${data[2]}.ui.json`;
    const fileBePath = `${data[1]}/${data[2]}.json`;
    
    readJsonFile(fileUiPath, fileBePath);
    openSaveFileDialog();
  });

  ipcMain.on('list-available-project-name',(event) => {
    mainWindow.webContents.send('received-list-project-name', uniqueName);
  });

  ipcMain.on('list-project-name', (event, data) => {
    uniqueName = data;
  });
  ipcMain.on('read-file-given-name',(event, data) => {
    fsExtra.readFile(data, 'utf8', (err, fileData) => {
      if (err) {
        console.error(err);
      } else {
        mainWindow.webContents.send('read-file-response', fileData);
      }
    });
  });

  ipcMain.on('save-json-file', (event, data) => {
    console.log("saveJsonToFile called initial",data);
    const filePath = `${data[1]}/${data[2]}.ui.json`;
    console.log("saveJsonToFile called",data[0],filePath);
    const jsonStrings = data[0].map(item => JSON.stringify(item, null, 2));
    fsExtra.writeFile(filePath, `[${jsonStrings.join(',\n')}]`, (err) => {
      if (err) {
        console.error(err);
      } else {
        console.log('File saved successfully');
      }   
    });
  });

  ipcMain.on('get-list-file-name', (event, data) => {
    
    fsExtra.readdir(data, (err, files) => {
      if (err) {
        console.error(err);
      } else {
        mainWindow.webContents.send('list-file-name', files);
      }
    });
  });

  ipcMain.on('open-pipeline', (event) => {
    mainWindow.loadFile(path.join(__dirname, 'Pipeline', 'pipeline.html'));
    // console.log(path.join(__dirname, 'Pipeline', 'pipeline.html'));
    // mainWindow.once('send-params-to-next-page', (event, params) => {
    //   mainWindow.webContents.send('pass-params', params);
    // });
  });

  ipcMain.on('navigate-back', (event) => {
    mainWindow.webContents.goBack();
  });

  ipcMain.on('save-pipeline-request', (event, data) => {
    clientSocket.write(JSON.stringify(data));
  });

  ipcMain.on('add-module', (event, data) => {
    console.log("load-pipeline-as-module called",data);
    clientSocket.write(JSON.stringify(data));
  });

  ipcMain.on('load-pipeline-as-module', (event, data) => {
    console.log("load-pipeline-as-module called",data);
    clientSocket.write(JSON.stringify(data));
  });

  ipcMain.on('set-module-hyperparameters', (event, data) => {
    clientSocket.write(JSON.stringify(data));
  });

  ipcMain.on('output_register', (event, data) => {
    clientSocket.write(JSON.stringify(data));
  });

  ipcMain.on('remove-module', (event, data) => {
    clientSocket.write(JSON.stringify(data));
  });

  ipcMain.on('disconnect-module',(event,data) =>{
    clientSocket.write(JSON.stringify(data));
  });

  ipcMain.on('connect-module',(event,data) =>{
    clientSocket.write(JSON.stringify(data));
  })

  ipcMain.on('run',(event,data) =>{
    clientSocket.write(JSON.stringify(data));
  });

  // Open the DevTools.
  //mainWindow.webContents.openDevTools();
};

const client = () => {
  clientSocket.connect(PORT, HOST, () => {
    console.log('Connected to server');
    createWindow();
    //clientSocket.write('Hello, server!');

  }); 
  clientSocket.on('data', (data) => {
    console.log('Received from server:', data.toString());
    mainWindow.webContents.send('received-data', data.toString());
  });
  clientSocket.on('close', () => {
    console.log('Connection closed');
  });
};


// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', () => {
  client();
});

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  // On OS X it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and import them here.


function createPipelineWindow() {
  let pipelineWindow = new BrowserWindow({
    width: 1920,
    height: 1080,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
    }
  });

}

