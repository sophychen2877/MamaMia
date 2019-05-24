from flask import Flask, jsonify, request,render_template, abort
from models import Prediction_Models
import pandas as pd

app = Flask(__name__)
@app.route('/predict/<string:model_name>', methods=['POST'])
def predict(model_name):
    user_json = request.get_json()
    test_data = pd.DataFrame(user_json, index=[0])
    model = None
    try:
        model = Prediction_Models.load_model_by_name(model_name)
    except:
        jsonify({'message': 'error occurred when loading the model'}), 500
    if model:
            result = int(model.model_func.predict(test_data))
    else:
        return jsonify({'message': 'there is no such model'}), 404
    return render_template("predict.html",prediction_result=result)

@app.route('/model/<string:model_name>', methods=['POST','PUT'])
def train_model(model_name):

        #request get parameters of the model
    param_json = request.get_json()
    model = Prediction_Models.load_model_by_name(model_name)
    if not model:
        try:
            model = Prediction_Models(model_name, **param_json)
        except:
            return jsonify({'message': 'problem occured when build the model'}),500
        try:
            model.train_model(**param_json)
        except:
            return jsonify({'message': 'problem occured when training the model'}), 500
        if request.method == 'POST':
            return jsonify({'message': f'model {model.model_name} has been built'})
        elif request.method == 'PUT':
            return jsonify({'message': f'model {model.model_name} has been re-trained and updated'})
        return render_template('train.html',)

#display model attributes (of latest created model)
@app.route('/model/<string:model_name>', methods=['GET'])
def display_model(model_name):
    try:
        model = Prediction_Models.load_model_by_name(model_name)
    except:
        return jsonify({'message': 'model does not exist'}), 404
    #return jsonify(model.load_model_attributes())
    return render_template('display.html')
    return jsonify(model.json())

if __name__ == '__main__':
    app.run(port=5000, debug=True)
