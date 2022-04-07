from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/calender')
def calender():
    return render_template('calender.html')

@app.route('/about')
def about():
    return render_template('about.html')

# error handling
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(404)
def server_error(e):
    return render_template('404.html'), 404

app.run()