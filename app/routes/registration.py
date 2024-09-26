from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import db, StudentParticipation, Campus, School
from app.utils.email_utils import send_confirmation_email

registration_bp = Blueprint('registration', __name__)

@registration_bp.route('/register', methods=['GET', 'POST'])        # Convert regular maps URL to embed format
def register_participation():
    if request.method == 'POST':
        # Obtención de datos del formulario
        cct = request.form.get('school_cct')
        form_name = request.form.get('name')
        form_email = request.form.get('email')
        form_curp = request.form.get('curp')
        form_school_name = request.form.get('school')
        form_coach_name = request.form.get('coach_name')
        form_coach_email = request.form.get('coach_email')
        form_campus_id = request.form.get('campus_id')
        form_level = request.form.get('level')

        # Establecer el puntaje inicial a cero
        score = 0

        # Validación de la existencia de la escuela
        school = School.query.filter_by(cct=cct).first()
        if not school:
            flash('La escuela no existe en la base de datos', 'danger')
            return redirect(url_for('registration.register_participation'))


        # Validación de CURP ya registrada
        existing_participant = StudentParticipation.query.filter_by(curp=form_curp).first()
        if existing_participant:
            flash('Esta CURP ya ha sido registrada en una participación.', 'danger')
            return redirect(url_for('registration.register_participation'))
        

        # Validación del límite de participantes por escuela
        limit_validation = StudentParticipation.query.filter_by(school_id=school.id).count()
        if limit_validation >= 18*3:
            flash('El límite de 18 participantes por escuela ya fue alcanzado', 'danger')
            return redirect(url_for('registration.register_participation'))



        # Generación del código de participación
        num_participants = StudentParticipation.query.filter_by(campus_id=form_campus_id).count()
        participation_code = f"{form_campus_id}_{num_participants + 1}"

        # Creación de una nueva participación
        participation = StudentParticipation(
            name=form_name,
            email=form_email,
            curp=form_curp,
            school=school,
            coach_name=form_coach_name,
            coach_email=form_coach_email,
            participation_code=participation_code,
            score=score,
            campus_id=form_campus_id,
            level=form_level
        )

        try:
            # Guardar la participación en la base de datos
            db.session.add(participation)
            db.session.commit()
            flash('Participación registrada con éxito', 'success')
            
            # Enviar correo de confirmación
            # try:
            #     send_confirmation_email(participation)
            
            # except Exception as e:
            #     print(f'Error al enviar el correo de confirmación: {e}')
            
            return redirect(url_for('home.index'))
        except Exception as e:
            # Manejo de errores en la transacción
            db.session.rollback()
            flash(f'Ocurrió un error al guardar la participación: {e}', 'danger')
            return redirect(url_for('registration.register_participation'))

    # Obtener los campus para mostrar en el formulario
    campuses = Campus.query.all()
    return render_template('registration.html', campuses=campuses)
