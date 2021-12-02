from __future__ import print_function

import base64
import io

import flask
from flask import Flask, request, abort, jsonify, send_from_directory
from google.cloud import vision
import os
import requests
from requests import api

UPLOAD_DIRECTORY = "/Users/RV/Desktop/nexTurn/assignment/Vision/uploads"

os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"] = "path to your google auth json"
os.environ["GRPC_VERBOSITY"] = "DEBUG"
os.environ["GRPC_TRACE"] = "handshaker"
app = flask.Flask(__name__)
app.config["DEBUG"] = True


# to post file
@app.route("/api/files/<filename>", methods=["POST"])
def post_file(filename):
    if "/" in filename:
        # Return 400 BAD REQUEST
        os.abort(400, "no subdirectories allowed")

    im_b64 = request.json['image']
    # convert it into bytes
    img_bytes = base64.b64decode(im_b64.encode('utf-8'))

    with open(os.path.join(UPLOAD_DIRECTORY, filename), "wb") as fp:
        fp.write(img_bytes)
    # Return 201 CREATED
    return "", 201


# A route to return the home page
@app.route('/', methods=['GET'])
def home():
    return "<h1>Count of Faces</h1><p>This site is a prototype API to count number of faces in an image using cloud vision tool.</p>"


# A route to return number of faces
@app.route('/api/num', methods=['GET'])
def api_num():
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    with open(os.path.join(UPLOAD_DIRECTORY, "first.jpg"), "rb") as ir:
        content = ir.read()
    image.content = content
    response = client.face_detection(image=image)
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return jsonify(len(response.face_annotations))


app.run()
