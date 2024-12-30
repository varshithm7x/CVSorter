from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User
from cv_screening_model import CVScreener
import os
import json
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

load_dotenv()  # Load environment variables

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URL'] = os.getenv('DATABASE_URL')
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

# Create database tables
with app.app_context():
    db.create_all()

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
        
        # Get experience requirement from user input
        experience = request.form.get('experience', '0')
        try:
            experience = int(experience.replace('+', ''))  # Remove '+' if present
        except ValueError:
            experience = 0
            
        education = request.form.get('education', '4')
        
        # Format job requirements
        job_requirements = f"""
        Required Skills:
        {chr(10).join('- ' + skill for skill in skills)}
        
        - {experience} years of experience
        - Education Level: {education}
        """
        
        # Process uploaded files
        files = request.files.getlist('resumes')
        cvs = []
        
        for file in files:
            if file.filename:
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filepath)
                cvs.append({
                    'candidate_name': os.path.splitext(file.filename)[0],
                    'file_path': filepath
                })
        
        # Screen CVs
        results = screener.screen_cvs(cvs, job_requirements)
        
        # Format results for JSON response
        formatted_results = [
            {
                'rank': idx + 1,
                'name': name,
                'score': f"{score:.2f}",
                'file': filepath,
                'matched_skills': matched_skills
            }
            for idx, (name, score, filepath, matched_skills) in enumerate(results)
        ]
        
        return jsonify({
            'status': 'success',
            'results': formatted_results
        })
        
    except Exception as e:
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