from flask import render_template, redirect, flash, url_for, request, abort, Blueprint
from blog.models import Users, Posts
from PIL import Image
import os
from blog.user.forms import RegisterForm, LoginForm, UpdateForm, RestRequestForm, RestPasswordForm
from blog.user.utils import send_reset_email
from flask_login import login_user, logout_user, login_required, current_user
from blog import db, bcrypt

end_user = Blueprint('end_user', __name__)

@end_user.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username= form.username.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember= form.remember.data)
            next_page = request.args.get('next') #redirect(next_page) if next_page else
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash("Incorrect Username/Password","danger")
    return render_template("login.html", title= "Login", form= form )


@end_user.route("/register", methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegisterForm()
    if form.validate_on_submit():
        pws_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(username= form.username.data, password= pws_hash, email= form.email.data)
        db.session.add(user)
        db.session.commit()
        flash("Succesfully registered, now you can login!", "success")
        return redirect(url_for('end_user.login'))
    return render_template("register.html", title="Register", form= form )

@end_user.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")




@end_user.route("/setting", methods=['GET', 'POST'])
@login_required
def setting():
    form = UpdateForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!','success')
        return redirect(url_for('end_user.setting'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='picture/' + current_user.picture)
    return render_template('setting.html', title='setting', image_file=image_file, form=form)



@end_user.route('/user/<string:username>', methods=['GET', 'POST'])
def User_profile(username):
    page = request.args.get('page', 1 ,type= int)
    user = Users.query.filter_by(username=username).first_or_404()
    posts= Posts.query.filter_by(author = user).order_by(Posts.time.desc())\
    .paginate(page= page, per_page= 5)
    return render_template('user_profile.html', posts=posts, user= user)



@end_user.route('/rest_request', methods=['GET', 'POST'])
def RestPequest():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RestRequestForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent. Follow the instruction in your email to rest the password!','info')
        return redirect(url_for('end_user.login'))
    return render_template('rest_request.html', title= 'Rest password', form= form)


@end_user.route('/rest_password/<token>', methods=['GET', 'POST'])
def RestPassword(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = Users.verify_token(token)
    if not user:
        flash('This invaild/expired token. please try again','warning')
        return redirect(url_for('end_user.RestPequest'))
    form = RestPasswordForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password= hashed
        db.session.commit()
        flash('Password has been Updated! Now you can log in.','success')
        return redirect(url_for('end_user.login'))
    return render_template('reset_password.html', form= form)


