import os, sys
from flask import Flask, flash, request, redirect, url_for, render_template, send_file, request
from werkzeug.utils import secure_filename
import requests
from dotenv import load_dotenv


restbai_url = 'https://api-eu.restb.ai/vision/v2/multipredict'

load_dotenv()  

app = Flask(__name__)

#Pàgina inicial
@app.route('/', methods=['GET', 'POST'])
def index():
    print("index")
    if request.method == 'POST':
        uploaded_file = request.files['file']
        t = request.form['prova']
        print(t)
        if uploaded_file.filename != '':
            p = os.path.join('static', 'Images', uploaded_file.filename)            
            uploaded_file.save(p)
        #return redirect(url_for('index'))
        return redirect(url_for('send', imatge=uploaded_file.filename)) 
    return render_template('index.html')

       


#Retorna una imatge guardada
@app.route('/get/<id>')
def download_file(id):
    print("get")
    p = os.path.join('static', 'Images', id)
    return send_file(p, as_attachment=False)

#Envia una imatge a restb.ai
@app.route('/send/<imatge>')
def send(imatge):
    print("send")
    p = os.path.join('static', 'Images', imatge)
    url_final = request.base_url.replace('send', 'get') 

    key = os.getenv('RESTBAI_API')

    payload = {
        'client_key': key,
        'model_id': 're_condition_c1c6',
        'image_url': url_final
    }
    # Make the API request
    response = requests.get(restbai_url, params=payload)
    # The response is formatted in JSON
    json_response = response.json()

    return render_template('result.html', resultat=json_response)

if __name__ == '__main__':
    app.run(debug=True)
