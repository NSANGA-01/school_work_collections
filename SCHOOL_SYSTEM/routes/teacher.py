from flask import Blueprint, app, render_template, session, redirect , request , current_app
from werkzeug.utils import secure_filename
import os
from docx import Document
from bson.objectid import ObjectId



teacher_bp = Blueprint("teacher", __name__)

ALLOWED_EXTENSIONS = {"txt", "pdf", "docx"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def read_docx(filepath):
    doc = Document(filepath)
    text = []

    for para in doc.paragraphs:
        text.append(para.text)

    return " ".join(text).strip()

def calculate_score(student_text, official_text):
    student_words = set(student_text.lower().split())
    official_words = set(official_text.lower().split())

    if not official_words:
        return 0

    matched = student_words.intersection(official_words)
    score = (len(matched) / len(official_words)) * 100

    return round(score, 2)




@teacher_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@teacher_bp.route("/teacher")
def teacher_dashboard():
    if session.get("role") != "teacher":
        return redirect("/login")
    
    db = current_app.db
    questions = list(db.questions.find({
        "teacher": session["name"]
    }))

    answers = list(db.answers.find({
        "teacher": session["name"]
    }))

    # attach official answer info to each question
    for q in questions:
        official = db.official_answers.find_one({
            "question_id": str(q["_id"])
        })
        q["official"] = official


    return render_template(
        "teacher_dashboard.html",
        questions=questions,answers = answers
    )

@teacher_bp.route("/upload_question", methods=["POST"])
def upload_question():
    if session.get("role") != "teacher":
        return redirect("/login")

    file = request.files["file"]
    class1 = request.form["class"]

    if file:
        filename = secure_filename(file.filename)
        path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        file.save(path)
        
        db = current_app.db
        db.questions.insert_one({
            "teacher": session["name"],
            "class": class1,
            "file": filename
        })

    return redirect("/teacher")

@teacher_bp.route("/upload_official_answer", methods=["POST"])
def upload_official_answer():
    if session.get("role") != "teacher":
        return redirect("/login")

    file = request.files["file"]
    question_id = request.form["question_id"]

    if file:
        filename = secure_filename(file.filename)
        path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        file.save(path)
        db = current_app.db
        db.official_answers.insert_one({
            "teacher": session["name"],
            "question_id": question_id,
            "file": filename
        })

    return redirect("/teacher")


@teacher_bp.route("/grade/<answer_id>")
def grade_answer(answer_id):
    if session.get("role") != "teacher":
        return redirect("/login")
    db = current_app.db
    answer = db.answers.find_one({"_id": ObjectId(answer_id)})
    official = db.official_answers.find_one({
        "question_id": str(answer["question_id"])
    })

    if not answer or not official:
        return "Missing files ❌"

    student_path = os.path.join(current_app.config["UPLOAD_FOLDER"], answer["file"])
    official_path = os.path.join(current_app.config["UPLOAD_FOLDER"], official["file"])

    student_text = read_docx(student_path)
    official_text = read_docx(official_path)

    score = calculate_score(student_text, official_text)

    db.answers.update_one(
        {"_id": ObjectId(answer_id)},
        {"$set": {"grade": score}}
    )

    return redirect("/teacher")


@teacher_bp.route("/delete_official/<official_id>")
def delete_official(official_id):
    if session.get("role") != "teacher":
        return redirect("/login")
    db = current_app.db
    official = db.official_answers.find_one({
        "_id": ObjectId(official_id)
    })

    if official:
        # delete file from uploads
        filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], official["file"])
        if os.path.exists(filepath):
            os.remove(filepath)

        db.official_answers.delete_one({
            "_id": ObjectId(official_id)
        })

    return redirect("/teacher")

@teacher_bp.route("/grade_report")
def grade_report():
    if session.get("role") != "teacher":
        return redirect("/login")
    db = current_app.db
    answers = db.answers.find({
        "teacher": session["name"],
        "grade": {"$ne": None}
    })

    report = []

    for a in answers:
        student = db.users.find_one({
            "name": a["student"]
        })

        report.append({
            "student_name": a["student"],
            "student_id": str(student["_id"]) if student else "N/A",
            "file": a["file"],
            "grade": a["grade"]
        })

    return render_template("grade_report.html", report=report)
@teacher_bp.route('/delete_answer/<answer_id>')
def delete_answer(answer_id):
    if session.get("role") != "teacher":
        return redirect("/login")
    db = current_app.db
    answer = db.answers.find_one({
        "_id": ObjectId(answer_id)
    })

    if answer:
        # delete file from uploads
        filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], answer["file"])
        if os.path.exists(filepath):
            os.remove(filepath)

        db.answers.delete_one({
            "_id": ObjectId(answer_id)
        })

    return redirect("/teacher")


