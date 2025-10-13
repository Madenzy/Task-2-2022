from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, Email, Length, Optional, ValidationError
from datetime import date

class RegisterForm(FlaskForm):
    username = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=7, max=20)])
    dob = DateField('Date of Birth', validators=[DataRequired()], format='%Y-%m-%d')
    address = StringField('Address', validators=[DataRequired(), Length(min=5, max=200)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    role = SelectField(
        'Select Role',
        choices=[
            ('student', 'Student'),
            ('tutor', 'Tutor'),
            ('admin', 'Admin')
        ],
        validators=[DataRequired()]
    )
    parent_email = StringField('Parent Email', validators=[Optional(), Email()])
    submit = SubmitField('Register')

    def validate(self, extra_validators=None):
        # Run built-in validation first
        if not super().validate(extra_validators):
            return False

        today = date.today()
        dob = self.dob.data
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

        # Student under 18 → parent email required
        if self.role.data == 'student' and age < 18 and not self.parent_email.data:
            self.parent_email.errors.append('Parent email is required for students under 18.')
            return False

        #  Tutor under 18 → not allowed
        if self.role.data == 'tutor' and age < 18:
            self.dob.errors.append('Tutors must be at least 18 years old.')
            return False

        # Admin under 18 → not allowed
        if self.role.data == 'admin' and age < 18:
            self.dob.errors.append('Admins must be at least 18 years old.')
            return False

        return True
