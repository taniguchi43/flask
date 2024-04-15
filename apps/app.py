from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from apps.config import config

#LoginManagerをインスタンス化
login_manager = LoginManager()

#login_view属性に未ログイン時にリダイレクトするエンドポイントを指定
login_manager.login_view = "auth.signup"

#SQLAlchemyをインスタンス化
db = SQLAlchemy()

#CSRFProtectクラスをインスタンス化
csrf = CSRFProtect()

#create_app関数を作成
def create_app(config_key):
    #Flaskインスタンス生成
    app = Flask(__name__)

    #config_keyにマッチする環境のコンフィグクラスを読み込む
    #ので、app.config.from_mappingは削除(コメントアウト)
    app.config.from_object(config[config_key])

    # #アプリのコンフィグ設定をする
    # app.config.from_mapping(
    #     SECRET_KEY="2AZSMss3p5QPbcY2hBs",
    #     SQLALCHEMY_DATABASE_URI=
    #      f"sqlite:///{Path(__file__).parent.parent / 'local.sqlite'}",
    #     SQLALCHEMY_TRACK_MODIFICATIONS=False,
    #     #SQLをコンソールログに出力する
    #     SQLALCHEMY_ECHO = True,
    #     WTF_CSRF_SECRET_KEY="AuwzyszU5sugKN7KZs6f"
    # )

    #カスタムエラー画面を登録
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)

    #アプリと連携
    csrf.init_app(app)

    #SQLAlchemyとアプリを連携する
    db.init_app(app)

    #Migrateとアプリを連携する
    Migrate(app, db)

    #login_managerとアプリを連携する
    login_manager.init_app(app)

    #CRUDパッケージからviewsをimport
    from apps.crud import views as crud_views

    #register_blueprintを使いviewsのcrudをアプリへ登録
    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    #authパッケージからviewsをimportする
    from apps.auth import views as auth_views

    #register_blueprintを使いviewsのauthをアプリへ登録
    app.register_blueprint(auth_views.auth, url_prefix="/auth")

    #detectorパッケージからviewsをimportする
    from apps.detector import views as dt_views

    #register_blueprintを使いviewsのdtをアプリへ登録
    app.register_blueprint(dt_views.dt)

    return app

#カスタムエラー（404）の関数作成
def page_not_found(e):
    """404 Not Found"""
    return render_template("404.html"), 404

#カスタムエラー（500）の関数作成
def internal_server_error(e):
    """500 Internal Server Error"""
    return render_template("500.html"), 500