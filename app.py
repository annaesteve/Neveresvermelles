import os, sys
from flask import Flask, flash, request, redirect, url_for, render_template, send_file, request
from werkzeug.utils import secure_filename
import requests, replicate
from dotenv import load_dotenv


restbai_url = 'https://api-eu.restb.ai/vision/v2/multipredict'
prompt = 'sink'

load_dotenv()  

app = Flask(__name__)

#Pàgina inicial
@app.route('/', methods=['GET', 'POST'])
def index():
    global prompt
    if request.method == 'POST':
        uploaded_file = request.files['file']
        prompt = request.form['prova']
        
        if uploaded_file.filename != '':
            p = os.path.join('static', 'Images', uploaded_file.filename)            
            uploaded_file.save(p)
        #return redirect(url_for('index'))
        return redirect(url_for('send', imatge=uploaded_file.filename)) 
    return render_template('index.html')       


#Retorna una imatge guardada
@app.route('/get/<id>')
def download_file(id):
    p = os.path.join('static', 'Images', id)
    return send_file(p, as_attachment=False)

#Envia una imatge a restb.ai
@app.route('/send/<imatge>')
def send(imatge):
    p = os.path.join('static', 'Images', imatge)
    url_final = request.base_url.replace('send', 'get') 

    key = os.getenv('RESTBAI_API')

    payload_original = {
        'client_key': key,
        'model_id': 're_condition_c1c6',
        'image_url': url_final
    }
    # Make the API request
    response_original = requests.get(restbai_url, params=payload_original)
    # The response is formatted in JSON
    json_response_original = response_original.json()

    
    #os.environ["REPLICATE_API_TOKEN"] = 'r8_MEI4HMiWMay10i6BA6AP6VHkD1rQZnK1i2UXN'
    output = replicate.run(
        "timothybrooks/instruct-pix2pix:30c1d0b916a6f8efce20493f5d61ee27491ab2a60437c13c588468b9810ec23f",
        input={"image": open(p, "rb"), "prompt": prompt}
    )

    print(output)
    
    payload_modificada = {
        'client_key': key,
        'model_id': 're_condition_c1c6',
        'image_url': output[0]
    }

    response_modificada = requests.get(restbai_url, params=payload_modificada)
    # The response is formatted in JSON
    json_response_modificada = response_modificada.json()

    score_modificada = json_response_modificada["response"]["solutions"]["re_condition_c1c6"]["score"]

    return render_template('result.html', score_original=json_response_original, score1=score_modificada, cerca=prompt)

if __name__ == '__main__':
    app.run(debug=True)
