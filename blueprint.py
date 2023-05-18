from flask import Blueprint, render_template, request, jsonify, redirect, url_for, send_from_directory
from get_files import fetch_file

blueprint = Blueprint(__name__, 'blueprint')

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