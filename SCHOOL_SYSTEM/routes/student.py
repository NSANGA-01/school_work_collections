from flask import Blueprint, render_template, session, redirect , current_app , request
from flask import send_from_directory
import os
from werkzeug.utils import secure_filename


student_bp = Blueprint("student", __name__)

@student_bp.route('/student')
def student_dashboard():
    if session.get("role") != "student":
        return redirect("/login")

    class1 = session.get("class")
    db = current_app.db
    questions = list(db.questions.find({
        "class": class1
    }))

    answers = list(db.answers.find({
        "student": session["name"]
    }))
        # attach official answer info to each question
    for q in questions:
        official = db.official_answers.find_one({
            "question_id": str(q["_id"])
        })
        q["official"] = official


    return render_template(
        "student_dashboard.html",
        questions=questions,
        school=class1,
        answers=answers
    )

@student_bp.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)


@student_bp.route("/upload_answer", methods=["POST"])
def upload_answer():
    if session.get("role") != "student":
        return redirect("/login")

    file = request.files["file"]
    question_id = request.form["question_id"]
    teacher = request.form["teacher"]

    if file:
        filename = secure_filename(file.filename)
        path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        file.save(path)
        db = current_app.db
        db.answers.insert_one({
            "student": session["name"],
            "teacher": teacher,
            "question_id": question_id,
            "file": filename,
            "grade": None
        })

    return redirect("/student")


