from flask_mail import Message
from app import mail
from app.models.students_participation import StudentParticipation

def send_confirmation_email(StudentParticipation):
    msg = Message('Confirmation Email', recipients=[StudentParticipation.email])
    msg.body = f"Hola  {StudentParticipation.name},\n\n Felicidades tu registro a sido completado de manera exitosa! \n\n este es tu codigo de participante recuerdalo  : {StudentParticipation.participation_code}"
    mail.send(msg)

def send_confirmation_emails_to_all():
    users = StudentParticipation.query.all()
    for user in users:
        send_confirmation_email(user)
