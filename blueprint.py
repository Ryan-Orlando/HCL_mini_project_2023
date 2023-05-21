from flask import Blueprint, render_template, request, jsonify, redirect, url_for, send_from_directory
from get_files import fetch_file

blueprint = Blueprint(__name__, 'blueprint')

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
#-------------------------------------

# home page
@blueprint.route('/')
def index():
    return render_template("index.html", name="Joe")

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
@blueprint.route('/json')
def json():
    args = request.args
    name = args.get('name')
    rollno = args.get('rollno')

    dic = {
        'name': name,
        'rollno': rollno
    }

    return jsonify(dic)

# redirecting
@blueprint.route('/redirect')
def redirecting():
    return redirect(url_for('blueprint.get_file'))

# get file - actual code
@blueprint.route('/get_file', methods=['GET'])
def get_file():
    if request.method == 'GET':
        return send_from_directory('adverts', fetch_file())