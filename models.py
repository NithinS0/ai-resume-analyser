# This file is kept for future database integration
# Currently using in-memory storage for simplicity

class ResumeModel:
    """Model for storing resume data"""
    def __init__(self, name=None, email=None, phone=None, skills=None, 
                 education=None, experience=None, raw_text=None):
        self.name = name
        self.email = email
        self.phone = phone
        self.skills = skills or []
        self.education = education or []
        self.experience = experience or []
        self.raw_text = raw_text

class JobModel:
    """Model for storing job data"""
    def __init__(self, id, title, company, description, requirements, 
                 location=None, salary=None):
        self.id = id
        self.title = title
        self.company = company
        self.description = description
        self.requirements = requirements
        self.location = location
        self.salary = salary
