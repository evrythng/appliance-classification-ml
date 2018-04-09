process.env.GOOGLE_APPLICATION_CREDENTIALS = './application_default_credentials.json';
const {vibrationProperty, padSequence, transformFnDecorator, standardization} = require('./preprocess.js');
const request = require('superagent');
const np = require('jsnumpy');
const {auth} = require('google-auth-library');




// @filter(onThngPropertiesChanged) propertyChangeNew.magnitude=*
function onThngPropertiesChanged(event) {
    const propertyUpdates = JSON.parse(event.changes.magnitude.newValue);
    let data = vibrationProperty(propertyUpdates, [1, 2, 3]);
    let inputDataParams = require('./input_data_params.json');
    const f = transformFnDecorator(standardization, inputDataParams);
    data = f(data);
    data = padSequence(data, inputDataParams.lookback);


    let inputs = {"instances": [{instances: data}]};
    let classes = require('./labels_encoding.json');

    return auth.getAccessToken().then(accessToken => {
        request
            .post("https://ml.googleapis.com/v1/projects/connected-machine-learning/models/applianceml:predict")
            .send(inputs)
            .set("Authorization", `Bearer ${accessToken}`)
            .set("Content-Type", "application/json")
            .end((err, res) => {
                if (err) {
                    logger.error(err);
                    throw res.body;
                } else {
                    let probabilities = res.body.predictions[0].predictions;
                    let m = 0;
                    let max_idx = 0;
                    for (let i = 0; i < probabilities.length;i++){
                        if (probabilities[i] > m){
                            m = probabilities[i];
                            max_idx = i;
                        }
                    }
                    logger.debug(JSON.stringify({class:classes[max_idx], probability:probabilities[max_idx]}));
                    app.action('_prediction').create({
                        thng: event.thng.id,
                        customFields: {class:classes[max_idx], probability:probabilities[max_idx]}
                    }).then(data => {
                        logger.info('new prediction ' + JSON.stringify(res.body));
                        return done();
                    }).catch(err => {
                        logger.error(JSON.stringify(err));
                        return done();
                    })
                }
            })
    }).catch(err => {
        logger.error(err);
        return done();
    })
}
