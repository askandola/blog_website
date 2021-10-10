from app import create_app, db

app = create_app()

@app.cli.command("create_db")
def create_db() :
    db.create_all()

if __name__=="__main__" :
    app.run(debug=True)
