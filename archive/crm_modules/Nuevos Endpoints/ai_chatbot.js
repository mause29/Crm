const { PythonShell } = require('python-shell');

function processMessage(clientMessage, clientId) {
    return new Promise((resolve, reject) => {
        let options = { mode: 'json', args: [JSON.stringify({ clientMessage, clientId })] };
        PythonShell.run('ai_chatbot_wrapper.py', options, (err, results) => {
            if (err) reject(err);
            resolve(results[0].reply);
        });
    });
}

module.exports = { processMessage };
