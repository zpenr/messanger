from flask import Blueprint, render_template,request, redirect, abort, jsonify
from ..extensions import bcrypt, db
from flask_login import login_user, logout_user, current_user
from .user import User
main = Blueprint('main', __name__)

@main.route('/health')
def health_check():
    try:
        # Test database connectivity
        db.session.execute('SELECT 1')
        return jsonify({
            "status": "healthy", 
            "message": "Service is running",
            "database": "connected"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "unhealthy", 
            "message": "Service is running but database connection failed",
            "database": "disconnected",
            "error": str(e)
        }), 503

@main.route('/me')
def me():
    if current_user.is_authenticated:
        if current_user.name == 'me':
            return render_template('main/me.html')
        else: 
            abort(403)
    else: 
        return redirect('/')
@main.route('/makar')
def makar():
    if current_user.is_authenticated:
        if current_user.name == 'makar':
            return render_template('main/makar.html')
        else: 
            abort(403)
    else: 
        return redirect('/')

@main.route('/liza')
def liza():
    if current_user.is_authenticated:
        if current_user.name == 'liza':
            return render_template('main/liza.html')
        else: 
            abort(403)
    else: 
        return redirect('/')

@main.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == "POST":
        hashed_password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        
        user = User(name = request.form['name'], password = hashed_password )
        
        db.session.add(user)
        db.session.commit()
    return render_template('main/index.html')

@main.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == "POST":
        user = User.query.filter_by(name=request.form['name']).first()
        if user and bcrypt.check_password_hash(user.password, request.form['password']):
            login_user(user, remember = request.form.get('remember'))
            return redirect(f'/{current_user.name}')
        else:
            return render_template('main/login.html', error='Неверное имя пользователя или пароль')
    return render_template('main/login.html')

@main.route('/logout', methods = ['POST', 'GET'])
def logout():
    logout_user()
    return redirect('/login')