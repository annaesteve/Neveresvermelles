import os, sys
from flask import Flask, request, redirect, url_for, render_template, send_file, request
import requests, replicate
from dotenv import load_dotenv

restbai_url = 'https://api-eu.restb.ai/vision/v2/multipredict'
prompt = ''

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

    key = os.getenv('RESTBAI_API')      #clau API restb.ai   

    #foto original passada per l'AI
    url_final = replicate.run(
        "timothybrooks/instruct-pix2pix:30c1d0b916a6f8efce20493f5d61ee27491ab2a60437c13c588468b9810ec23f",
        input={"image": open(p, "rb"), "prompt": ''}
    )[0]   

    #restb.ai foto original (no funciona)
    payload_original = {
        'client_key': key,
        'model_id': 're_condition_c1c6',
        'image_url': url_final
    }    
    response_original = requests.get(restbai_url, params=payload_original)    
    json_response_original = response_original.json()
    score_original = json_response_original["response"]["solutions"]["re_condition_c1c6"]["score"]
    
    #enllaços de les fotos modificades
    output = replicate.run(
        "timothybrooks/instruct-pix2pix:30c1d0b916a6f8efce20493f5d61ee27491ab2a60437c13c588468b9810ec23f",
        input={"image": open(p, "rb"), "prompt": prompt, "num_outputs":4, "image_guidance_scale":2, "guidance_scale":7}
    )

    print(output)

    scores = []
    imatges = []
    for i in range(len(output)):
        url = output[i]    
        payload = {
            'client_key': key,
            'model_id': 're_condition_c1c6',
            'image_url': output[i]
        }
        response = requests.get(restbai_url, params=payload)        
        json_response = response.json()

        if json_response != None:
            scores.append(json_response["response"]["solutions"]["re_condition_c1c6"]["score"])
        else:
            scores.append(-1);
    
        img_response = requests.get(url)
        pathGenerated = os.path.join('static', 'Generated', str(i)+'.jpg')

        with open(pathGenerated, "wb") as f:            
            f.write(img_response.content)
        
        imatges.append('/'+pathGenerated)
    
    print(imatges)
    return render_template('result.html', score0 = score_original, 
                           score1=scores[0], score2=scores[1], score3=scores[2], score4=scores[3], cerca=prompt,
                           img_original=('/'+p), img0=imatges[0], img1=imatges[1], img2=imatges[2], img3=imatges[3])

if __name__ == '__main__':
    app.run(debug=True)
