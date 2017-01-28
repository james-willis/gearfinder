from app import app
app.run(port=os.environ.get("PORT"), debug=True)
