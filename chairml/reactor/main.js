process.env.GOOGLE_APPLICATION_CREDENTIALS = './application_default_credentials.json';
const {vibrationProperty, padSequence, transformFnDecorator, standardization} = require('./preprocess.js');
const request = require('superagent');
const np = require('jsnumpy');
const {auth} = require('google-auth-library');




// @filter(onThngPropertiesChanged) propertyChangeNew.magnitude=*
function onThngPropertiesChanged(event) {
    const propertyUpdates = JSON.parse(event.changes.magnitude.newValue);
    let data = vibrationProperty(propertyUpdates, [0, 1, 2, 3]);
    const f = transformFnDecorator(standardization, require('./fit_params.json'));
    logger.info('debug hello world');
    data = f(data);
    data = padSequence(data, 40);
    data = np.transpose(data);


    let inputs = {"instances": [{instances: data}]};
    auth.getAccessToken().then(accessToken => {
        request
            .post("https://ml.googleapis.com/v1/projects/connected-machine-learning/models/keras_chairml/versions/v1:predict")
            .send(inputs)
            .set("Authorization", `Bearer ${accessToken}`)
            .set("Content-Type", "application/json")
            .end((err, res) => {
                if (err) {
                    throw res.body;
                } else {
                    app.action('_eventClassification').create({
                        thng: event.thng.id,
                        customFields: res.body
                    }).then(data => {
                        logger.info('new prediction ' + JSON.stringify(res.body));
                        done();
                    }).catch(err => {
                        logger.error(err);
                        done();
                    })
                }
            })
    }).catch(err => {
        logger.error(err);
        done();
    })
}
