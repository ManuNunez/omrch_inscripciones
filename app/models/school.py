from app import db

class School(db.Model):
    __tablename__ = 'schools'

    id = db.Column(db.Integer, primary_key=True)
    school = db.Column(db.String(100), nullable=False, unique=True)  # Nombre de la escuela
    cct = db.Column(db.String(20), nullable=False)  # Código CCT (si aplica)

    # Relación con StudentParticipation
    student_participations = db.relationship('StudentParticipation', back_populates='school')

    def __repr__(self):
        return f'<School {self.school}>'
