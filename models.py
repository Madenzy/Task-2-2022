from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, date

db = SQLAlchemy()

# ------------------ ACCOUNT RECOVERY ------------------
class Account_Recovery(db.Model):
    __tablename__ = 'account_recovery'
    RecoveryID = db.Column(db.Integer, primary_key=True)
    UserEmail = db.Column(db.String(100), nullable=False)
    QuestionText = db.Column(db.String(255), nullable=False)
    AnswerHash = db.Column(db.String(255), nullable=False)

# ------------------ STUDENT ------------------
class Student(UserMixin, db.Model):
    __tablename__ = 'student'
    StudentID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100))
    Email = db.Column(db.String(100), unique=True, nullable=False)
    Address = db.Column(db.String(200))
    DOB = db.Column(db.Date)
    Password = db.Column(db.String(255))
    Phone = db.Column(db.String(20))
    ParentEmail = db.Column(db.String(100), db.ForeignKey('parent.ParentEmail'))

    parent = db.relationship('Parent', back_populates='students')
    enrollments = db.relationship('Enrollment', back_populates='student')
    submissions = db.relationship('Submission', back_populates='student')
    progresses = db.relationship('Progress', back_populates='student')
    xp = db.relationship('XP', back_populates='student', uselist=False)

    # Flask-Login required
    def get_id(self):
        return f"student-{self.StudentID}"

# ------------------ PARENT ------------------
class Parent(UserMixin, db.Model):
    __tablename__ = 'parent'
    ParentEmail = db.Column(db.String(100), primary_key=True)
    Password = db.Column(db.String(255))

    students = db.relationship('Student', back_populates='parent')

    def get_id(self):
        return f"parent-{self.ParentEmail}"

# ------------------ TUTOR ------------------
class Tutor(UserMixin, db.Model):
    __tablename__ = 'tutor'
    TutorID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100))
    Email = db.Column(db.String(100), unique=True, nullable=False)
    Address = db.Column(db.String(200))
    DOB = db.Column(db.Date)
    Password = db.Column(db.String(255))

    courses = db.relationship('Course', back_populates='tutor')

    def get_id(self):
        return f"tutor-{self.TutorID}"

# ------------------ COURSE ------------------
class Course(db.Model):
    __tablename__ = 'course'
    CourseID = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(100))
    Description = db.Column(db.String(255))
    TutorID = db.Column(db.Integer, db.ForeignKey('tutor.TutorID'))

    tutor = db.relationship('Tutor', back_populates='courses')
    enrollments = db.relationship('Enrollment', back_populates='course')
    assignments = db.relationship('Assignment', back_populates='course')

# ------------------ ENROLLMENT ------------------
class Enrollment(db.Model):
    __tablename__ = 'enrollment'
    EnrollmentID = db.Column(db.Integer, primary_key=True)
    StudentID = db.Column(db.Integer, db.ForeignKey('student.StudentID'))
    CourseID = db.Column(db.Integer, db.ForeignKey('course.CourseID'))
    DateEnrolled = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship('Student', back_populates='enrollments')
    course = db.relationship('Course', back_populates='enrollments')

# ------------------ ASSIGNMENT ------------------
class Assignment(db.Model):
    __tablename__ = 'assignment'
    AssignmentID = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(100))
    MaxScore = db.Column(db.Integer)
    CourseID = db.Column(db.Integer, db.ForeignKey('course.CourseID'))
    DateDue = db.Column(db.DateTime)

    course = db.relationship('Course', back_populates='assignments')
    submissions = db.relationship('Submission', back_populates='assignment')
    progresses = db.relationship('Progress', back_populates='assignment')

# ------------------ SUBMISSION ------------------
class Submission(db.Model):
    __tablename__ = 'submission'
    SubmissionID = db.Column(db.Integer, primary_key=True)
    StudentID = db.Column(db.Integer, db.ForeignKey('student.StudentID'))
    AssignmentID = db.Column(db.Integer, db.ForeignKey('assignment.AssignmentID'))
    SubmittedAt = db.Column(db.DateTime, default=datetime.utcnow)
    FileName = db.Column(db.String(255))
    FileType = db.Column(db.String(50))
    FileDataBlob = db.Column(db.LargeBinary)
    Status = db.Column(db.Boolean, default=False)

    student = db.relationship('Student', back_populates='submissions')
    assignment = db.relationship('Assignment', back_populates='submissions')
    progresses = db.relationship('Progress', back_populates='submission')

# ------------------ PROGRESS ------------------
class Progress(db.Model):
    __tablename__ = 'progress'
    ProgressID = db.Column(db.Integer, primary_key=True)
    StudentID = db.Column(db.Integer, db.ForeignKey('student.StudentID'))
    AssignmentID = db.Column(db.Integer, db.ForeignKey('assignment.AssignmentID'))
    SubmissionID = db.Column(db.Integer, db.ForeignKey('submission.SubmissionID'))
    Score = db.Column(db.Integer)
    GradedBy = db.Column(db.String(100))
    GradedAt = db.Column(db.DateTime)
    Feedback = db.Column(db.String(255))

    student = db.relationship('Student', back_populates='progresses')
    assignment = db.relationship('Assignment', back_populates='progresses')
    submission = db.relationship('Submission', back_populates='progresses')


# ------------------ XP ------------------
class XP(db.Model):
    __tablename__ = 'xp'
    XPID = db.Column(db.Integer, primary_key=True)
    StudentID = db.Column(db.Integer, db.ForeignKey('student.StudentID'))
    XPLevel = db.Column(db.Integer)

    student = db.relationship('Student', back_populates='xp')