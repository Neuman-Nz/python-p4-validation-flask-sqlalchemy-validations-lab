from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Name cannot be empty.")
        if Author.query.filter_by(name=name).first():
            raise ValueError("Name must be unique.")
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if phone_number and (len(phone_number) != 10 or not phone_number.isdigit()):
            raise ValueError("Phone number must be exactly ten digits.")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'
class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('title')
    def validate_title(self, key, title):
        print(len(title))  
        if not title:
            raise ValueError("Title cannot be empty.")
        if len(title) < 10 or len(title) > 255:
            raise ValueError("Title must be between 10 and 255 characters.")
        if 'clickbait' in title.lower():
            raise ValueError("Title cannot contain 'clickbait'.")
        if len(title) >= 260:
            raise ValueError("Title cannot exceed 260 characters.")
        return title

    @validates('category')
    def validate_category(self, key, category):
        valid_categories = ['Fiction', 'Non-Fiction']  
        if category not in valid_categories:
            raise ValueError("Invalid category.")
        return category

    @validates('content')
    def validate_content(self, key, content):
        if content and len(content) < 250:
            raise ValueError("Content must be at least 250 characters long.")
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        if summary and len(summary) > 250:
            raise ValueError("Summary must be at most 250 characters long.")
        return summary

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'