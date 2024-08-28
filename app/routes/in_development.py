from flask import render_template, Blueprint

development_bp = Blueprint('development', __name__)

@development_bp.route('/under-development')
def under_development():
    return render_template('under_development.html')
