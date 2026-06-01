from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, SelectField
from wtforms.validators import InputRequired, Email, EqualTo, Length, ValidationError
from TutorGate.models import student


class RegisterForm(FlaskForm):
    def validate_email(self,email_to_check):
        student_exists=student.query.filter_by(email=email_to_check.data).first()
        if student_exists:
            raise ValidationError('Email already exists! Please try logging in')

    name = StringField('First Name', validators=[InputRequired(),Length(min=2,max=30)])
    LName = StringField('Last Name', validators=[InputRequired(),Length(min=2,max=30)])
    email = StringField('E-Mail Address', validators=[InputRequired(), Email()])
    password1 = PasswordField('Password', validators=[InputRequired(), Length(min=6)])
    password2 = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password1', message='Passwords must match')])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    email = StringField('E-Mail Address', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Submit')

class ApplicationForm(FlaskForm):
    authorised = SelectField('Authorised to work in SA?',choices=[('Yes'),('No')],validators=[InputRequired()])
    experience = SelectField('Have experience?',choices=[('Yes'),('No')],validators=[InputRequired()])
    educationlvl = SelectField('Education Level',choices=[('Matric'),('Certificate'),('Diploma'),('Bachelors'),('Honours'),('Masters'),('Doctorate')],validators=[InputRequired()])
    year = SelectField('Year of study',choices=[('1st'),('2nd'),('3rd'),('4th'),('5th'),('6th+')],validators=[InputRequired()])
    preferred_days = SelectField('Preferred working days', choices=[('Monday'),('Tuesday'),('Wednesday'),('Thursday'),('Friday')],validators=[InputRequired()])
    preferred_time = SelectField('Preferred Time',choices=[('Morning'),('Afternoon'),('Evening')],validators=[InputRequired()])
    more_info = StringField('Best candidate for this job',validators=[InputRequired(),Length(max=1000)])
    cv = FileField('Curriculum Vitae', validators=[InputRequired()])
    supporting_doc = FileField('Supporting Document', validators=[InputRequired()])
    submit = SubmitField('Submit')

class ProfileForm(FlaskForm):
    name = StringField('First Name', validators=[InputRequired(),Length(min=2,max=30)])
    LName = StringField('Last Name', validators=[InputRequired(),Length(min=2,max=30)])
    email = StringField('E-Mail Address', validators=[InputRequired(), Email()])
    Phone = StringField('Phone Number',validators=[Length(min=10,max=14)])
    Address = StringField('Address',validators=[Length(max=500)])
    submit = SubmitField('Submit')