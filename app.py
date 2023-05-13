import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            p = os.path.join('uploads', uploaded_file.filename)
            #uploaded_file.save(uploaded_file.filename)
            uploaded_file.save(p)
        return redirect(url_for('index'))
    return render_template('index.html')

#url_for('download_file', id=nom)
@app.route('/get_image/<id>')
def download_file(id):
    p = os.path.join('uploads', id)
    return send_file(p, as_attachment=True)

if __name__ == '__main__':
    app.run()