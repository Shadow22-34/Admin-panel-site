from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from datetime import datetime
import os  # Add this import

# At the top of the file
app = Flask(__name__,
    template_folder='templates',
    static_folder='static'
)
app.config['DEBUG'] = False  # Set to False for production
app.config['SECRET_KEY'] = 'your-secret-key'
# Change the database path to be outside the instance folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../crystal.db'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Specify the login view

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Stats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_buyers = db.Column(db.Integer, default=0)
    active_users = db.Column(db.Integer, default=0)
    total_executions = db.Column(db.Integer, default=0)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.password == request.form['password']:
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/')
@login_required
def dashboard():
    stats = Stats.query.first()
    if not stats:
        stats = Stats()
        db.session.add(stats)
        db.session.commit()
    return render_template('dashboard.html', stats=stats)

# First, add a Script model after your existing models
class Script(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    version = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    game_id = db.Column(db.String(20), nullable=False)  # Roblox game asset ID
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Update the scripts route to handle both GET and POST
@app.route('/scripts', methods=['GET', 'POST'])
@login_required
def scripts():
    if request.method == 'POST':
        name = request.form.get('script_name')
        version = request.form.get('version')
        content = request.form.get('content')
        game_id = request.form.get('game_id')
        
        if name and version and content and game_id:
            script = Script(
                name=name, 
                version=version, 
                content=content,
                game_id=game_id
            )
            db.session.add(script)
            db.session.commit()
            flash('Script added successfully!', 'success')
            return redirect(url_for('scripts'))
        
        flash('Please fill all fields', 'error')
    
    all_scripts = Script.query.all()
    return render_template('scripts.html', scripts=all_scripts)

@app.route('/stats')
@login_required
def stats():
    stats = Stats.query.first()
    if not stats:
        stats = Stats(
            total_buyers=0,
            active_users=0,
            total_executions=0
        )
        db.session.add(stats)
        db.session.commit()
    
    stats_data = {
        'total_buyers': stats.total_buyers,
        'active_users': stats.active_users,
        'total_executions': stats.total_executions
    }
    
    return jsonify(stats_data)

# Add a new route for the statistics page
@app.route('/statistics')
@login_required
def statistics():
    return render_template('statistics.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/script/<int:script_id>')
@login_required
def view_script(script_id):
    script = Script.query.get_or_404(script_id)
    return render_template('view_script.html', script=script)

@app.route('/script/delete/<int:script_id>', methods=['POST'])
@login_required
def delete_script(script_id):
    script = Script.query.get_or_404(script_id)
    db.session.delete(script)
    db.session.commit()
    flash('Script deleted successfully!', 'success')
    return redirect(url_for('scripts'))

# Initialize database
# Update the database initialization to only create if not exists
with app.app_context():
    if not os.path.exists('../../crystal.db'):
        db.create_all()
        # Create admin user if it doesn't exist
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', password='admin123', is_admin=True)
            db.session.add(admin)
            db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)