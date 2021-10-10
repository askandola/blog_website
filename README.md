
# Blog Website

Blog website is a blogging website built using flask and bootstrap. It allows users to Register / Sign-In and create their posts, comment on others posts, reply to the comments.

Deployed on Heroku at https://blog-askandola.herokuapp.com/

## Tech Stack

**Client:** HTML, CSS, JavaScript, Bootstrap

**Server:** Python, flask

**Database:** SQLite (using flask-sqlAlchemy)

## Run Locally

Clone the project

```bash
  git clone https://github.com/askandola/blog_website.git
```

Go to the project directory

```bash
  cd blog_website
```

If you want use virtual environment

```bash
  virtualenv env
```

```bash
  env/Scripts/activate
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  python ./run.py
```
