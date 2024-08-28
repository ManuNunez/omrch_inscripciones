from app import db

class StudentParticipation(db.Model):
    __tablename__ = 'students_participation'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    curp = db.Column(db.String(18), nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False)
    coach_name = db.Column(db.String(100), nullable=False)
    coach_email = db.Column(db.String(100), nullable=False)
    participation_code = db.Column(db.String(20), unique=True, nullable=False)
    score = db.Column(db.Integer, default=0, nullable=False)
    campus_id = db.Column(db.Integer, db.ForeignKey('campuses.id'), nullable=False)
    level = db.Column(db.String(50), nullable=False) 

    # Relación con Campus
    campus = db.relationship('Campus', backref=db.backref('participants', lazy=True))
    
    # Relación con School
    school = db.relationship('School', back_populates='student_participations')

    def __repr__(self):
        return f'<StudentParticipation {self.participation_code}>'
