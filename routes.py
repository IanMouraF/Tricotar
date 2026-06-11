import uuid
from flask import session, render_template, request, jsonify
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, db, login_manager
from models import User, Fio


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)


@app.before_request
def make_session_permanent():
    session.permanent = True


# ---- Páginas ----

@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('app.html', user=current_user)
    return render_template('landing.html')


@app.route('/app')
@login_required
def main_app():
    return render_template('app.html', user=current_user)


# ---- Auth ----

@app.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''
    first_name = (data.get('first_name') or '').strip()

    if not email or not password:
        return jsonify({'error': 'E-mail e senha são obrigatórios.'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Este e-mail já está cadastrado.'}), 409

    user = User(
        id=str(uuid.uuid4()),
        email=email,
        first_name=first_name,
        password_hash=generate_password_hash(password),
    )
    db.session.add(user)
    db.session.commit()
    login_user(user)
    return jsonify({'ok': True, 'first_name': user.first_name}), 201


@app.route('/auth/login', methods=['POST'])
def auth_login():
    data = request.get_json()
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'E-mail ou senha incorretos.'}), 401

    login_user(user, remember=True)
    return jsonify({'ok': True, 'first_name': user.first_name})


@app.route('/auth/logout', methods=['POST'])
@login_required
def auth_logout():
    logout_user()
    session.clear()
    return jsonify({'ok': True})


# ---- API: Fios ----

@app.route('/api/fios', methods=['GET'])
@login_required
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
@login_required
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
@login_required
def atualizar_gramas(fio_id):
    fio = Fio.query.filter_by(id=fio_id, user_id=current_user.id).first_or_404()
    data = request.get_json()
    delta = int(data.get('delta', 0))
    fio.gramas = max(0, fio.gramas + delta)
    db.session.commit()
    return jsonify({'gramas': fio.gramas})


@app.route('/api/fios/<fio_id>', methods=['DELETE'])
@login_required
def deletar_fio(fio_id):
    fio = Fio.query.filter_by(id=fio_id, user_id=current_user.id).first_or_404()
    db.session.delete(fio)
    db.session.commit()
    return jsonify({'ok': True})
