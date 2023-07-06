from flask import Flask
from blueprint import blueprint
import json

client_key = json.load(open("client_key.json"))

# flask app
app = Flask(__name__)
app.secret_key = client_key['web']['client_secret']
app.config['UPLOAD_FOLDER'] = 'adverts'

# blueprint
app.register_blueprint(blueprint, url_prefix='/')

# running the flask app
if __name__ == '__main__':
    app.run(debug=True)