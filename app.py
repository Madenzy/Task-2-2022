from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin

from models import db, Student, Tutor, Parent, Account_Recovery

# ---------------------- FLASK SETUP ----------------------
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)

with app.app_context():
    db.create_all()

# ---------------------- FLASK-LOGIN SETUP ----------------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID stored in session."""
    if user_id.startswith("student-"):
        return Student.query.get(int(user_id.split("-")[1]))
    elif user_id.startswith("tutor-"):
        return Tutor.query.get(int(user_id.split("-")[1]))
    elif user_id.startswith("parent-"):
        return Parent.query.get(user_id.split("-", 1)[1])
    return None

# ---------------------- ROUTES ----------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    try:
        return render_template('about.html')
    except Exception:
        return render_template('index.html')

@app.route('/courses')
def courses():
    return render_template('course.html')

@app.route('/assignments')
def assignments():
    return render_template('index.html')

@app.route('/contact', methods=['GET', 'POST'])
@app.route('/contact-us', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        mailto = f"mailto:support@gibjohn.ac.uk?subject={subject}&body=From: {name} ({email})%0D%0A%0D%0A{message}"
        flash("Redirecting to your email client...", "success")
        return redirect(mailto)

    return render_template('contact-us.html')

@app.route('/adim-panel')
def adim_panel():
    return render_template('adim-panel.html')

@app.route('/base')
def base():
    return render_template('base.html')

@app.route('/course')
def course():
    return render_template('course.html')

@app.route('/learner')
def learner():
    return render_template('learner.html')

@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy-policy.html')

@app.route('/progress')
def progress():
    return render_template('progress.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for('index'))

# ---------------------- LOGIN ----------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = None
        user_type = None

        # Check Student
        student = Student.query.filter_by(Email=email).first()
        if student and check_password_hash(student.Password, password):
            user = student
            user_type = 'student'

        # Check Tutor
        tutor = Tutor.query.filter_by(Email=email).first()
        if tutor and check_password_hash(tutor.Password, password):
            user = tutor
            user_type = 'tutor'

        # Check Parent
        parent = Parent.query.filter_by(ParentEmail=email).first()
        if parent and check_password_hash(parent.Password, password):
            user = parent
            user_type = 'parent'

        if user:
            login_user(user)
            flash(f'Logged in successfully as {user_type.capitalize()}!', 'success')
            
            # Redirect to next page if exists, else dashboard
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)

            if user_type == 'student':
                return redirect(url_for('student_dashboard'))
            elif user_type == 'tutor':
                return redirect(url_for('teacher_dashboard'))
            else:
                return redirect(url_for('parent_dashboard'))

        flash('Invalid email or password', 'danger')

    return render_template('login.html')
# ---------------------- REGISTER ----------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email'].lower()
        phone = request.form['phone']
        dob_str = request.form['dob']
        address = request.form['address']
        password = request.form['password']
        confirm_password = request.form.get('confirm_password')
        role = request.form['role']
        parent_email = request.form.get('parent_email')

        # Validate fields
        if not all([username, email, phone, dob_str, address, password, confirm_password, role]):
            flash('All fields are required', 'danger')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('register.html')

        if len(password) < 8:
            flash('Password must be at least 8 characters', 'danger')
            return render_template('register.html')

        # DOB
        try:
            dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age < 13:
                flash('You must be at least 13 years old to register', 'danger')
                return render_template('register.html')
        except ValueError:
            flash('Invalid date format', 'danger')
            return render_template('register.html')

        # Hash password
        password_hash = generate_password_hash(password)

        # ---------------------- STUDENT ----------------------
        if role == 'student':
            if Student.query.filter_by(Email=email).first():
                flash('Email already registered as a student', 'danger')
                return render_template('register.html')

            if age < 18 and not parent_email:
                flash('Parent email required for students under 18', 'danger')
                return render_template('register.html')

            last_student = Student.query.order_by(Student.StudentID.desc()).first()
            next_student_id = 505001 if not last_student else last_student.StudentID + 1

            new_student = Student(
                StudentID=next_student_id,
                Name=username,
                Email=email,
                Address=address,
                DOB=dob,
                Password=password_hash,
                Phone=phone,
                ParentEmail=parent_email if age < 18 else None
            )

            try:
                db.session.add(new_student)
                db.session.commit()

                # Create Parent if needed
                if age < 18 and parent_email:
                    if not Parent.query.filter_by(ParentEmail=parent_email).first():
                        parent_pass = generate_password_hash(f"{new_student.StudentID}{new_student.Email}")
                        new_parent = Parent(ParentEmail=parent_email, Password=parent_pass)
                        db.session.add(new_parent)
                        db.session.commit()

                flash('Student registered successfully!', 'success')
                return redirect(url_for('login'))
            except:
                db.session.rollback()
                flash('Registration failed. Try again.', 'danger')
                return render_template('register.html')

        # ---------------------- TUTOR ----------------------
        elif role == 'tutor':
            if Tutor.query.filter_by(Email=email).first():
                flash('Email already registered as tutor', 'danger')
                return render_template('register.html')

            if age < 18:
                flash('Tutors must be at least 18', 'danger')
                return render_template('register.html')

            last_tutor = Tutor.query.order_by(Tutor.TutorID.desc()).first()
            next_tutor_id = 1 if not last_tutor else last_tutor.TutorID + 1

            new_tutor = Tutor(
                TutorID=next_tutor_id,
                Name=username,
                Email=email,
                Address=address,
                DOB=dob,
                Password=password_hash
            )

            try:
                db.session.add(new_tutor)
                db.session.commit()
                flash('Tutor registered successfully!', 'success')
                return redirect(url_for('login'))
            except:
                db.session.rollback()
                flash('Registration failed. Try again.', 'danger')
                return render_template('register.html')

        # ---------------------- ADMIN ----------------------
        elif role == 'admin':
            flash('Admin registration is not allowed', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html')

# ---------------------- DASHBOARDS ----------------------
@app.route('/student-dashboard')
@login_required
def student_dashboard():
    return render_template('student-dashboard.html')

@app.route('/teacher-dashboard')
@login_required
def teacher_dashboard():
    return render_template('teacher-dashboard.html', tutor=current_user)

@app.route('/parent-dashboard')
@login_required
def parent_dashboard():
    return render_template('parent-dashboard.html')

# ---------------------- SECURITY QUESTIONS ----------------------
@app.route('/security_questions', methods=['GET', 'POST'])
@login_required
def security_questions():
    question_list = [
        "What was the name of your first pet?",
        "What is your mother’s maiden name?",
        "What was the model of your first car?",
        "What city were you born in?",
        "What is your favorite teacher’s name?"
    ]

    if request.method == 'POST':
        selected_questions = []
        answers = []

        for i in range(1, 4):
            q_text = request.form.get(f'question{i}')
            ans = request.form.get(f'answer{i}')
            if q_text and ans:
                selected_questions.append(q_text)
                answers.append(ans)

        if len(selected_questions) != 3:
            flash("Answer exactly 3 questions.", "danger")
            return redirect(url_for('security_questions'))

        for q_text, ans in zip(selected_questions, answers):
            entry = Account_Recovery(
                UserEmail=current_user.Email if hasattr(current_user, 'Email') else current_user.ParentEmail,
                QuestionText=q_text,
                AnswerHash=generate_password_hash(ans)
            )
            db.session.add(entry)

        db.session.commit()
        flash("Security questions saved!", "success")
        return redirect(url_for('student_dashboard'))

    return render_template('security_questions.html', question_list=question_list)

# ---------------------- MAIN ----------------------
if __name__ == '__main__':
    app.run(debug=True)
