const {vibrationProperty, padSequence, transformFnDecorator, minMaxScaling} = require('./preprocess.js');
const np = require('numjs');

const request = require('superagent');

// @filter(onThngPropertiesChanged) propertyChangeNew.magnitude=*
function onThngPropertiesChanged(event) {
    const propertyUpdates = JSON.parse(event.changes.magnitude.newValue);
    let data = vibrationProperty(propertyUpdates, [1, 2, 3]);
    data = padSequence(data, 40);
    data = np.array(data);
    data = data.transpose().tolist();
    let inputs = {"instances": [{instances: data}]};

    request
        .post("https://ml.googleapis.com/v1/projects/connected-machine-learning/models/keras_chairml/versions/v1:predict")
        .send(inputs) // sends a JSON post body
        .set("Authorization", "Bearer ")
        .set("Content-Type", "application/json")
        .end((err, res) => {
            console.log(JSON.stringify(res.body))
        });

}


onThngPropertiesChanged(require('./event.json'))

