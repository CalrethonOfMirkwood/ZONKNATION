
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from cruddy.query import user_by_id
from cruddy.model import Resources

# blueprint defaults https://flask.palletsprojects.com/en/2.0.x/api/#blueprint-objects
app_resources = Blueprint('resources', __name__,
                      url_prefix='/resources',
                      template_folder='templates/resourcey/',
                      static_folder='static',
                      static_url_path='static')


@app_resources.route('/resources')
@login_required
def resources():
    return render_template('resources.html', retable=Resources)


# Notes create/add
@app_resources.route('/createresource/', methods=["POST"])
@login_required
def createresource():
    """gets data from form and add to Notes table"""
    if request.form:
        # construct a Notes object
        resource_object = Resources(
            request.form.get("resource"),
            request.form.get("link"),
            request.form.get("name"),
            request.form.get("grade")
        )
        resource_object.createresource()
    return redirect(url_for('resources.resources'))