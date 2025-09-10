const { PythonShell } = require('python-shell');

function analyzeSentiment(message) {
    return new Promise((resolve, reject) => {
        let options = { mode: 'json', args: [message] };
        PythonShell.run('ai_wrapper.py', options, (err, results) => {
            if (err) reject(err);
            resolve(results[0].sentiment);
        });
    });
}

function predictLeadClosure(leadData) {
    return new Promise((resolve, reject) => {
        let options = { mode: 'json', args: [JSON.stringify(leadData)] };
        PythonShell.run('ai_wrapper.py', options, (err, results) => {
            if (err) reject(err);
            resolve(results[0].probability);
        });
    });
}

function recommendUpsell(customerData) {
    return new Promise((resolve, reject) => {
        let options = { mode: 'json', args: [JSON.stringify(customerData)] };
        PythonShell.run('ai_wrapper.py', options, (err, results) => {
            if (err) reject(err);
            resolve(results[0].recommendations);
        });
    });
}

module.exports = { analyzeSentiment, predictLeadClosure, recommendUpsell };
