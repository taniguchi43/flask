from apps.app import db
from apps.auth.forms import SignUpForm, LoginForm
from apps.crud.models import User
from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_login import login_user, logout_user

#Blueprintを使ってauthを生成
auth = Blueprint(
    "auth",
    __name__,
    template_folder="templates",
    static_folder="static",
)

#indexエンドポイントを作成
@auth.route("/")
def index():
    return render_template("auth/index.html")

#サインアップのエンドポイント
@auth.route("/signup", methods=["GET", "POST"])
def signup():
    #SignUpFormをインスタンス化
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(
            username = form.username.data,
            email = form.email.data,
            password = form.password.data,
        )
        
        #メールアドレス重複チェック
        if user.is_duplicate_email():
            flash("指定のメールアドレスは登録済みです")
            return redirect(url_for("auth.signup"))
        
        #ユーザ情報を登録する
        db.session.add(user)
        db.session.commit()

        #ユーザ情報をセッションに格納
        login_user(user)

        #サインアップ完了時のリダイレクト先をdetector.indexに変更
        next_ = request.args.get("next")
        if next_ is None or not next_.startswith("/"):
            next_ = url_for("detector.index")
        return redirect(next_)
    
    return render_template("auth/signup.html", form=form)

#ログイン画面
@auth.route("/login", methods=["GET", "POST"])
def login():
    #LoginFormをインスタンス化
    form = LoginForm()

    if form.validate_on_submit():
        #メールアドレスからユーザを取得
        user = User.query.filter_by(email=form.email.data).first()

        #ユーザが存在しパスワードが一致する場合はログイン許可
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for("detector.index"))
        
        #ログイン失敗メッセージを設定
        flash("メールアドレスかパスワードが不正です")
    return render_template("auth/login.html", form=form)

#ログアウト画面
@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))