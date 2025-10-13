from flask import Flask, jsonify, request, url_for, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import db
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Student, Tutor, Parent
from flask_login import login_user




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)
with app.app_context():
    db.create_all()



@app.route('/')
def index():
    return render_template('index.html')
    

# Friendly aliases and placeholder routes used by templates
@app.route('/home')
def home():
    # Alias to index
    return render_template('index.html')


@app.route('/about')
def about():
    # About page placeholder - if you add about.html, change this to render it
    try:
        return render_template('about.html')
    except Exception:
        return render_template('index.html')


@app.route('/courses')
def courses():
    # Template is named course.html in the project
    return render_template('course.html')


@app.route('/logout')
def logout():
    # Simple sign-out placeholder: redirect to home/index
    return redirect(url_for('index'))


@app.route('/assignments')
def assignments():
    # Placeholder route; create assignments.html if you want a dedicated page
    return render_template('index.html')


# Contact can be reached by both /contact and /contact-us (accepts GET and POST)
@app.route('/contact', methods=['GET', 'POST'])
@app.route('/contact-us', methods=['GET', 'POST'])
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        # Build the mailto link dynamically
        mailto = f"mailto:support@gibjohn.ac.uk?subject={subject}&body=From: {name} ({email})%0D%0A%0D%0A{message}"

        flash("Redirecting to your email client...", "success")
        return redirect(mailto)  # This opens the user's default email app

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


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy-policy.html')


@app.route('/progress')
def progress():
    return render_template('progress.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email'].lower()
        phone = request.form['phone']
        dob_str = request.form['dob']
        address = request.form['address']
        password = request.form['password']
        role = request.form['role']
        parent_email = request.form.get('parent_email')

        # --- FIXED: correct date format for HTML input ---
        dob = datetime.strptime(dob_str, '%Y-%m-%d').date()

        # --- calculate age ---
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

        # --- role-based validation ---
        if role == 'student' and age < 18 and not parent_email:
            flash('Parent email is required for students under 18.', 'danger')
            # Re-render page but show the parent email field
            return render_template('register.html', 
            error='Parent email is required for students under 18.',show_parent_email=True)

        if role == 'tutor' and age < 18:
            flash('Tutors must be at least 18 years old.', 'danger')
            return render_template('register.html', error='Tutors must be at least 18 years old.')

        if role == 'admin' and age < 18:
            flash('Admins must be at least 18 years old.', 'danger')
            return render_template('register.html', error='Admins must be at least 18 years old.')
        # --- check for existing email ---
        if role == 'student' and Student.query.filter_by(ParentEmail=email).first():
            flash('Email already registered as a student.', 'danger')
            return render_template('register.html', error='Email already registered as a student.')

        if role == 'tutor' and Tutor.query.filter_by(Name=username).first():
            flash('Email already registered as a tutor.', 'danger')
            return render_template('register.html', error='Email already registered as a tutor.')

        if role == 'admin' and Admins.query.filter_by(Name=username).first():
            flash('Email already registered as an admin.', 'danger')
            return render_template('register.html', error='Email already registered as an admin.')

        if role == 'student':
            #add parent to parent table if under 18 and not exists
            if age < 18 and parent_email:
                if not Parent.query.filter_by(ParentEmail=parent_email).first():
                    new_parent = Parent(
                    ParentEmail=parent_email,
                    Password='defaultpassword')
                    db.session.add(new_parent)
                    db.session.commit()
            else:
                parent_email = None

            new_student = Student(
                Name=username,
                Address=address,
                DOB=dob,
                Password=password,
                Phone=phone,
                ParentEmail=parent_email if age < 18 else None
            )
            db.session.add(new_student)
            db.session.commit()
            flash('Student registered successfully!', 'success')
            return redirect(url_for('login'))

        elif role == 'tutor':
            new_tutor = Tutor(
                Name=username,
                Address=address,
                DOB=dob,
                Password=password
            )
            db.session.add(new_tutor)
            db.session.commit()
            flash('Tutor registered successfully!', 'success')
            return redirect(url_for('login'))

        elif role == 'admin':
            flash('Admin registered successfully!', 'success')
            return redirect(url_for('login'))

    # Default page (no parent email shown yet)
    return render_template('register.html', show_parent_email=False)


@app.route('/student-dashboard')
def student_dashboard():
    return render_template('student-dashboard.html')


@app.route('/teacher-dashboard')
def teacher_dashboard():
    return render_template('teacher-dashboard.html')


if __name__ == '__main__':
    # Start the dev server when run directly. Use debug=True while developing.
    app.run(debug=True)

