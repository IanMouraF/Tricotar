import uuid
from flask import session, render_template, request, jsonify
from app import app, db
from replit_auth import require_login, make_replit_blueprint
from flask_login import current_user
from models import Fio

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


# ---- API: Fios ----

@app.route('/api/fios', methods=['GET'])
@require_login
def get_fios():
    fios = Fio.query.filter_by(user_id=current_user.id).order_by(Fio.created_at.desc()).all()
    return jsonify([{
        'id': f.id,
        'marca': f.marca,
        'cor': f.cor,
        'espessura': f.espessura,
        'gramas': f.gramas,
        'foto': f.foto,
    } for f in fios])


@app.route('/api/fios', methods=['POST'])
@require_login
def criar_fio():
    data = request.get_json()
    fio = Fio(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        marca=data.get('marca', ''),
        cor=data.get('cor', ''),
        espessura=data.get('espessura', ''),
        gramas=int(data.get('gramas', 0)),
        foto=data.get('foto'),
    )
    db.session.add(fio)
    db.session.commit()
    return jsonify({'id': fio.id}), 201


@app.route('/api/fios/<fio_id>/gramas', methods=['POST'])
@require_login
def atualizar_gramas(fio_id):
    fio = Fio.query.filter_by(id=fio_id, user_id=current_user.id).first_or_404()
    data = request.get_json()
    delta = int(data.get('delta', 0))
    fio.gramas = max(0, fio.gramas + delta)
    db.session.commit()
    return jsonify({'gramas': fio.gramas})


@app.route('/api/fios/<fio_id>', methods=['DELETE'])
@require_login
def deletar_fio(fio_id):
    fio = Fio.query.filter_by(id=fio_id, user_id=current_user.id).first_or_404()
    db.session.delete(fio)
    db.session.commit()
    return jsonify({'ok': True})
