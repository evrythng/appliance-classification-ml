print = console.log

function transformFnDecorator(fn, fitParams) {
    function call(data) {
        let out = [];
        for (let r = 0; r < data.length; r++) {
            out[r] = [];
            for (let c = 0; c < data[r].length; c++) {
                out[r][c] = fn(data[r], fitParams, c);
            }
        }
        return out;
    }

    return call;
}

function minMaxScaling(row, fitParams, c) {
    return (row[c] - fitParams['min'][c]) / (fitParams['max'][c] - fitParams['min'][c]);
}


function meanNormalisation(row, fitParams, c) {
    return (row[c] - fitParams['mean'][c]) / (fitParams['max'][c] - fitParams['min'][c]);
}

function standardization(row, fitParams, c) {
    return (row[c] - fitParams['mean'][c]) / fitParams['std'][c];
}


function vibrationProperty(data, keepColumns) {
    if (keepColumns === undefined) {
        keepColumns = [0, 1, 2, 3];
    }
    let frame = [];
    for (let row of data) {
        let _row = [];
        for (let i of keepColumns) {
            _row.push(row[i])
        }
        frame.push(_row);
    }
    return frame;

}

function padSequence(data, maxlen) {
    if (data.length === maxlen) {
        return data;
    } else if (data.length > maxlen) {
        return data.slice(0, maxlen);
    }
    else {
        let colSize = data[0].length;
        for (let i = data.length; i < maxlen; i++) {
            data.push(Array(colSize).fill(0.0));
        }
        return data
    }


}

module.exports.vibrationProperty = vibrationProperty;
module.exports.transformFnDecorator = transformFnDecorator;
module.exports.minMaxScaling = minMaxScaling;
module.exports.padSequence = padSequence;