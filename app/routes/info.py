from flask import Blueprint, request, jsonify
from app.models import School

info_bp = Blueprint('info', __name__)

@info_bp.route('/school', methods=['GET'])
def get_school_by_cct():
    cct = request.args.get('cct')  # Suponiendo que el parámetro de la solicitud se llama 'cct'
    school = School.query.filter_by(cct=cct).first()  # Usa el modelo School para consultar por cct

    if school:
        return jsonify({
            'id': school.id,
            'school': school.school,
            'cct': school.cct
        })
    else:
        return jsonify({'message': 'School not found'}), 404

