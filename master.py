from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(404)
def server_error(e):
    return render_template('404.html'), 404

app.run()