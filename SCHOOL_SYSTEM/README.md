# School System - Web Application

A comprehensive web-based school management system that facilitates interaction between students and teachers through a secure authentication system, question submission, and answer grading platform.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Folder Structure](#folder-structure)
- [API Routes](#api-routes)
- [Technologies Used](#technologies-used)
- [Database](#database)
- [Contributing](#contributing)
- [License](#license)

---

## Features

### Authentication
- **User Registration**: Students can create accounts with registration number, class, email, and password
- **Secure Login**: Password hashing using bcrypt for security
- **Role-Based Access**: Different dashboards and permissions for Students and Teachers
- **Session Management**: Secure session handling for user authentication

### Student Features
- **Dashboard**: View all questions assigned to their class
- **Answer Submission**: Upload answers to questions (supports PDF, DOCX, TXT files)
- **Automatic Scoring**: Real-time score calculation based on keyword matching
- **View Official Answers**: Access correct answers once submitted by teacher
- **Grade Report**: View performance feedback from teachers

### Teacher Features
- **Question Management**: Create and manage questions for different classes
- **Answer Collection**: Receive and organize student submissions
- **Official Answer Upload**: Submit correct answers for auto-grading
- **Answer Grading**: Score student submissions based on keyword matching with official answers
- **Grade Reports**: Generate and view detailed grade reports by student or class

---

## Project Structure

```
SCHOOL_SYSTEM/
├── app.py                      # Main Flask application
├── bb.py                       # Additional configuration file
├── package.json                # Node.js dependencies (Socket.IO)
├── routes/                     # Route blueprints
│   ├── auth.py                # Authentication routes (register, login)
│   ├── student.py             # Student routes (dashboard, uploads)
│   └── teacher.py             # Teacher routes (dashboard, grading)
├── templates/                 # HTML templates
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   ├── student_dashboard.html # Student interface
│   ├── teacher_dashboard.html # Teacher interface
│   └── grade_report.html      # Grade report page
├── static/                    # Static files (CSS, JavaScript, Images)
├── uploads/                   # Uploaded answer files storage
└── myvenv/                    # Python virtual environment

```

---

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** - [Download Python](https://www.python.org/)
- **MongoDB** - [Download MongoDB Community Edition](https://www.mongodb.com/try/download/community)
- **Node.js** (optional, for Socket.IO) - [Download Node.js](https://nodejs.org/)
- **Git** - [Download Git](https://git-scm.com/)

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/SCHOOL_SYSTEM.git
cd SCHOOL_SYSTEM
```

### 2. Create Virtual Environment (Windows)

```powershell
# Create virtual environment
python -m venv myvenv

# Activate virtual environment
myvenv\Scripts\Activate.ps1
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or manually install:

```bash
pip install Flask flask-bcrypt pymongo python-docx lxml dnspython
```

### 4. Start MongoDB

Ensure MongoDB is running on your local machine:

```bash
mongod
```

MongoDB should be accessible at `mongodb://127.0.0.1:27017/`

### 5. Run the Application

```powershell
python app.py
```

The application will be available at `http://localhost:5000`

---

## Configuration

### Flask Configuration

In `app.py`, the following configurations are set:

```python
app.secret_key = "super_secret_key"  # Change this in production!
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
```

### MongoDB Configuration

Database: `school_system`

Collections:
- `users` - User accounts (students and teachers)
- `questions` - Questions created by teachers
- `answers` - Student submissions
- `official_answers` - Teacher's correct answers
- `grades` - Grade records and reports

### Modify Secret Key (IMPORTANT FOR PRODUCTION)

Update the secret key in `app.py`:

```python
app.secret_key = os.environ.get("SECRET_KEY", "your-secret-key-here")
```

---

## Usage

### For Students

1. **Register Account**
   - Click "Register" on the home page
   - Enter Name, Email, Registration Number, Class, and Password
   - Account is created with "student" role

2. **Login**
   - Navigate to `/login`
   - Enter Registration Number and Password
   - Access student dashboard

3. **Submit Answers**
   - View questions for your class on dashboard
   - Upload answer file (PDF, DOCX, or TXT)
   - System automatically scores your answer
   - View official answers once teacher submits them

### For Teachers

1. **Access as Teacher**
   - Must have an account created with "teacher" role
   - Login with credentials
   - Access teacher dashboard

2. **Create Questions**
   - Add new questions for specific classes
   - Specify question details and target class

3. **Review Submissions**
   - View all student answers submitted to your questions
   - Download and review student work

4. **Upload Official Answers**
   - Submit the correct answer to enable auto-grading
   - System uses keyword matching against student answers

5. **View Grades**
   - Access grade report
   - See score breakdown by student or class
   - Monitor class performance

---

## API Routes

### Authentication Routes (`/`)

| Method | Route | Description |
|--------|-------|-------------|
| GET, POST | `/` | Register new student |
| GET, POST | `/login` | Login for students and teachers |
| GET | `/logout` | Logout and clear session |

### Student Routes (`/student`)

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/student` | Student dashboard (questions & answers) |
| GET | `/uploads/<filename>` | Download uploaded file |
| POST | `/upload_answer` | Submit answer to a question |

### Teacher Routes (`/teacher`)

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/teacher` | Teacher dashboard |
| POST | `/create_question` | Create new question |
| POST | `/upload_official_answer` | Upload correct answer |
| GET | `/grade_report` | View grade reports |
| POST | `/grade_answer` | Score a student answer |

---

## Technologies Used

### Backend
- **Flask** - Python web framework
- **Flask-Bcrypt** - Password hashing and verification
- **PyMongo** - MongoDB driver for Python
- **Werkzeug** - WSGI utilities for file uploads and security

### Database
- **MongoDB** - NoSQL database for data storage

### Frontend
- **HTML5** - Markup
- **CSS3** - Styling
- **JavaScript** - Interactivity
- **Jinja2** - Template engine (Flask)

### Additional
- **Python-docx** - DOCX file reading
- **Socket.IO** - Real-time communication (configured but implementation pending)
- **Click** - Command-line interface utilities
- **Blinker** - Signal support

---

## Database

### Collections Schema

#### Users Collection
```javascript
{
  "_id": ObjectId,
  "name": string,
  "email": string,
  "regNo": string,
  "class": string,
  "password": string (hashed),
  "role": "student" | "teacher"
}
```

#### Questions Collection
```javascript
{
  "_id": ObjectId,
  "teacher": string,
  "class": string,
  "title": string,
  "description": string,
  "createdAt": date
}
```

#### Answers Collection
```javascript
{
  "_id": ObjectId,
  "student": string,
  "teacher": string,
  "question_id": string,
  "filename": string,
  "uploadedAt": date
}
```

#### Official Answers Collection
```javascript
{
  "_id": ObjectId,
  "question_id": string,
  "teacher": string,
  "officialAnswer": string,
  "uploadedAt": date
}
```

#### Grades Collection
```javascript
{
  "_id": ObjectId,
  "student": string,
  "question_id": string,
  "teacher": string,
  "score": number,
  "gradedAt": date
}
```

---

## File Upload

- **Upload Folder**: `uploads/` directory
- **Allowed File Types**: PDF, DOCX, TXT
- **Max File Size**: Configurable in Flask (default: 16MB)
- **File Security**: Filenames are sanitized using `secure_filename()`

---

## Error Handling

- Invalid login credentials display flash message
- File upload validation for allowed types
- Session verification for protected routes
- Database connection error handling

---

## Security Considerations

⚠️ **Warning**: This is a development version. For production:

1. Change `app.secret_key` to a strong, random value
2. Use environment variables for sensitive configuration
3. Enable CSRF protection
4. Implement rate limiting on login
5. Use HTTPS instead of HTTP
6. Add input validation and sanitization
7. Implement proper logging
8. Use MongoDB authentication credentials
9. Set strict file upload limits

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## Support

For issues or questions:
- Open an issue on GitHub
- Contact the development team

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## Author

Created as a School Management System for educational purposes.

---

**Last Updated**: February 26, 2026
