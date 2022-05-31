
import markdown
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from resourcey.resquery import resources_all
from cruddy.model import MyResources

# blueprint defaults https://flask.palletsprojects.com/en/2.0.x/api/#blueprint-objects
app_myresources = Blueprint('myresources', __name__,
                      url_prefix='/myresources',
                      template_folder='templates/',
                      static_folder='static',
                      static_url_path='static')


@app_myresources.route('/myresources')
@login_required
def myresources():
    return render_template('resources.html', restable=resources_all())


# Notes create/add
@app_myresources.route('/createresource/', methods=["POST"])
@login_required
def createresource():
    """gets data from form and add to Notes table"""
    if request.form:
        # construct a Notes object
        resource_object = MyResources(
            request.form.get("resource"),
            request.form.get("link"),
            request.form.get("name"),
            request.form.get("grade")
        )
        resource_object.createresource()
    return redirect(url_for('myresources.myresources'))