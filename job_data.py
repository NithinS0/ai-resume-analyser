import logging

class JobDatabase:
    """Simple in-memory job database for demonstration purposes"""
    
    def __init__(self):
        """Initialize the job database with sample jobs"""
        self.jobs = [
            {
                'id': '1',
                'title': 'Software Engineer',
                'company': 'Tech Corp',
                'location': 'San Francisco, CA',
                'salary': '$120,000 - $160,000',
                'description': 'We are looking for a skilled Software Engineer to join our team. You will be responsible for developing and maintaining web applications using modern technologies.',
                'requirements': 'Bachelor\'s degree in Computer Science or related field. 3+ years of experience in software development. Proficiency in Python, JavaScript, React, and SQL. Experience with cloud platforms like AWS or Azure. Strong problem-solving skills and ability to work in a team environment.'
            },
            {
                'id': '2',
                'title': 'Data Scientist',
                'company': 'DataTech Solutions',
                'location': 'New York, NY',
                'salary': '$110,000 - $150,000',
                'description': 'Join our data science team to analyze large datasets and build predictive models. You will work with stakeholders to understand business requirements and translate them into data-driven solutions.',
                'requirements': 'Master\'s degree in Data Science, Statistics, or related field. 2+ years of experience in data analysis and machine learning. Proficiency in Python, R, SQL, and machine learning libraries like scikit-learn, pandas, numpy. Experience with data visualization tools. Strong analytical and communication skills.'
            },
            {
                'id': '3',
                'title': 'Frontend Developer',
                'company': 'Creative Agency',
                'location': 'Los Angeles, CA',
                'salary': '$90,000 - $120,000',
                'description': 'We are seeking a talented Frontend Developer to create engaging user interfaces and experiences. You will work closely with designers and backend developers to bring mockups to life.',
                'requirements': 'Bachelor\'s degree or equivalent experience. 2+ years of frontend development experience. Expert knowledge of HTML, CSS, JavaScript, and React or Vue.js. Experience with responsive design and cross-browser compatibility. Familiarity with version control systems like Git. Strong attention to detail and design sense.'
            },
            {
                'id': '4',
                'title': 'DevOps Engineer',
                'company': 'CloudFirst Inc',
                'location': 'Seattle, WA',
                'salary': '$130,000 - $170,000',
                'description': 'We are looking for a DevOps Engineer to help streamline our development and deployment processes. You will be responsible for maintaining our cloud infrastructure and implementing CI/CD pipelines.',
                'requirements': 'Bachelor\'s degree in Computer Science or related field. 3+ years of DevOps experience. Proficiency with AWS, Docker, Kubernetes, and Terraform. Experience with CI/CD tools like Jenkins or GitLab. Strong knowledge of Linux systems and shell scripting. Understanding of networking and security best practices.'
            },
            {
                'id': '5',
                'title': 'Product Manager',
                'company': 'Innovation Labs',
                'location': 'Austin, TX',
                'salary': '$100,000 - $140,000',
                'description': 'We need a Product Manager to drive the development of our consumer-facing products. You will work with cross-functional teams to define product strategy and roadmap.',
                'requirements': 'Bachelor\'s degree in Business, Engineering, or related field. 3+ years of product management experience. Strong analytical and problem-solving skills. Experience with agile development methodologies. Excellent communication and leadership abilities. Understanding of user experience design principles.'
            },
            {
                'id': '6',
                'title': 'UX/UI Designer',
                'company': 'Design Studio',
                'location': 'Portland, OR',
                'salary': '$80,000 - $110,000',
                'description': 'Join our design team to create intuitive and beautiful user experiences. You will be responsible for the entire design process from user research to final implementation.',
                'requirements': 'Bachelor\'s degree in Design, HCI, or related field. 2+ years of UX/UI design experience. Proficiency in design tools like Figma, Sketch, or Adobe Creative Suite. Strong portfolio demonstrating user-centered design process. Experience with user research and usability testing. Understanding of frontend technologies and design systems.'
            }
        ]
        
        logging.info(f"Job database initialized with {len(self.jobs)} jobs")
    
    def get_all_jobs(self):
        """Get all jobs from the database"""
        return self.jobs
    
    def get_job_by_id(self, job_id):
        """Get a specific job by ID"""
        for job in self.jobs:
            if job['id'] == job_id:
                return job
        return None
    
    def get_jobs_by_title(self, title):
        """Get jobs by title (case-insensitive search)"""
        title_lower = title.lower()
        return [job for job in self.jobs if title_lower in job['title'].lower()]
    
    def get_jobs_by_company(self, company):
        """Get jobs by company name"""
        company_lower = company.lower()
        return [job for job in self.jobs if company_lower in job['company'].lower()]
    
    def add_job(self, job_data):
        """Add a new job to the database"""
        # Generate new ID
        max_id = max([int(job['id']) for job in self.jobs]) if self.jobs else 0
        job_data['id'] = str(max_id + 1)
        
        self.jobs.append(job_data)
        logging.info(f"Added new job: {job_data['title']} at {job_data['company']}")
        return job_data['id']
    
    def update_job(self, job_id, updated_data):
        """Update an existing job"""
        for i, job in enumerate(self.jobs):
            if job['id'] == job_id:
                self.jobs[i].update(updated_data)
                logging.info(f"Updated job: {job_id}")
                return True
        return False
    
    def delete_job(self, job_id):
        """Delete a job from the database"""
        for i, job in enumerate(self.jobs):
            if job['id'] == job_id:
                deleted_job = self.jobs.pop(i)
                logging.info(f"Deleted job: {deleted_job['title']}")
                return True
        return False
    
    def search_jobs(self, query):
        """Search jobs by query in title, company, or description"""
        query_lower = query.lower()
        results = []
        
        for job in self.jobs:
            if (query_lower in job['title'].lower() or 
                query_lower in job['company'].lower() or 
                query_lower in job['description'].lower() or
                query_lower in job['requirements'].lower()):
                results.append(job)
        
        return results
