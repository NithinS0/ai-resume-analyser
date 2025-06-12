import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix
from resume_analyzer import ResumeAnalyzer
from job_matcher import JobMatcher
from job_data import JobDatabase

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize components
resume_analyzer = ResumeAnalyzer()
job_matcher = JobMatcher()
job_db = JobDatabase()

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main page with resume upload form"""
    jobs = job_db.get_all_jobs()
    return render_template('index.html', jobs=jobs)

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    """Analyze uploaded resume and match with jobs"""
    try:
        # Check if file was uploaded
        if 'resume' not in request.files:
            flash('No file selected', 'error')
            return redirect(url_for('index'))
        
        file = request.files['resume']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('index'))
        
        if not allowed_file(file.filename):
            flash('Invalid file type. Please upload PDF or TXT files only.', 'error')
            return redirect(url_for('index'))
        
        # Get selected job IDs
        selected_jobs = request.form.getlist('jobs')
        if not selected_jobs:
            flash('Please select at least one job to match against', 'error')
            return redirect(url_for('index'))
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Analyze resume
        logging.info(f"Analyzing resume: {filename}")
        resume_data = resume_analyzer.analyze_resume(file_path)
        
        if not resume_data:
            flash('Failed to analyze resume. Please check the file format.', 'error')
            # Clean up uploaded file
            if os.path.exists(file_path):
                os.remove(file_path)
            return redirect(url_for('index'))
        
        # Get job matches
        job_matches = []
        for job_id in selected_jobs:
            job = job_db.get_job_by_id(job_id)
            if job:
                match_result = job_matcher.match_resume_to_job(resume_data, job)
                job_matches.append(match_result)
        
        # Sort matches by similarity score
        job_matches.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        # Store results in session
        session['resume_data'] = resume_data
        session['job_matches'] = job_matches
        session['filename'] = filename
        
        # Clean up uploaded file
        if os.path.exists(file_path):
            os.remove(file_path)
        
        return redirect(url_for('results'))
        
    except Exception as e:
        logging.error(f"Error analyzing resume: {str(e)}")
        flash('An error occurred while analyzing your resume. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/results')
def results():
    """Display analysis results"""
    if 'resume_data' not in session or 'job_matches' not in session:
        flash('No analysis results found. Please upload a resume first.', 'error')
        return redirect(url_for('index'))
    
    resume_data = session['resume_data']
    job_matches = session['job_matches']
    filename = session.get('filename', 'Unknown')
    
    return render_template('results.html', 
                         resume_data=resume_data, 
                         job_matches=job_matches,
                         filename=filename)

@app.route('/clear')
def clear_session():
    """Clear session data and return to home"""
    session.clear()
    return redirect(url_for('index'))

@app.errorhandler(413)
def too_large(e):
    flash('File is too large. Please upload a file smaller than 16MB.', 'error')
    return redirect(url_for('index'))

@app.errorhandler(500)
def internal_error(e):
    logging.error(f"Internal error: {str(e)}")
    flash('An internal error occurred. Please try again.', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
