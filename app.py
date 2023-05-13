import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "principal"

@app.route('/foto')
def foto():
    img = os.path.join('static', 'Image')
    file = os.path.join(img, 'imatge.png')
    return render_template('img_render.html', image=file)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

