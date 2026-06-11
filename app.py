    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_login import LoginManager, UserMixin
    from sqlalchemy.orm import DeclarativeBase
    import os
    from werkzeug.middleware.proxy_fix import ProxyFix
    import logging

    logging.basicConfig(level=logging.DEBUG)

    class Base(DeclarativeBase):
        pass

    app = Flask(__name__)
    app.secret_key = os.environ.get("SESSION_SECRET", "segredo-do-cantinho-da-lilly")
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # Já configurado para ler o Supabase!
    db_url = os.environ.get("EXTERNAL_DB_URL")
    if not db_url:
        print("⚠️ AVISO: EXTERNAL_DB_URL não encontrado nos Segredos. Usando banco local.")
        db_url = "sqlite:///banco_local.db"

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        'pool_pre_ping': True,
        "pool_recycle": 300,
    }

    db = SQLAlchemy(app, model_class=Base)

    login_manager = LoginManager(app)
    login_manager.login_view = "login"

    class AdminUser(UserMixin):
        def __init__(self):
            self.id = "lily"

    @login_manager.user_loader
    def load_user(user_id):
        if user_id == "lily":
            return AdminUser()
        return None

    with app.app_context():
        import models  # noqa: F401
        db.create_all()
        print(f"🔌 BANCO CONECTADO: {db_url}")
        logging.info("Tabelas criadas com sucesso!")