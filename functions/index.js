const {onRequest} = require("firebase-functions/v2/https");
const { exec } = require("child_process");
const path = require("path");

exports.app = onRequest((req, res) => {
    const scriptPath = path.resolve(__dirname, "../backend/main.py");
    
    exec(`python ${scriptPath}`, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error}`);
            res.status(500).send(stderr);
        } else {
            res.status(200).send(stdout);
        }
    });
});