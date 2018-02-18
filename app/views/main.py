import flask
from flask import (
    Blueprint, 
    render_template, 
    redirect, 
    url_for,
    abort, 
    flash,
    jsonify,
    request
)
from flask.ext.login import current_user
from app import app, models, db
from app.forms import post as post_forms
import random


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/posts', methods=['GET', 'POST'])
def posts():
    form = post_forms.Create()
    if form.validate_on_submit():
        post = models.Post(
            title=form.title.data,
            body=form.body.data,
            user_id=current_user.id
        )
        db.session.add(post)
        db.session.commit()
        flash('Created post successfully.')
        return redirect(url_for('posts'))

    posts = models.Post.query.all()
    return render_template(
        'posts/index.html', 
        form=form, 
        title='Posts',
        posts=[post.serialize() for post in posts]
    )

@app.route('/posts/new', methods=['GET'])
def add_post():
    form = post_forms.Create()
    return render_template(
        'posts/new.html',
        form=form,
        title='New Post'
    )

@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):

    post = models.Post.query.filter_by(id=post_id).first()

    return render_template(
        'posts/show.html',
        post=post.serialize()
    )
