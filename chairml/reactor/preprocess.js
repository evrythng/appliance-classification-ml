
const np = require('jsnumpy');

function minMaxScaling(data, fitParams) {
    return (data - fitParams['min']) / (fitParams['max'] - fitParams['min'])
}

function meanNormalisation(data, fitParams) {

}

function standardization(data, fitParams) {
    return (data - fitParams['mean'])/ fitParams['std']
}