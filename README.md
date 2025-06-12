# AI Resume Analyzer & Job Matcher

An intelligent web application that analyzes resumes and matches them with job descriptions using Natural Language Processing (NLP) and machine learning techniques.

## Features

- **Resume Upload**: Support for PDF and TXT file formats (up to 16MB)
- **Intelligent Parsing**: Automatically extracts contact information, skills, education, and experience
- **Job Matching**: Compare resumes against multiple job descriptions with similarity scoring
- **Smart Recommendations**: AI-powered feedback for resume improvement
- **Responsive Design**: Clean, modern interface using Bootstrap with dark theme
- **Real-time Analysis**: Instant results with detailed compatibility breakdowns

## Technology Stack

- **Backend**: Flask (Python 3.11+)
- **NLP Libraries**: NLTK, spaCy, scikit-learn
- **PDF Processing**: PyPDF2
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Deployment**: Gunicorn WSGI server

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-resume-analyzer.git
cd ai-resume-analyzer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

4. Open your browser and navigate to `http://localhost:5000`

## Usage

1. **Upload Resume**: Select a PDF or TXT resume file
2. **Choose Jobs**: Select one or more job positions to match against
3. **Analyze**: Click "Analyze Resume" to get instant results
4. **Review Results**: View compatibility scores, matched skills, and improvement suggestions

## Project Structure

```
ai-resume-analyzer/
├── app.py                 # Main Flask application
├── main.py               # Application entry point
├── resume_analyzer.py    # Resume parsing and analysis
├── job_matcher.py        # Job matching algorithms
├── job_data.py          # Sample job database
├── models.py            # Data models
├── templates/           # HTML templates
│   ├── base.html
│   ├── index.html
│   └── results.html
├── static/             # CSS, JS, and assets
│   ├── css/
│   └── js/
└── uploads/            # Temporary file storage
```

## Sample Jobs

The application includes 6 pre-loaded job positions:
- Software Engineer
- Data Scientist  
- Frontend Developer
- DevOps Engineer
- Product Manager
- UX/UI Designer

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with Flask and modern NLP libraries
- Responsive design powered by Bootstrap
- AI-driven matching algorithms for accurate job compatibility scoring