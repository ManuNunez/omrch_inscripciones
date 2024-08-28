from app import db

# Importar todas las clases primero
from .campus import Campus
from .school import School
from .students_participation import StudentParticipation

__all__ = ['db', 'Campus', 'School', 'StudentParticipation']
