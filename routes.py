import uuid
import os
from flask import render_template, request, jsonify, redirect, url_for, send_from_directory
from flask_login import login_required, login_user, current_user

from app import app, db, AdminUser
from models import Fio, Ideia, Projeto

@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_app'))

    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        if usuario == 'lily' and senha == 'teamo':
            login_user(AdminUser(), remember=True)
            return redirect(url_for('main_app'))
        else:
            return render_template('landing.html', erro="Usuário ou senha incorretos! 💕")

    return render_template('landing.html')

@app.route('/app')
@login_required
def main_app():
    return render_template('app.html')

# ---- APIs DO BANCO DE DADOS ----
@app.route('/api/fios', methods=['GET'])
@login_required
def get_fios():
    fios = Fio.query.order_by(Fio.created_at.desc()).all()
    return jsonify([{'id': f.id, 'marca': f.marca, 'cor': f.cor, 'espessura': f.espessura, 'gramas': f.gramas, 'foto': f.foto} for f in fios])

@app.route('/api/fios', methods=['POST'])
@login_required
def criar_fio():
    data = request.get_json()
    fio = Fio(id=str(uuid.uuid4()), marca=data.get('marca',''), cor=data.get('cor',''), espessura=data.get('espessura',''), gramas=int(data.get('gramas',0)), foto=data.get('foto'))
    db.session.add(fio)
    db.session.commit()
    return jsonify({'id': fio.id}), 201

@app.route('/api/fios/<fio_id>/gramas', methods=['POST'])
@login_required
def atualizar_gramas(fio_id):
    fio = db.session.get(Fio, fio_id)
    if fio:
        fio.gramas = max(0, fio.gramas + int(request.get_json().get('delta', 0)))
        db.session.commit()
        return jsonify({'gramas': fio.gramas})
    return jsonify({'erro': 'Não encontrado'}), 404

@app.route('/api/fios/<fio_id>', methods=['DELETE'])
@login_required
def deletar_fio(fio_id):
    fio = db.session.get(Fio, fio_id)
    if fio:
        db.session.delete(fio)
        db.session.commit()
    return jsonify({'ok': True})

@app.route('/api/ideias', methods=['GET'])
@login_required
def get_ideias():
    ideias = Ideia.query.order_by(Ideia.created_at.desc()).all()
    return jsonify([{'id': i.id, 'nome': i.nome, 'link': i.link, 'req': {'cor': i.cor_requerida, 'espessura': i.espessura_requerida}} for i in ideias])

@app.route('/api/ideias', methods=['POST'])
@login_required
def criar_ideia():
    data = request.get_json()
    req = data.get('req', {})
    ideia = Ideia(id=str(uuid.uuid4()), nome=data.get('nome',''), link=data.get('link',''), cor_requerida=req.get('cor',''), espessura_requerida=req.get('espessura',''))
    db.session.add(ideia)
    db.session.commit()
    return jsonify({'id': ideia.id}), 201

@app.route('/api/ideias/<ideia_id>', methods=['DELETE'])
@login_required
def deletar_ideia(ideia_id):
    ideia = db.session.get(Ideia, ideia_id)
    if ideia:
        db.session.delete(ideia)
        db.session.commit()
    return jsonify({'ok': True})

@app.route('/api/projetos', methods=['GET'])
@login_required
def get_projetos():
    projetos = Projeto.query.order_by(Projeto.created_at.desc()).all()
    return jsonify([{'id': p.id, 'nome': p.nome, 'progresso': p.progresso, 'notas': p.notas} for p in projetos])

@app.route('/api/projetos', methods=['POST'])
@login_required
def criar_projeto():
    projeto = Projeto(id=str(uuid.uuid4()), nome=request.get_json().get('nome',''), progresso=0, notas=[])
    db.session.add(projeto)
    db.session.commit()
    return jsonify({'id': projeto.id}), 201

@app.route('/api/projetos/<projeto_id>/progresso', methods=['POST'])
@login_required
def atualizar_progresso(projeto_id):
    projeto = db.session.get(Projeto, projeto_id)
    if projeto:
        projeto.progresso = int(request.get_json().get('valor', 0))
        db.session.commit()
    return jsonify({'ok': True})

@app.route('/api/projetos/<projeto_id>/notas', methods=['POST'])
@login_required
def adicionar_nota(projeto_id):
    projeto = db.session.get(Projeto, projeto_id)
    if projeto:
        # Agora ele pega tudo que o visual mandar (texto, data, foto e progresso)
        nova_nota = request.get_json()
        notas_atualizadas = list(projeto.notas)
        notas_atualizadas.append(nova_nota)
        projeto.notas = notas_atualizadas
        db.session.commit()
    return jsonify({'ok': True})

@app.route('/api/projetos/<projeto_id>/notas/<int:nota_idx>', methods=['DELETE'])
@login_required
def deletar_nota(projeto_id, nota_idx):
    projeto = db.session.get(Projeto, projeto_id)
    if projeto:
        notas_atualizadas = list(projeto.notas)
        if 0 <= nota_idx < len(notas_atualizadas):
            notas_atualizadas.pop(nota_idx)
            projeto.notas = notas_atualizadas
            db.session.commit()
    return jsonify({'ok': True})

@app.route('/api/projetos/<projeto_id>', methods=['DELETE'])
@login_required
def deletar_projeto(projeto_id):
    projeto = db.session.get(Projeto, projeto_id)
    if projeto:
        db.session.delete(projeto)
        db.session.commit()
    return jsonify({'ok': True})

# ---- ROTAS PARA O PWA (Aplicativo de Celular) ----
@app.route('/manifest.json')
def serve_manifest():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'manifest.json')

@app.route('/sw.js')
def serve_sw():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'sw.js')