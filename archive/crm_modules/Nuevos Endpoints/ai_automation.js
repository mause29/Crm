const { PythonShell } = require('python-shell');
const fs = require('fs');

function routeLead(leadData) {
    return new Promise((resolve, reject) => {
        let options = { mode: 'json', args: [JSON.stringify(leadData)] };
        PythonShell.run('ai_automation_wrapper.py', options, (err, results) => {
            if (err) reject(err);
            resolve(results[0].assignedAgent);
        });
    });
}

function generateAlerts(dataStream) {
    return new Promise((resolve, reject) => {
        let options = { mode: 'json', args: [JSON.stringify(dataStream)] };
        PythonShell.run('ai_automation_wrapper.py', options, (err, results) => {
            if (err) reject(err);
            resolve(results[0].alerts);
        });
    });
}

module.exports = { routeLead, generateAlerts };
