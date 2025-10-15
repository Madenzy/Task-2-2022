from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Admins(db.Model):
    __tablename__ = 'admins'
    AdminID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100))
    Address = db.Column(db.String(200))
    DOB = db.Column(db.DateTime)
    Password = db.Column(db.String(100))

# ------------------ STUDENT ------------------
class Student(db.Model):
    __tablename__ = 'student'
    StudentID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100))
    Address = db.Column(db.String(200))
    DOB = db.Column(db.Date)
    Password = db.Column(db.String(100))
    Phone = db.Column(db.String(20))
    ParentEmail = db.Column(db.String(100), db.ForeignKey('parent.ParentEmail'))

    parent = db.relationship('Parent', back_populates='students', foreign_keys=[ParentEmail])
    enrollments = db.relationship('Enrollment', back_populates='student')
    submissions = db.relationship('Submission', back_populates='student')
    progresses = db.relationship('Progress', back_populates='student')
    xp = db.relationship('XP', back_populates='student', uselist=False)
    learning = db.relationship('Learning', back_populates='student')


# ------------------ PARENT ------------------
class Parent(db.Model):
    __tablename__ = 'parent'
    ParentEmail = db.Column(db.String(100), primary_key=True)
    Password = db.Column(db.String(100))

    students = db.relationship('Student', back_populates='parent', foreign_keys='Student.ParentEmail')


# ------------------ TUTOR ------------------
class Tutor(db.Model):
    __tablename__ = 'tutor'
    TutorID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100))
    Address = db.Column(db.String(200))
    DOB = db.Column(db.DateTime)
    Password = db.Column(db.String(100))

    # One tutor can teach many courses
    courses = db.relationship('Course', back_populates='tutor', foreign_keys='Course.TutorID')


# ------------------ COURSE ------------------
class Course(db.Model):
    __tablename__ = 'course'
    CourseID = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(100))
    Description = db.Column(db.String(255))
    TutorID = db.Column(db.Integer, db.ForeignKey('tutor.TutorID'))

    tutor = db.relationship('Tutor', back_populates='courses', foreign_keys=[TutorID])
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


# ------------------ LEARNING ------------------
class Learning(db.Model):
    __tablename__ = 'learning'
    LearnerID = db.Column(db.Integer, primary_key=True)
    StudentID = db.Column(db.Integer, db.ForeignKey('student.StudentID'))
    Completed = db.Column(db.Boolean, default=False)

    student = db.relationship('Student', back_populates='learning')


# ------------------ XP ------------------
class XP(db.Model):
    __tablename__ = 'xp'
    XPID = db.Column(db.Integer, primary_key=True)
    StudentID = db.Column(db.Integer, db.ForeignKey('student.StudentID'))
    XPLevel = db.Column(db.Integer)

    student = db.relationship('Student', back_populates='xp')
