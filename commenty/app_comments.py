import markdown
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from commenty.appquery import comments_all_alc
from cruddy.model import Comments

# blueprint defaults https://flask.palletsprojects.com/en/2.0.x/api/#blueprint-objects
app_comments = Blueprint('comments', __name__,
                         url_prefix='/comments',
                         template_folder='templates/',
                         static_folder='static',
                         static_url_path='static')


@app_comments.route('/comments')
@login_required
def comments():
    return render_template('comments.html', comtable=comments_all_alc())


# Notes create/add
@app_comments.route('/create/', methods=["POST"])
@login_required
def create():
    """gets data from form and add to Notes table"""
    if request.form:
        # construct a Notes object
        comments_object = Comments(
            request.form.get("comment"),
        )
        comments_object.create()
    return redirect(url_for('comments.comments'))