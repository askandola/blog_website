from flask import Blueprint, request, render_template, flash, redirect
import math
from . import params, db
from .models import Posts, Contact, User, Categories

blog = Blueprint('blog', __name__, static_folder='static', template_folder='templates/blog')

@blog.route("/",methods=['GET'])
def index() :
    posts=Posts.query.filter_by().order_by(Posts.date.desc()).all()
    categories = Categories.query.filter_by().all()
    categories.sort(key=lambda category:len(category.posts), reverse=True)
    categories = categories[0:10]
    featured_post = Posts.query.order_by(Posts.views.desc()).first()
    last=math.ceil(len(posts)/int(params['posts_per_page']))
    page=request.args.get('page')
    if(not str(page).isnumeric()):
        page=1
    page=int(page)
    if(page==1):
        prev="#"
        next="?page="+str(page+1)
    elif(page==last):
        prev="/?page="+str(page-1)
        next="#"
    else:
        prev="/?page="+str(page-1)
        next="?page="+str(page+1)
    posts=posts[(page-1)*int(params['posts_per_page']):page*int(params['posts_per_page'])]
    return render_template('index.html', params=params, featured_post=featured_post, categories=categories, posts=posts, prev=prev, next=next, curr=page, last=last)

@blog.route("/profile/<string:slug>",methods=['GET','POST'])
def user_route(slug) :
    user = User.query.filter_by(slug=slug).first()
    categories = Categories.query.filter_by().all()
    categories.sort(key=lambda category:len(category.posts), reverse=True)
    categories = categories[0:10]
    featured_post = Posts.query.order_by(Posts.views.desc()).first()
    page = request.args.get('page')
    last = math.ceil(len(user.posts)/int(params['posts_per_page']))
    if not str(page).isnumeric() :
        page=1
    page = int(page)
    if page==1 :
        prev = "#"
        next = f"/profile/{slug}?page="+str(page+1)
    elif page==last :
        prev = f"/profile.{slug}?page="+str(page-1)
        next = "#"
    else :
        prev = f"/profile/{slug}?page="+str(page-1)
        next = f"/profile/{slug}?page="+str(page+1)
    posts = user.posts[(page-1)*int(params['posts_per_page']): page*int(params['posts_per_page'])]
    return render_template('profile.html', params=params, featured_post=featured_post, categories=categories, user=user, posts=posts, prev=prev, curr=page, next=next, last=last)

@blog.route("/category/<string:slug>")
def category_route(slug) :
    category = Categories.query.filter_by(slug=slug).first()
    categories = Categories.query.filter_by().all()
    categories.sort(key=lambda category:len(category.posts), reverse=True)
    categories = categories[0:10]
    featured_post = Posts.query.order_by(Posts.views.desc()).first()
    page = request.args.get("page")
    if page is None :
        page = 1
    page = int(page)
    total_posts = len(category.posts)
    last=math.ceil(total_posts/int(params['posts_per_page']))
    if page==1 :
        prev = "#"
        next = f"/category/{slug}?page="+str(page+1)
    elif page==last :
        prev = f"/category/{slug}?page="+str(page-1)
        next = "#"
    else :
        prev = f"/category/{slug}?page="+str(page+1)
        next = f"/category/{slug}?page="+str(page+1)
    posts = category.posts[(page-1)*int(params["posts_per_page"]):page*int(params["posts_per_page"])]
    return render_template("category.html", params=params, featured_post=featured_post, categories=categories, curr=page, total_posts=total_posts, last=last, prev=prev, next=next, category=category, posts=posts)

@blog.route("/search")
def search_route() :
    keyword = request.args.get("q")
    if keyword!=None :
        print(keyword)
        results = Posts.query.msearch(keyword, fields={"title", "content"}).order_by(Posts.date.desc()).all()
        total_results = len(results)
        last=math.ceil(total_results/int(params['posts_per_page']))
        page = request.args.get("page")
        if not str(page).isnumeric() :
            page = 1
        page = int(page)
        if page==1 :
            prev = "#"
            next = f"/search?q={keyword}&page="+str(page+1)
        elif page==last :
            prev = f"/search?q={keyword}&page="+str(page-1)
            next = "#"
        else :
            prev = f"/search?q={keyword}&page="+str(page-1)
            next = f"/search?q={keyword}&page="+str(page+1)
        results = results[(page-1)*int(params["posts_per_page"]):page*int(params["posts_per_page"])]
    else :
        results = []
        prev="#"
        next="#"
        last = 1
        page = 1
        total_results = 0
        keyword = ''
    categories = Categories.query.filter_by().all()
    categories.sort(key=lambda category:len(category.posts), reverse=True)
    categories = categories[0:10]
    featured_post = Posts.query.order_by(Posts.views.desc()).first()
    return render_template('search.html', params=params, categories=categories, featured_post=featured_post, total_results=total_results, curr=page, last=last, next=next, prev=prev, keyword=keyword, results=results)

@blog.route("/about")
def about():
    return render_template("about.html", params=params)

@blog.route("/contact",methods=['GET','POST'])
def contact() :
    if(request.method=='POST'):
        #add entries to database
        name=request.form.get('name')
        email=request.form.get('email')
        msg=request.form.get('message')
        entry=Contact(name=name,email=email,message=msg)
        db.session.add(entry)
        db.session.commit()
        flash("Thanks for contacting with us. We will get back to you soon.","success")
        return redirect("/contact")
    return render_template('contact.html',params=params)
