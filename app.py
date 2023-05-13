import os, sys
from flask import Flask, flash, request, redirect, url_for, render_template, send_file, request
from werkzeug.utils import secure_filename
import requests

restbai_url = 'https://api-eu.restb.ai/vision/v2/multipredict'

app = Flask(__name__)

#Pàgina inicial
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' in request.form:
            uploaded_file = request.files['file']
            if uploaded_file.filename != '':
                p = os.path.join('uploads', uploaded_file.filename)
                #uploaded_file.save(uploaded_file.filename)
                uploaded_file.save(p)
            return redirect(url_for('index'))

        if 'Kitchen' in request.form:
            return redirect(url_for('kitchen'))

    return render_template('index.html')


#Retorna una imatge guardada
@app.route('/get/<id>')
def download_file(id):
    p = os.path.join('static', 'Images', id)
    return send_file(p, as_attachment=False)

#Envia una imatge a restb.ai
@app.route('/send/<imatge>')
def send(imatge):
    imatge = imatge + '.jpg'
    p = os.path.join('static', 'Images', imatge)
    url_final = request.base_url + url_for('download_file', id=imatge)

    key = os.getenv('RESTBAI_API')
    #print(key)

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

#Entra a les opcions de la cuina
@app.route('/kitchen')
def kitchen():
    # render the new page template
    return render_template('kitchen.html')

if __name__ == '__main__':
    app.run()
