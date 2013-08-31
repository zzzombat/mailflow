from flask import Flask

app = Flask(__name__)
import views

def main():
    app.run(debug = True)
