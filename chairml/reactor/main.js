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
    let data = vibrationProperty(propertyUpdates, [0, 1, 2, 3]);
    const f = transformFnDecorator(standardization, {"std":[37.4726948414,0.5668747745,0.4292762528,0.5470030048],"mean":[28.392496191,0.1113913954,-0.0082839365,0.6383515595]});
    data = f(data);
    data = padSequence(data, 40);
    data = np.transpose(data);
    let inputs = {"instances": [{instances: data}]};
    request
        .post("https://ml.googleapis.com/v1/projects/connected-machine-learning/models/keras_chairml/versions/v1:predict")
        .send(inputs) // sends a JSON post body
        .set("Authorization", "Bearer ya29.Glx9BXxzcw820YwfYBBRtVxMsGg3F-zoXSMx-niOjXmGdd8ksTHaLD_lyes5HpgHkKA0OriUpq55WSYY0YwmacgBKTpLEIgLFKqs31ilhYmPAPs02rUuv0oyH4GXRA")
        .set("Content-Type", "application/json")
        .end((err, res) => {
            console.log(JSON.stringify(res.body));
            // app.action('_eventClassification').create({
            //     thng: event.thng.id,
            //     customFields: JSON.stringify(res.body)
            // }).then(data=>{
            //     done();
            // }).catch(err=>{
            //     logger.error(err)
            // });
        });
}

onThngPropertiesChanged(require('./event.json'))
