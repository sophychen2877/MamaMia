from flask import Flask, jsonify, request
import warnings
from models import Prediction_Models
import pandas as pd
from jinja2 import Template


'''
template = Template('Hello {{ name }}!')
template.render(name='John Doe')
'''
#warnings.filterwarnings("ignore")

app = Flask(__name__)
#jwt = JWT(app, authenticate, identity)

#post method returns the prediction
#@jwt
@app.route('/predict/<string:model_name>', methods=['POST'])
def predict(model_name):
    user_json = request.get_json()
    test_data = pd.DataFrame(user_json, index=[0])
    try:
        model = Prediction_Models.load_model_by_name(model_name)
    except:
        jsonify({'message': 'error occurred when loading the model'}), 500
    if model:
            result = int(model.predict(test_data))
    else:
        return jsonify({'message': 'there is no such model'}), 404
    return jsonify(prediction_result=result)


@app.route('/model/<string:model_name>', methods=['POST','PUT'])
def train_model(model_name):
    #request get parameters of the model
    param_json = request.get_json()
    model = Prediction_Models.load_model_by_name(model_name)
    if model:
        try:
            model.train_model(**param_json)
        except:
            return jsonify({'message': 'problem occured when re-train the model'}), 500
    else:
        try:
            model = Prediction_Models(model_name, param_json)
        except:
            return jsonify({'message': 'problem occured when build the model'}),500

    return jsonify({'message': f'model {model.model_name} has been built'})


@app.route('/model/<string:model_name>', methods=['GET'])
def display_model(model_name):
    try:
        model = Prediction_Models.load_model_by_name(model_name)
    except:
        return jsonify({'message': 'model does not exist'}), 404
    return jsonify(model.load_model_attributes())

if __name__ == '__main__':
    app.run(port=5000, debug=True)
