const { app, BrowserWindow, ipcMain, remote } = require('electron');
const path = require('path');
const net = require('net');
const HOST = '127.0.0.1';
const PORT = 7777;

var fsExtra = require('fs-extra');

let clientSocket = new net.Socket();

// Handle creating/removing shortcuts on Windows when installing/uninstalling.
if (require('electron-squirrel-startup')) {
  app.quit();
}


const createWindow = () => {
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    width: 1920,
    height: 1080,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
    },
  });

  // and load the index.html of the app.
  mainWindow.loadFile(path.join(__dirname, 'index.html'));

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
    clientSocket.write(JSON.stringify(data));
  });

  ipcMain.on('set-module-hyperparameters', (event, data) => {
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

