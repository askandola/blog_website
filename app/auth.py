from flask import Blueprint, redirect, flash, request, render_template, g
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from . import params, db
from .models import User

auth = Blueprint('auth', __name__, static_folder='static', template_folder='templates/auth')

@auth.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method == "POST" :
        email = request.form['email']
        name = request.form['name']
        pw = request.form['pw']
        pwr = request.form['pwr']
        if pw != pwr :
            flash("Password didn't match", "danger")
            return redirect("/auth/register")
        if len(pw)<8 or len(pw)>30 :
            flash("Password length must be within 8 characters and 30 characters", "danger")
            return redirect("/auth/register")
        user = User.query.filter_by(email = email).first()
        if user is not None :
            flash("Email already exists", "danger")
            return redirect("/auth/register")
        slug = ''.join(i if i.isalnum() else '-' for i in name)
        slug_check = User.query.filter_by(slug=slug).first()
        i = 1
        while slug_check is not None :
            slug = slug+str(i)
            slug_check = User.query.filter_by(slug=slug).first()
            i += 1
        user = User(email = email, name = name, slug=slug, password_hash = generate_password_hash(pw))
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Account created successfully.", "success")
        return redirect(f"/profile/{current_user.slug}")
    return render_template("signup.html", params = params)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if(request.method=='POST'):
        email = request.form.get('email')
        pw = request.form.get('pw')
        user = User.query.filter_by(email = email).first()
        remember_me = request.form.get("remember-me")
        if remember_me=="true" :
            remember=True
        else :
            remember=False
        if user is not None and check_password_hash(user.password_hash, pw) :
            next = request.args.get('next')
            login_user(user, remember=remember)
            return redirect(next or f"/profile/{current_user.slug}")
        flash("Invalid email or password", "danger")
        return redirect("/auth/login")
    return render_template("login.html", params = params)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@auth.route("/edit", methods=['GET', 'POST'])
@login_required
def edit() :
    if request.method=='POST' :
        name = request.form.get('name')
        slug = request.form.get('slug')
        about_me = request.form.get('about_me')
        f = request.files['image']
        filename = secure_filename(f.filename)
        user = User.query.filter_by(id=current_user.id).first()
        user.name = name
        user.about_me = about_me
        slug_check = User.query.filter_by(slug=slug).first()
        if slug_check is not None and slug_check.id!=current_user.id :
            flash("Slug already taken.", "danger")
            return redirect("/auth/edit")
        user.slug = slug
        if filename!=user.img_url and filename!="" :
            f.save(os.path.join("./static/user_uploads/profile", filename))
            user.img_url = filename
        db.session.commit()
        return redirect(f"/profile/{current_user.slug}")
    return render_template("edit.html", params=params)

@auth.route("/change-email", methods=['GET', 'POST'])
@login_required
def change_email() :
    if request.method == "POST" :
        email = request.form.get('email')
        pw = request.form.get('pw')
        user = User.query.filter_by(id=current_user.id).first()
        if check_password_hash(user.password_hash, pw) :
            user.email = email
            db.session.commit()
            flash("Email changed succesfully", "success")
            return redirect(f"/profile/{current_user.slug}")
        flash("wrong password", "danger")
        return redirect("/auth/change-email")
    return render_template("change_email.html", params=params)

@auth.route("/change-password", methods=['GET', 'POST'])
@login_required
def change_password() :
    if request.method == 'POST' :
        old_pw = request.form.get('old_pw')
        new_pw = request.form.get('new_pw')
        new_pwr = request.form.get('new_pwr')
        user = User.query.filter_by(id=current_user.id).first()
        if not check_password_hash(user.password_hash, old_pw) :
            flash("wrong password", "danger")
            return redirect("/auth/change-password")
        if new_pw != new_pwr :
            flash("Passwords didn't match", "danger")
            return redirect("/auth/change-password")
        if len(new_pw)<8 or len(new_pw)>30 :
            flash("Your new password must be 8-30 characters long.", "danger")
            return redirect("/auth/change-password")
        user.password_hash = generate_password_hash(new_pw)
        db.session.commit()
        flash("Password changed successfully", "success")
        return redirect(f"/profile/{current_user.slug}")
    return render_template("change_password.html", params=params)

@auth.route("/delete", methods=['GET', 'POST'])
@login_required
def delete() :
    if request.method == "POST" :
        pw = request.form.get('pw')
        user = User.query.filter_by(id=current_user.id).first()
        if check_password_hash(user.password_hash, pw) :
            db.session.delete(user)
            db.session.commit()
            flash("Account deleted successfully", "success")
            return redirect("/")
        flash("Wrong password", "danger")
        return redirect("/auth/delete")
    return render_template("delete.html", params=params)
