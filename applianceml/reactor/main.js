process.env.GOOGLE_APPLICATION_CREDENTIALS = './application_default_credentials.json';
const {vibrationProperty, padSequence, transformFnDecorator, standardization} = require('./preprocess.js');
const request = require('superagent');
const np = require('jsnumpy');
const {auth} = require('google-auth-library');




// @filter(onThngPropertiesChanged) propertyChangeNew.magnitude=*
function onThngPropertiesChanged(event) {
    const propertyUpdates = JSON.parse(event.changes.magnitude.newValue);
    let data = vibrationProperty(propertyUpdates, [1, 2, 3]);
    let modelConfigParams = require('./model_config_params.json');
    if (data.length< modelConfigParams.lookback) {
        logger.warn(JSON.stringify(data));
        done();
    } else {
        data = data.slice(0,100);
    const f = transformFnDecorator(standardization, modelConfigParams);
    data = f(data);
    // data = padSequence(data, modelConfigParams.lookback);


    let inputs = {"instances": [{instances: data}]};
    let classes = require('./labels_encoding.json');

    return auth.getAccessToken().then(accessToken => {
        request
            .post("https://ml.googleapis.com/v1/projects/"+modelConfigParams.google_project +"/models/" + modelConfigParams.model_name + "/versions/v1:predict")
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
                    app.action('_ml_prediction').create({
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
    })}
}
