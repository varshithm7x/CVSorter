from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User
from cv_screening_model import CVScreener
import os
import json
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy_utils import database_exists, create_database

load_dotenv()  # Load environment variables

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')

# Make sure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

screener = CVScreener()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Initialize database
def init_database():
    with app.app_context():
        if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
            create_database(app.config['SQLALCHEMY_DATABASE_URI'])
        db.create_all()
        print("Database initialized!")

# Create database tables
init_database()

@app.route('/')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        company = request.form.get('company')

        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('signup'))

        user = User(email=email, name=name, company=company)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect(url_for('home'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('home'))
        
        flash('Invalid email or password')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'pdf', 'docx', 'txt'}

@app.route('/screen', methods=['POST'])
@login_required
def screen_cvs():
    try:
        # Get selected skills
        skills = json.loads(request.form.get('skills', '[]'))
        print(f"Received skills: {skills}")  # Debug print
        
        # Get experience requirement
        experience = request.form.get('experience', '0')
        try:
            experience = int(experience.replace('+', ''))
        except ValueError:
            experience = 0
        
        # Format job requirements
        job_requirements = f"""
        Required Skills:
        {chr(10).join('- ' + skill for skill in skills)}
        
        - {experience} years of experience
        """
        
        # Process uploaded files
        files = request.files.getlist('resumes')
        print(f"Received {len(files)} files")  # Debug print
        
        cvs = []
        for file in files:
            if file and file.filename:
                # Secure the filename
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                cvs.append({
                    'candidate_name': os.path.splitext(filename)[0],
                    'file_path': filepath
                })
        
        # Screen CVs
        results = screener.screen_cvs(cvs, job_requirements)
        print(f"Screening results: {len(results)}")  # Debug print
        
        # Format results for JSON response
        formatted_results = []
        for idx, result in enumerate(results):
            formatted_results.append({
                'rank': idx + 1,
                'name': result['candidate_name'],
                'score': f"{result['score']:.2f}",
                'file': result['file_path'],
                'matched_skills': result['matched_skills']
            })
        
        return jsonify({
            'status': 'success',
            'results': formatted_results
        })
        
    except Exception as e:
        print(f"Error in screen_cvs route: {str(e)}")  # Debug print
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

@app.route('/register', methods=['POST'])
def register():
    email = request.form.get('email')
    password = request.form.get('password')
    
    # Hash password before storing
    hashed_password = generate_password_hash(password)
    
    user = User(email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 