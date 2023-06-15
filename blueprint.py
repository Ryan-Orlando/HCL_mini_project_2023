from flask import Blueprint, render_template, request, jsonify, redirect, url_for, send_from_directory, session, abort, send_file

from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
import requests

import os
import pathlib
import json

from get_files import fetch_file, upload_file
from google_drive import create_folder, upload_to_folder, fetch_file_drive

#-------------------------------------------------------------------------

blueprint = Blueprint(__name__, 'blueprint')

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" # to allow Http traffic for local development

# Request headers
@blueprint.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r

# protected wrapper decorater
def login_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()
    return wrapper
#-------------------------------------

# home page
@blueprint.route('/')
def index():
    return render_template("index.html", name="HCL Mini Project")

# about page
@blueprint.route('/about')
def about():
    return 'About Page'

# profile page
@blueprint.route('/profile')
def profile():
    args = request.args
    name = args.get('name')
    return render_template("index.html", name=name)

# json page
# @blueprint.route('/json')
# def json():
#     args = request.args
#     name = args.get('name')
#     rollno = args.get('rollno')

#     dic = {
#         'name': name,
#         'rollno': rollno
#     }

#     return jsonify(dic)

# redirecting
@blueprint.route('/redirect')
def redirecting():
    return redirect(url_for('blueprint.get_file'))

# get file - locally
@blueprint.route('/get_file', methods=['GET'])
def get_file():
    if request.method == 'GET':
        return send_from_directory('adverts', fetch_file())

# uploading file in local
@blueprint.route('/post_file', methods=['POST'])
def post_file():
    if request.method == 'POST':
        
        files = request.files.getlist('file')

        if files[0].filename == '':                     # suggestion of uploading empty list of files
            return render_template("no_files.html")

        for file in files:
            upload_file(file)
    
    return render_template("index.html")

# uploading file in google drive
@blueprint.route('/post_file_drive', methods=['POST'])
def post_file_drive():
    if request.method == 'POST':

        folder_id = create_folder(flow)
        
        files = request.files.getlist('file')

        if files[0].filename == '':                     # suggestion of uploading empty list of files
            return render_template("no_files.html")

        for file in files:
           upload_to_folder(flow, folder_id, file)
    
    return render_template("upload.html")

# getting files from drive
@blueprint.route('/get_file_drive', methods=['GET'])
def get_file_drive():
    if request.method == 'GET':

        folder_id = create_folder(flow)

        file = fetch_file_drive(flow, folder_id)

        if file is None:
            return render_template("no_files.html")

        return send_file(file, mimetype='image/jpeg')

#---------- Oauth Google ----------------

client_key = json.load(open("client_key.json"))         # get the client key from json
GOOGLE_CLIENT_ID = client_key["web"]["client_id"]

client_secret = os.path.join(pathlib.Path(__file__).parent, "client_key.json")

#-----------flow----------------
flow = Flow.from_client_secrets_file(

    client_secrets_file=client_secret,
    scopes= ['https://www.googleapis.com/auth/userinfo.profile', 
             'https://www.googleapis.com/auth/userinfo.email',
             'https://www.googleapis.com/auth/drive',
             'openid'],
    redirect_uri="http://127.0.0.1:5000/callback"
                                    )
#-----------

@blueprint.route('/login')
def login():
    authorization_url, state = flow.authorization_url()
    print(session)
    session["state"] = state
    return redirect(authorization_url)

@blueprint.route('/logout')
def logout():

    session.clear() 
    return redirect(url_for('blueprint.index'))
    

@blueprint.route('/callback')
def callback():

    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")

    return redirect("/protected")

@blueprint.route('/protected')
@login_required
def protected():
    return render_template("logged.html", 
                            user=session["name"])
