from TutorGate import app,db
from flask import render_template, request, redirect,url_for, flash
from TutorGate.models import student, application, job, course, schedule, faculty_member
from TutorGate.forms import RegisterForm, LoginForm, ApplicationForm, ProfileForm
from flask_login import login_user, current_user, logout_user
import datetime
#from datetime import datetime
from werkzeug.utils import secure_filename

#Routes
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        if current_user.role=='Student':
            return redirect(url_for('student_dashboard'))
        elif current_user.role=='Faculty Member':
            return redirect(url_for('faculty_dashboard'))
    else:
        form = RegisterForm()
        if form.validate_on_submit():
            # Form data is valid, process it
            # For example, you can access form.name.data to get the value of the name field
            name  = form.name.data
            lname = form.LName.data
            email = form.email.data
            password = form.password1.data
            password2 = form.password2.data
        
        # Create a new User instance and add it to the database
            new_user = student(Name=name, LName=lname, email=email, password=password, role='Student')
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('student_dashboard'))
        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(f'There was an error creating user: {err_msg}', category='danger')
        return render_template('register.html', form=form)


@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role=='Student':
            return redirect(url_for('student_dashboard'))
        elif current_user.role=='Faculty Member':
            return redirect(url_for('faculty_dashboard'))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            attempted_faculty_member = faculty_member.query.filter_by(email=form.email.data).first()
            if attempted_faculty_member and attempted_faculty_member.check_password_correction(attempted_password=form.password.data):
                login_user(attempted_faculty_member)
                return redirect(url_for('faculty_dashboard'))
            attempted_student = student.query.filter_by(email=form.email.data).first()
            if attempted_student and attempted_student.check_password_correction(attempted_password=form.password.data):
                login_user(attempted_student)
                return redirect(url_for('student_dashboard'))
            else:
                flash('Incorrrect username or password. Please try again', category='danger')
        return render_template("login.html",form=form)

@app.route("/application", methods=['GET','POST'])
def apply():
    job_id = request.args.get('job_id')  # Retrieve the job_id parameter from the query string
    if job_id is None:
        # Handle the case where job_id is not provided
        # For example, redirect the user to a page where they can choose a job to apply for
        return redirect(url_for('jobs'))
    
    if not current_user.is_authenticated or current_user.role != 'Student':
        return redirect(url_for('login'))
    else:
        form = ApplicationForm()
        if form.validate_on_submit():
            authorised = form.authorised.data
            experience = form.experience.data
            educationlvl = form.educationlvl.data
            year = form.year.data
            preferred_time = form.preferred_time.data
            preferred_days = form.preferred_days.data
            cv = form.cv.data
            supporting_doc = form.supporting_doc.data
            more_info = form.more_info.data
            applicationDate = datetime.datetime.now()
            applicationStatus = 'Pending'
            jobId = job_id
            studentId = current_user.id

            new_application= application(authorised=authorised,experience=experience,educationlvl=educationlvl,year=year,preferred_days=preferred_days,preferred_time=preferred_time,cv=cv.read(),supporting_doc=supporting_doc.read(),more_info=more_info,applicationDate=applicationDate,applicationStatus=applicationStatus,jobId=jobId,studentId=studentId)
            db.session.add(new_application)
            db.session.commit()
            return redirect(url_for('student_dashboard'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error appying: {err_msg}', category='danger')
    return render_template("application.html", form=form)

@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/student/dashboard')
def student_dashboard():
    if not current_user.is_authenticated or current_user.role != 'Student':
        return redirect(url_for('login'))
    jobs=job.query.all()
    appl = application.query.filter_by(studentId=current_user.id).all()
    calcappl = len(appl)

    calcjob=0
    for number in jobs:
        calcjob=calcjob+1
    return render_template('student_dashboard.html', calcjob=calcjob, calcappl=calcappl)

@app.route('/faculty/dashboard')
def faculty_dashboard():
    return render_template('faculty_dashboard.html')

@app.route('/jobs')
def jobs():
    if not current_user.is_authenticated or current_user.role != 'Student':
        return redirect(url_for('login'))
    else:
        jobs=job.query.all()
        courses=course.query.all()
        return render_template('jobs.html',jobs=jobs, courses=courses)

@app.route('/applications')
def applications():
    if not current_user.is_authenticated or current_user.role != 'Student':
        return redirect(url_for('login'))
    else:
        applications=application.query.all()
        jobs=job.query.all()
        courses=course.query.all()
        return render_template('applications.html', applications=applications, jobs=jobs, courses=courses)

@app.route('/faculty/applications')
def facApplications():
    applications=application.query.all()
    jobs=job.query.all()
    courses=course.query.all()
    return render_template('faculty_applications.html', applications=applications, jobs=jobs, courses=courses)


@app.route('/profile', methods=['GET','POST'])
def profile():
    if not current_user.is_authenticated or current_user.role != 'Student':
        return redirect(url_for('login'))
    else:
        form = ProfileForm()
        if form.validate_on_submit():

            name = form.name.data
            LName = form.LName.data
            email = form.email.data
            Phone = form.Phone.data
            Address = form.Address.data
    
            update_user = student.query.filter_by(id=current_user.id).first()
            update_user.Name = name
            update_user.LName = LName
            update_user.email = email
            update_user.Phone = Phone
            update_user.Address = Address

            db.session.commit()
            flash(f'Information succesfully updated', category='success')
    
        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(f'There was an error appying: {err_msg}', category='danger')
        return render_template('profile.html', form=form)

@app.route('/schedule')
def studentschedule():
    if not current_user.is_authenticated or current_user.role != 'Student':
        return redirect(url_for('login'))
    else:
        schedules=schedule.query.all()
        return render_template('schedule.html', schedules=schedules)

@app.route('/search')
def search():
    if not current_user.is_authenticated or current_user.role != 'Student':
        return redirect(url_for('login'))
    else:
        q = request.args.get('q')

        if q:
            jobs = job.query.join(course).filter(
                (job.name.ilike(f'%{q}%')) |
                (course.courseName.ilike(f'%{q}%'))
            ).all()
            courses = course.query.all()
        else:
            return redirect(url_for('jobs'))

        return render_template('job_search.html', jobs=jobs, courses=courses)

@app.route("/about_us")
@app.route("/contact_us")
def about_us():
    return render_template("about_us.html")

@app.route("/logout")
def logout():
    if not current_user.is_authenticated or current_user.role != 'Student':
        return redirect(url_for('login'))
    else:
        logout_user()
        return redirect(url_for('home'))

#faculty member
@app.route('/job_post', methods=['GET', 'POST'])
def job_post():
    from datetime import datetime
    if request.method == 'POST':
        name = request.form['jobTitle']
        location = request.form['location']
        coursename = request.form['course']
        closing_date_str = request.form['date']

        thiscourse = course.query.filter_by(courseName=coursename).first()
        if thiscourse:
            courseId = thiscourse.id

        # Convert the string date to a Python date object
        if closing_date_str:
            closing_date = datetime.strptime(closing_date_str, '%Y-%m-%d').date()

        new_job = job(name=name, location=location, courseId=courseId, closing_date=closing_date)
        db.session.add(new_job)
        db.session.commit()
        return redirect(url_for('faculty_dashboard'))
    return render_template('job-post.html')

if __name__ == '__main__':
    app.run(debug=True)
