from flask import Blueprint, request, render_template, redirect, flash, jsonify, make_response
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from . import db, params
from .models import Posts, Categories, Comments, User

post = Blueprint('post', __name__, static_folder='static', template_folder='templates/post')

@post.route("/<string:post_slug>",methods=['GET', 'POST'])
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    if request.method=='POST' :
        # post comments
        parent_id = request.args.get("replyto")
        delete = request.args.get("delete")
        if str(delete).isnumeric() :
            id = int(delete)
            comment = Comments.query.filter_by(id=id).first()
            db.session.delete(comment)
            db.session.commit()
            return redirect(f"/post/{post_slug}")
        parent = Comments.query.filter_by(id=parent_id).first()
        content = request.form.get('content')
        author = User.query.filter_by(id=current_user.id).first()
        if parent is not None :
            entry = Comments(content=content, post=post, author=author, parent=parent)
        else :
            entry = Comments(content=content, post=post, author=author)
        db.session.add(entry)
        db.session.commit()
        return redirect(f"/post/{post_slug}")
    post.views += 1
    db.session.commit()
    comments = Comments.query.filter_by(post_id=post.id).filter_by(parent=None).order_by(Comments.date.desc()).all()
    categories = Categories.query.filter_by().all()
    categories.sort(key=lambda category:len(category.posts), reverse=True)
    categories = categories[0:10]
    featured_post = Posts.query.order_by(Posts.views.desc()).first()
    return render_template('post.html', params=params, post=post, featured_post=featured_post, categories=categories, comments=comments)

@post.route("/edit/<string:id>",methods=["GET","POST"])
@login_required
def edit(id):
    if(request.method=='POST'):
        #add post to database
        title = request.form.get('title')
        slug = request.form.get('slug')
        content = request.form.get('content')
        categories = request.form.getlist('categories')
        slug_check = Posts.query.filter_by(slug=slug).first()
        if slug_check is not None and slug_check.id!=int(id) :
            message = str(slug_check.id)+" "+slug_check.title+str(slug_check.id==int(id))
            flash(message+"Slug already taken.", "danger")
            return redirect(f"/post/edit/{id}")
        if(id=='0'):
            #add a new post
            entry = Posts(title=title, slug=slug ,author=current_user, content=content, date=datetime.now())
            for category in categories :
                category = category.lower()
                c = Categories.query.filter_by(name=category).first()
                if c is None :
                    slug = ''.join(i if i.isalnum() else '-' for i in category)
                    c = Categories.query.filter_by(slug=slug).first()
                    i = 1
                    while c is not None :
                        slug = slug+str(i)
                        c = Categories.query.filter_by(slug=slug).first()
                        i += 1
                    c = Categories(name=category, slug=slug)
                entry.categories.append(c)
            db.session.add(entry)
            db.session.commit()
        else:
            #edit old post
            post=Posts.query.filter_by(id=id).first()
            post.title=title
            post.slug=slug
            post.content=content
            post.categories.clear()
            for category in categories :
                category = category.lower()
                c = Categories.query.filter_by(name=category).first()
                if c is None :
                    slug = ''.join(i if i.isalnum() else '-' for i in category)
                    c = Categories.query.filter_by(slug=slug).first()
                    i = 1
                    while c is not None :
                        slug = slug+str(i)
                        c = Categories.query.filter_by(slug=slug).first()
                        i += 1
                    c = Categories(name=category, slug=slug)
                post.categories.append(c)
            db.session.commit()
        return redirect(f"/profile/{current_user.slug}")
    post=Posts.query.filter_by(id=id).first()
    return render_template('post_edit.html',id=id,params=params,post=post)

@post.route('/imageuploader', methods=['POST'])
@login_required
def imageuploader():
    file = request.files.get('file')
    if file:
        filename = secure_filename(file.filename)
        filename = filename.lower()
        img_fullpath = os.path.join("app/static/user_uploads/post/", filename)
        file.save(img_fullpath)
        return jsonify({'location' : filename})

    # fail, image did not upload
    output = make_response(404)
    output.headers['Error'] = 'Image failed to upload'
    return output

@post.route('/delete/<string:id>', methods=['POST'])
@login_required
def delete(id):
    post=Posts.query.filter_by(id=id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(f"/profile/{current_user.slug}")
