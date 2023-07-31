from flask import Blueprint,flash,render_template,request,redirect,url_for
from app.database import contact_form
from flask_mail import Message
from app.users.utils import save_picture
from .forms import LoginForm, NewPassword, RegistrationForm, RequestResetForm, UpdateForm
from app.models import User
from app import db, bcrypt,mail
from flask_login import current_user, login_required, login_user, logout_user


users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == "POST":
        if form.is_submitted():
            password = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
            if form.email.data:
                unique_email = User.query.filter_by(email=form.email.data).first()
                if unique_email:
                    flash('Email already exists', 'danger') 
                    return redirect('register')
            user = User(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email= form.email.data,
                password= password
                )
            db.session.add(user)
            db.session.commit()

            flash(f'Account created for {form.first_name.data}', 'success')
            return redirect(url_for('users.login'))
    #db = single_database(id)

    return render_template("register.html",form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('Already Logged in, Logout First', 'info')
        return redirect('/')
    form = LoginForm()
    data= request.form
    contact_form(data)
    if request.method == "POST":
        if form.is_submitted():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect('/')
            # if form.email.data == 'admin@gmail.com' and form.password.data== 'password':
            #     flash('You are logged in', 'success')
            #     return redirect('home')
            else:
                flash('Login, unsuccessful, Please confirm your email or password', 'danger')
            # return redirect('home')
    return render_template('login.html', form=form)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))

@users.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = UpdateForm()
    if form.is_submitted():
        if form.email.data:
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                flash('Email Already Exists', 'info')
                return redirect('dashboard')
        image = request.files.get('image_upload')
        if image:

            print('image',image.filename)
            #filename = secure_filename(image.filename)
            picture = save_picture(image)
            # saved_pic_path = os.path.join(users.root_path, 'static\profile_pics', image.filename) 
            # image.save(saved_pic_path)
            current_user.image_file = picture


        current_user.email = form.email.data
        current_user.first_name =  form.first_name.data
        current_user.last_name = form.last_name.data
        db.session.commit()
        flash('Profile updated', 'success')
        return redirect(url_for('users.dashboard'))
    elif request.method =="GET":
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
    return render_template('dashboard.html', form=form)

def send_email(user):
    token = user.get_reset_token()
    message = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    message.body = f''''
                    To reset your password, visit this link:
                    {url_for('users.new_password', token=token, _external=True)}
                    If you did'nt make this request, simply ignore this message.
    '''
    mail.send(message)
    

@users.route("/request_email", methods=['GET', 'POST'])
def request_email():
    # if current_user.is_authenticated:
    #     flash('Already Logged in, Logout First', 'info')
    #     return redirect('/')
    form = RequestResetForm()
    if current_user.is_authenticated:
        form.email.data = current_user.email
    if form.is_submitted():
        user = User.query.filter_by(email=form.email.data).first()
        send_email(user)
        flash(f"An email have been sent to {user}." 'info')
        return redirect('login')
    
    return render_template('reset_request.html', form=form)

@users.route("/request_password/<token>", methods=['GET', 'POST'])
def new_password(token):
    # if current_user.is_authenticated:
    #     flash('Already Logged in, Logout First', 'info')
    #     return redirect('/')
    user = User.verify_reset_token(token)
    if user:
        form = NewPassword
        if request.method == "POST":
            if form.is_submitted():
                password = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
                user.password = password
                db.session.commit()
                flash('Password Updated', 'success')
                return redirect('login')
        #return render_template('new_password.html', form=form)
    else:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.request_email')) 
    form = NewPassword()
    return render_template('reset_request.html', form=form)
