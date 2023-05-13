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
    if request.method == 'POST':
        if 'Kitchen' in request.form:
            return redirect(url_for('kitchen'))
        
        elif 'Bathroom' in request.form:
            return redirect(url_for('bathroom'))

    return render_template('index.html')

#Retorna una imatge guardada
@app.route('/get/<id>')
def download_file(id):
    p = os.path.join('uploads', id)
    return send_file(p, as_attachment=False)

#Envia una imatge a restb.ai
@app.route('/send/<imatge>')
def send(imatge):
    p = os.path.join('static', 'Images', imatge)
    url_final = request.base_url.replace('send', 'get') 

    key = os.getenv('RESTBAI_API')
    #key = config.RESTBAI_API
    #print(key)

    payload = {
        'client_key': os.environ.get("restbai_api"),
        'model_id': 're_condition_c1c6',
        'image_url': url_final
    }
    # Make the API request
    response = requests.get(restbai_url, params=payload)
    # The response is formatted in JSON
    json_response = response.json()

    print(json_response)
    print("FINAL")
    return render_template('result.html', resultat=json_response)

#Entra a les opcions de la cuina
@app.route('/kitchen', methods=['GET', 'POST'])
def kitchen():
    if request.method == 'POST':
        if 'Fridge' in request.form:
            print('Fridge', file=sys.stderr)
            return redirect(url_for('fridge'))
        
        elif 'Stove' in request.form:
            return redirect(url_for('stove'))
    
    return render_template('kitchen.html')

@app.route('/fridge', methods=['GET', 'POST'])
def fridge():
    if request.method == 'POST':
        if 'file' in request.form:
            uploaded_file = request.files['file']
            if uploaded_file.filename != '':
                p = os.path.join('uploads', uploaded_file.filename)
                uploaded_file.save(uploaded_file.filename)
                uploaded_file.save(p)
            return redirect(url_for('fridge'))

    return render_template('fridge.html')

@app.route('/stove', methods=['GET', 'POST'])
def stove():
    if request.method == 'POST':
        if 'file' in request.form:
            uploaded_file = request.files['file']
            if uploaded_file.filename != '':
                p = os.path.join('uploads', uploaded_file.filename)
                uploaded_file.save(uploaded_file.filename)
                uploaded_file.save(p)
            return redirect(url_for('stove'))

    return render_template('stove.html')

#Entra a les opcions del bany
@app.route('/bathroom', methods=['GET', 'POST'])
def bathroom():
    if request.method == 'POST':
        if 'Toilet' in request.form:
            return redirect(url_for('toilet'))
        
        elif 'Sink' in request.form:
            return redirect(url_for('sink'))
    
    return render_template('bathroom.html')

@app.route('/toilet', methods=['GET', 'POST'])
def toilet():
    if request.method == 'POST':
        if 'file' in request.form:
            uploaded_file = request.files['file']
            if uploaded_file.filename != '':
                p = os.path.join('uploads', uploaded_file.filename)
                uploaded_file.save(uploaded_file.filename)
                uploaded_file.save(p)
            return redirect(url_for('toilet'))

    return render_template('toilet.html')

@app.route('/sink', methods=['GET', 'POST'])
def sink():
    if request.method == 'POST':
        if 'file' in request.form:
            uploaded_file = request.files['file']
            if uploaded_file.filename != '':
                p = os.path.join('uploads', uploaded_file.filename)
                uploaded_file.save(uploaded_file.filename)
                uploaded_file.save(p)
            return redirect(url_for('sink'))

    return render_template('sink.html')

if __name__ == '__main__':
    app.run(debug=True)
