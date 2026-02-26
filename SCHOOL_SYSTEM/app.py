from flask import Flask
from pymongo import MongoClient
import os 


UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)



# import blueprints
from routes.auth import auth_bp, init_db
from routes.student import student_bp
from routes.teacher import teacher_bp

app = Flask(__name__)
app.secret_key = "super_secret_key"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# MongoDB connection
client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["school_system"]
app.db = db

# ohereza db muri routes
init_db(db)

# register routes
app.register_blueprint(auth_bp)
app.register_blueprint(student_bp)
app.register_blueprint(teacher_bp)

if __name__ == "__main__":
    app.run(debug=True)
