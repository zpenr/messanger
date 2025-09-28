from flask import Blueprint, render_template,request, redirect, abort, jsonify
from ..extensions import bcrypt, db
from flask_login import login_user, logout_user, current_user
from ..models.user import User
main = Blueprint('main', __name__)

@main.route('/health')
def health_check():
    return jsonify({"status": "healthy", "message": "Service is running"}), 200

@main.route('/test')
def test():
    return "Test page works! Server is running correctly.", 200

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
    # Health check for Railway
    if request.headers.get('User-Agent') == 'Railway-Health-Check':
        return jsonify({"status": "healthy", "message": "Service is running"}), 200
    
    if request.method == "POST":
        try:
            hashed_password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
            
            user = User(name = request.form['name'], password = hashed_password )
            
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            print(f"Database error: {e}")
            return "Error creating user. Please try again.", 500
    
    try:
        return render_template('main/index.html')
    except Exception as e:
        print(f"Template error: {e}")
        # Fallback to simple HTML if template fails
        return """
        <html>
        <head><title>ZPENR Messenger</title></head>
        <body>
            <h1>ZPENR Messenger</h1>
            <p>Welcome to the messenger!</p>
            <form method="POST">
                <input type="text" name="name" placeholder="Username" required><br><br>
                <input type="password" name="password" placeholder="Password" required><br><br>
                <button type="submit">Register</button>
            </form>
            <p><a href="/login">Login</a></p>
        </body>
        </html>
        """, 200

@main.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == "POST":
        try:
            user = User.query.filter_by(name=request.form['name']).first()
            if user and bcrypt.check_password_hash(user.password, request.form['password']):
                login_user(user, remember = request.form.get('remember'))
                return redirect(f'/{current_user.name}')
            else:
                return render_template('main/login.html', error='Неверное имя пользователя или пароль')
        except Exception as e:
            print(f"Login error: {e}")
            return "Error during login. Please try again.", 500
    
    try:
        return render_template('main/login.html')
    except Exception as e:
        print(f"Template error: {e}")
        # Fallback to simple HTML if template fails
        return """
        <html>
        <head><title>Login - ZPENR Messenger</title></head>
        <body>
            <h1>Login</h1>
            <form method="POST">
                <input type="text" name="name" placeholder="Username" required><br><br>
                <input type="password" name="password" placeholder="Password" required><br><br>
                <button type="submit">Login</button>
            </form>
            <p><a href="/">Register</a></p>
        </body>
        </html>
        """, 200

@main.route('/logout', methods = ['POST', 'GET'])
def logout():
    logout_user()
    return redirect('/login')