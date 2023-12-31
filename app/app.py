from flask import Flask, render_template, request, jsonify
import numpy as np
from joblib import load
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import uuid


app = Flask(__name__)

def make_picture(training_data_filename, model, new_input_np_arr, output_file):
  data = pd.read_pickle(training_data_filename)
  age = data['Age']
  data = data[age > 0]
  age = data['Age']
  height = data['Height']
  x_new = np.array(list(range(19))).reshape(19,1)
  preds = model.predict(x_new)

  fig = px.scatter(x=age, y=height, title = 'heigh vs age', labels={'x': 'Age (Years)', 'y': 'Height (inches)'})

  fig.add_trace(go.Scatter(x=x_new.reshape(19), y = preds, mode = 'lines', name='Model'))

  new_preds = model.predict(new_input_np_arr)

  fig.add_trace(go.Scatter(x=new_input_np_arr.reshape(len(new_input_np_arr)), y=new_preds, name='New Outputs', mode='markers', marker=dict(color='purple', size=20, line=dict(color='purple', width=2))))
  
  fig.write_image(output_file, width=800, engine='kaleido')
  fig.show()

def floats_string_to_np_arr(floats_str):
    def is_float(s):
        try: 
            float(s)
            return True
        except:
            return False
    floats = np.array([float(x) for x in floats_str.split(',') if is_float(x)])
    return floats.reshape(len(floats), 1)

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    request_type_str = request.method
    if request_type_str == 'GET':
        return render_template('index.html', href='static/base_pic.svg')
    else:
        text = request.form['text']
        random_string = uuid.uuid4().hex
        path = 'static/' + random_string + '.svg'
        model = load('model.joblib')
        np_arr = floats_string_to_np_arr(text)
        make_picture('AgesAndHeights.pkl', model, np_arr, path)

        return render_template('index.html', href=path)
    

