from flask import session, render_template
from app import app
from replit_auth import require_login, make_replit_blueprint
from flask_login import current_user

app.register_blueprint(make_replit_blueprint(), url_prefix="/auth")


@app.before_request
def make_session_permanent():
    session.permanent = True


@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('app.html', user=current_user)
    return render_template('landing.html')


@app.route('/app')
@require_login
def main_app():
    return render_template('app.html', user=current_user)
