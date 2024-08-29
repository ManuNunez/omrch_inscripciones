from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import db, StudentParticipation, Campus, School

registration_bp = Blueprint('registration', __name__)

@registration_bp.route('/register', methods=['GET', 'POST'])
def register_participation():
    if request.method == 'POST':
        cct = request.form.get('school_cct')
        form_name = request.form.get('name')
        form_email = request.form.get('email')
        form_curp = request.form.get('curp')
        form_school_name = request.form.get('school')  # Nombre de la escuela recibido desde el formulario
        form_coach_name = request.form.get('coach_name')
        form_coach_email = request.form.get('coach_email')
        form_campus_id = request.form.get('campus_id')
        form_level = request.form.get('level')  # Capturando el nivel seleccionado desde el formulario

        # Configurar score por defecto a 0
        score = 0

        # Buscar la instancia de School según el CCT
        school = School.query.filter_by(cct=cct).first()
        if not school:
            flash('La escuela no existe en la base de datos', 'danger')
            return redirect(url_for('registration.register_participation'))

        # Validar el número de participantes de la escuela
        limit_validation = StudentParticipation.query.filter_by(school_id=school.id).count()
        if limit_validation >18:
            flash('El límite de 6 participantes por escuela ya fue alcanzado', 'danger')
            return redirect(url_for('registration.register_participation'))

        # Obtener el número de participantes en la sede seleccionada para generar el código
        num_participants = StudentParticipation.query.filter_by(campus_id=form_campus_id).count()

        # Generar el código de participante en el formato <id de la sede>_<número de participante>
        participation_code = f"{form_campus_id}_{num_participants + 1}"

        # Crear instancia de StudentParticipation
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
            level=form_level  # Asignar el nivel seleccionado
        )

        try:
            db.session.add(participation)
            db.session.commit()
            print('Participación guardada con éxito')  # Mensaje de depuración
            flash('Participación registrada con éxito', 'success')
            return redirect(url_for('home.index'))
        except Exception as e:
            db.session.rollback()
            print(f'Ocurrió un error al guardar la participación: {e}')  # Imprime el error
            flash(f'Ocurrió un error al guardar la participación: {e}', 'danger')
            return redirect(url_for('registration.register_participation'))

    campuses = Campus.query.all()
    return render_template('registration.html', campuses=campuses)
