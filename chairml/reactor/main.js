// const {vibrationProperty, padSequence, transformFnDecorator, minMaxScaling} = require('./preprocess.js');

const request = require('superagent');
const np = require('jsnumpy');

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


// @filter(onThngPropertiesChanged) propertyChangeNew.magnitude=*
function onThngPropertiesChanged(event) {
    const propertyUpdates = JSON.parse(event.changes.magnitude.newValue);
    let data = vibrationProperty(propertyUpdates, [1, 2, 3]);
    data = padSequence(data, 40);
    data = np.transpose(data);
    let inputs = {"instances": [{instances: data}]};
    request
        .post("https://ml.googleapis.com/v1/projects/connected-machine-learning/models/keras_chairml/versions/v1:predict")
        .send(inputs) // sends a JSON post body
        .set("Authorization", "Bearer ya29.Glx9BbmshA8xXs1Vuw181wdYVC3wQz0ke5ZOQ3SWbugdt5AK6l7IvQ7O4uVLdrIa6lTxZG5Qmq7oLzGVyvvoSgRddv-MQhBkGr0MA8cibWtIv15xUaNbPE90H5VoTg")
        .set("Content-Type", "application/json")
        .end((err, res) => {
            logger.debug(JSON.stringify(res.body));
            done();
        });
}


