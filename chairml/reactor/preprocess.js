
const np = require('jsnumpy');
print = console.log;
function minMaxScaling(data, fitParams) {
    return (data - fitParams['min']) / (fitParams['max'] - fitParams['min'])
}

function meanNormalisation(data, fitParams) {

}

function standardization(data, fitParams) {
    return (data - fitParams['mean'])/ fitParams['std']
}
function vibrationPropertyValue(data) {
    data.fo
    return JSON.parse(data)
}
var data = require('../data/rawdata.json');
for (let d in data){
    for (p of data[d]) {
        print(typeof(p.value))
    }
}