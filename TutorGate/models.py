from TutorGate import db, login_manager, bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    if student.query.get(int(user_id)):
        return student.query.get(int(user_id))
    else:
        return faculty_member.query.get(int(user_id))

#models
class admin(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable = False, unique = True)
    email = db.Column(db.String(length = 50), nullable = False, unique = True)
    password = db.Column(db.String(length = 60), nullable = False)
    FName = db.Column(db.String(length = 30), nullable = False)
    LName = db.Column(db.String(length = 30), nullable = False)
    role = db.Column(db.String(length = 30), nullable = False)

class student(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True, nullable = False, unique = True)
    email = db.Column(db.String(length = 50), nullable = False, unique = True)
    password_hash = db.Column(db.String(length = 60), nullable = False)
    Name = db.Column(db.String(length = 30), nullable = False)
    LName = db.Column(db.String(length = 30), nullable = False)
    role = db.Column(db.String(length = 30), nullable = False)
    Phone = db.Column(db.String(length = 14))
    Address = db.Column(db.String(length = 500))
    interview = db.relationship('interview', backref = 'student', lazy = True)
    application = db.relationship('application', back_populates = 'student')
    schedule = db.relationship('schedule', back_populates = 'student')

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


class faculty(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable = False, unique = True)
    facultyName = db.Column(db.String(length = 100), nullable = False)
    course = db.relationship('course', backref = 'faculty', lazy = True)
    faculty_member = db.relationship('faculty_member', backref = 'faculty', lazy = True)

class course(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable = False, unique = True)
    courseName = db.Column(db.String(length = 100), nullable = False)
    courseDescip = db.Column(db.String(length = 1024), nullable = False)
    facultyId = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    job = db.relationship('job', backref = 'course', lazy = True)

class faculty_member(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True, nullable = False, unique = True)
    email = db.Column(db.String(length = 50), nullable = False, unique = True)
    password_hash = db.Column(db.String(length = 60), nullable = False)
    Name = db.Column(db.String(length = 30), nullable = False)
    LName = db.Column(db.String(length = 30), nullable = False)
    role = db.Column(db.String(length = 30), nullable = False)
    FacultyId = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    interview = db.relationship('interview', backref = 'faculty_member', lazy = True)
    schedule = db.relationship('schedule', back_populates = 'faculty_member')

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

class job(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable = False, unique = True)
    name = db.Column(db.String(length = 100), nullable = False)
    location = db.Column(db.String(length = 30), nullable = False)
    closing_date = db.Column(db.Date, nullable = False)
    courseId = db.Column(db.Integer, db.ForeignKey('course.id'))
    application = db.relationship('application', backref = 'job', lazy = True)

class application(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable = False, unique = True)
    authorised = db.Column(db.String(length = 5), nullable = False)
    experience = db.Column(db.String(length = 5), nullable = False)
    educationlvl = db.Column(db.String(length = 13), nullable = False)
    year = db.Column(db.String(length = 5), nullable = False)
    preferred_days = db.Column(db.String(length = 50), nullable = False)
    preferred_time = db.Column(db.String(length = 10), nullable = False)
    cv = db.Column(db.LargeBinary)
    supporting_doc = db.Column(db.LargeBinary)
    applicationDate = db.Column(db.Date, nullable = False)
    applicationStatus = db.Column(db.String(length = 20), nullable = False)
    more_info = db.Column(db.String(length = 1000), nullable = False)
    student = db.relationship('student', back_populates = 'application')
    jobId = db.Column(db.Integer, db.ForeignKey('job.id'))
    studentId = db.Column(db.Integer, db.ForeignKey('student.id'))


class schedule(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable = False, unique = True)
    scheduleType = db.Column(db.String(length = 30), nullable = False)
    scheduleDate = db.Column(db.Date, nullable = False)
    scheduleStatus = db.Column(db.String(length = 30), nullable = False)
    location = db.Column(db.String(length = 30), nullable = False)
    student = db.relationship('student', back_populates = 'schedule')
    faculty_member = db.relationship('faculty_member', back_populates = 'schedule')
    studentId = db.Column(db.Integer, db.ForeignKey('student.id'))
    faculty_memberId = db.Column(db.Integer, db.ForeignKey('faculty_member.id'))

class interview(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable = False, unique = True)
    interviweDate = db.Column(db.Date, nullable = False)
    interviewStatus = db.Column(db.String(length = 30), nullable = False)
    studentId = db.Column(db.Integer, db.ForeignKey('student.id'))
    faculty_memberId = db.Column(db.Integer, db.ForeignKey('faculty_member.id'))