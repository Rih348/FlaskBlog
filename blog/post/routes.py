from flask import render_template, redirect, flash, url_for, request, abort, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from blog import db, bcrypt
from blog.models import Users, Posts
from blog.post.forms import PostForm


posts_ = Blueprint('posts_', __name__ )

@posts_.route('/post/new', methods=['GET', 'POST'])
@login_required
def Postform():
    form = PostForm()
    if form.validate_on_submit():
        post = Posts(title= form.title.data, content= form.content.data, author= current_user )
        db.session.add(post)
        db.session.commit()
        flash('Post added successfully','info')
        return redirect(url_for('main.home'))
    return render_template("create_post.html", title= 'Posts', legend= 'New post', form= form)


@posts_.route('/post/<int:post_id>',  methods=['GET', 'POST'])
def PostID(post_id):
    post = Posts.query.get_or_404(post_id)
    return render_template('post.html', title= post.title , post= post)


@posts_.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def PostUpdate(post_id):
    post = Posts.query.get_or_404(post_id)
    if post.author != current_user:
        abort(404)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post updated successfully!','info')
        return redirect(url_for('main.home'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template("create_post.html", title= post.title , legend='Update post', form= form)


@posts_.route('/post/<int:post_id>/delete', methods=['POST'])
def PostDelete(post_id):
    post = Posts.query.get_or_404(post_id)
    if post.author != current_user:
        abort(404)
    db.session.delete(post)
    db.session.commit()
    flash('Post has been deleted!','info')
    return redirect(url_for('main.home'))

