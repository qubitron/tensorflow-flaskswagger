import flask
from flask import Flask, request, redirect, url_for
from flasgger import Swagger
from werkzeug.utils import secure_filename
import os

from mnist_softmax import classify_image

app = Flask(__name__)
UPLOAD_FOLDER = 'image_upload'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

swagger = Swagger(app)

@app.route('/')
def get_index():
    """
    Index API, returns "Hello!"
    ---
    operationId: getPetsById
    responses:
      200:
        description: the word "Hello!"
    """
    return "Hello!"

@app.route('/number/<number>')
def get_number(number):
    """
    Repeats back a number to you
    ---
    operationId: getPetsById
    parameters:
      - name: number
        in: path
        type: string
        description: the number
    responses:
        200:
            description: Hello number!
    """

    return "Hello {}!".format(number)



@app.route('/digit', methods=['POST'])
def upload_file():
    """
    Takes a digit and attempts to classify using MNIST data
    ---
    operationId: uploadFile
    consumes:
      - multipart/form-data
    parameters:
      - name: file
        in: formData
        description: The uploaded file data
        required: true
        type: file
    """
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        return classify_image(path)
        #return redirect(url_for('uploaded_file', filename=filename))

app.run(debug=True)
