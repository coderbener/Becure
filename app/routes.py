from flask import Blueprint, render_template,redirect,url_for,flash,request
from app import db, bcrypt
from app.models import User, Task
from flask_login import login_user, current_user, logout_user, login_required

main= Blueprint('main', __name__)

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method=='POST':
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        role=request.form['role']

        hashed_pw=bcrypt.generate_password_hash(password).decode('utf-8')
        new_user=User(username=username, email=email, password=hashed_pw, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! you can now login ', 'success')
        return redirect(url_for('main.login'))
    return render_template('signup.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        user=User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password,password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html')
  
# Logout
@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))

# Dashboard
@main.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        tasks = Task.query.all()
    else:
        tasks = Task.query.filter_by(owner_id=current_user.id).all()
    return render_template('dashboard.html', tasks=tasks)

# Add Task
@main.route('/add-task', methods=['POST'])
@login_required
def add_task():
    title = request.form['title']
    description = request.form['description']
    new_task = Task(title=title, description=description, owner_id=current_user.id)
    db.session.add(new_task)
    db.session.commit()
    flash('Task added successfully!', 'success')
    return redirect(url_for('main.dashboard'))

# Delete Task
@main.route('/delete-task/<int:task_id>')
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if current_user.role == 'admin' or task.owner_id == current_user.id:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted!', 'info')
    else:
        flash('Not authorized to delete this task.', 'danger')
    return redirect(url_for('main.dashboard'))