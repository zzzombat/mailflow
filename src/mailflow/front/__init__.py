from flask import Flask

app = Flask(__name__, static_folder='static', static_url_path='/static')
import views

def main():
    app.run(debug = True)
