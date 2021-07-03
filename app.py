from flask import Flask,render_template,request,session,redirect,flash
from flask_sqlalchemy import SQLAlchemy
# from flask_mail import Mail,Message
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import math
import json

with open('config.json','r') as c:
    params=json.load(c)["params"]

app=Flask(__name__)

app.secret_key='super-secret-key'

app.config['UPLOAD_FOLDER']=params['upload_folder']

# app.config.update(
#     MAIL_SERVER='smtp.gmail.com',
#     MAIL_PORT='465',
#     MAIL_USE_SSL=True,
#     MAIL_USERNAME=params['mail_username'],
#     MAIL_PASSWORD=params['mail_password']
# )
# mail=Mail(app)

if(params['local_server']):
    app.config['SQLALCHEMY_DATABASE_URI']=params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI']=params['production_uri']

db=SQLAlchemy(app)


class Contact(db.Model):
    id=db.Column(db.Integer,primary_key=True,unique=True)
    name=db.Column(db.String(50),nullable=False)
    email=db.Column(db.String(50),nullable=False)
    message=db.Column(db.String(500),nullable=False)
    date=db.Column(db.DateTime,default=datetime.now())


class Posts(db.Model):
    id=db.Column(db.Integer,primary_key=True,unique=True)
    title=db.Column(db.String(100),nullable=False)
    slug=db.Column(db.String(50),nullable=False)
    author=db.Column(db.String(40),nullable=False)
    content=db.Column(db.String(3000),nullable=False)
    img_url=db.Column(db.String(30),nullable=False)
    date=db.Column(db.DateTime,nullable=False,default=datetime.now())


@app.route("/",methods=['GET'])
def index():
    posts=Posts.query.filter_by().all()
    last=math.ceil(len(posts)/int(params['number_of_posts']))
    page=request.args.get('p')
    if(not str(page).isnumeric()):
        page=1
    page=int(page)
    if(page==1):
        prev="#"
        next="?p="+str(page+1)
    elif(page==last):
        prev="/?p="+str(page-1)
        next="#"
    else:
        prev="/?p="+str(page-1)
        next="?p="+str(page+1)
    posts=posts[(page-1)*int(params['number_of_posts']):page*int(params['number_of_posts'])]
    return render_template('index.html',params=params,posts=posts,prev=prev,next=next,curr=page,last=last,blogger='user' in session)


@app.route("/dashboard",methods=['GET','POST'])
def dashboard():
    if('user' in session and session['user']==params['admin-user']):
        posts=Posts.query.all()
        return render_template('dashboard.html',params=params,posts=posts,blogger=True)
    if(request.method=='POST'):
        username=request.form.get('username')
        password=request.form.get('password')
        if(username==params['admin-user'] and password==params['admin-pass']):
            session['user']=username
            posts=Posts.query.all()
            return redirect("/dashboard")
    return render_template('login.html',params=params)


@app.route('/logout')
def logout():
    if('user' in session and session['user']==params['admin-user']):
        #kill the session variable
        session.pop('user')
        return redirect('/')
    return redirect('/dashboard')


@app.route("/post/<string:post_slug>",methods=['GET'])
def post_route(post_slug):
    post=Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html',params=params,post=post,blogger='user' in session)


@app.route("/edit/<string:id>",methods=["GET","POST"])
def edit(id):
    if('user' in session and session['user']==params['admin-user']):
        if(request.method=='POST'):
            #add post to database
            title=request.form.get('title')
            slug=request.form.get('slug')
            content=request.form.get('content')
            f=request.files['image']
            filename=secure_filename(f.filename)
            if(id=='0'):
                #add a new post
                f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                entry=Posts(title=title,slug=slug,author=params['admin-user'],content=content,img_url=filename)
                db.session.add(entry)
                db.session.commit()
                #redirect to dashboard
                return redirect("/dashboard")
            else:
                #edit old post
                post=Posts.query.filter_by(id=id).first()
                post.title=title
                post.slug=slug
                post.content=content
                if(post.img_url != f.filename):
                    f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                    post.img_url=filename
                db.session.commit()
                #redirect to dashboard
                return redirect("/dashboard")
        post=Posts.query.filter_by(id=id).first()
        return render_template('edit.html',id=id,params=params,post=post,blogger=True)
    #ask to login
    return redirect("/dashboard")


@app.route('/delete/<string:id>')
def delete(id):
    if('user' in session and session['user']==params['admin-user']):
        #delete post
        post=Posts.query.filter_by(id=id).first()
        db.session.delete(post)
        db.session.commit()
    return redirect("/dashboard")


@app.route("/contact",methods=['GET','POST'])
def contact():
    if(request.method=='POST'):
        #add entries to database
        name=request.form.get('name')
        email=request.form.get('email')
        msg=request.form.get('message')
        entry=Contact(name=name,email=email,message=msg)
        db.session.add(entry)
        db.session.commit()
        # mail.send_message("Clean Blog - New message from "+name,
                    # sender=email,
                    # recipients=[params['mail_username']],
                    # body=msg)
        flash("Thanks for contacting with us. We will get back to you soon.","success")

    return render_template('contact.html',params=params,blogger='user' in session)


if(__name__=="__main__"):
    app.run(debug=True)