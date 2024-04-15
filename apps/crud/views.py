from apps.app import db
from apps.crud.models import User
from apps.crud.forms import UserForm
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required

#Blueprintでcrudアプリ生成
crud = Blueprint(
    "crud",                         #エンドポイント前の階層名
    __name__,                       #通常は、__name__を指定する
    template_folder="templates",    #テンプレートフォルダ名
    static_folder="static",         #静的ファイルのフォルダ名
)

#indexエンドポイントを作成し、index.htmlを返す
@crud.route("/")
@login_required
def index():
    return render_template("crud/index.html")

@crud.route("/sql")
@login_required
def sql():
    db.session.query(User).all()    #全てSELECT

    db.session.query(User).first()  #１件のみSELECT

    db.session.query(User).get(2)   #プライマリキーの値を指定してSELECT

    db.session.query(User).count()  #検索件数をSELECT

    #db.session.query(User).paginate(2, 10, False)  #2ページ目、10件ずつ

    db.session.query(User).filter_by(id=2, username="admin").all()      #filter_byでWHERE句
    db.session.query(User).filter(User.id==2, User.username=="admin")   #filterでWHERE句　※こっちの方がめんどくさそう

    db.session.query(User).limit(1).all()               #先頭の1件のみ取得
    db.session.query(User).limit(1).offset(2).all()     #3番目のレコードから1件のみ取得

    db.session.query(User).order_by("username").all()   #ユーザ名で昇順にして取得

    db.session.query(User).group_by("username").all()   #ユーザ名でグループ化

    #データの追加(INSERT)
    user = User(username="谷口幸正", email="tani@gmail.com", password="パスワード")
    db.session.add(user)    #addで追加して、
    db.session.commit()     #commitしないと変更が反映されない！！

    #データの更新(UPDATE)
    user = db.session.query(User).filter_by(id=1).first()   #検索して
    user.username = "大原　太郎"         #書き換える
    user.email = "asdfghjkl@gmail.com"  
    user.password = "パスワード２"
    db.session.add(user)                #書き換えたものを追加する
    db.session.commit()                 #コミットして完了

    #データの削除(DELETE)
    user = db.session.query(User).filter_by(id=1).delete()
    db.session.commit()

    return "コンソールログを確認してください"

@crud.route("/users/new", methods=["GET", "POST"])
@login_required
def create_user():
    #UserFormをインスタンス化
    form = UserForm()

    #フォームの値をバリデートする
    if form.validate_on_submit():
        #ユーザを作成
        user = User(
            username = form.username.data,
            email = form.email.data,
            password = form.password.data,
        )

        #ユーザを追加してコミット
        db.session.add(user)
        db.session.commit()

        #ユーザの一覧画面へリダイレクト
        return redirect(url_for("crud.users"))
    return render_template("crud/create.html", form=form)

@crud.route("/users")
@login_required
def users():
    """ユーザの一覧を取得"""
    users = User.query.all()
    return render_template("crud/index.html", users=users)

@crud.route("/users/<user_id>", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    form = UserForm()

    #Userモデルを利用してユーザを取得
    user = User.query.filter_by(id=user_id).first()

    #formからサブミットされた場合はユーザ情報を更新しユーザの一覧画面へリダイレクト
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("crud.users"))
    
    #GETの場合はHTMLを返す
    return render_template("crud/edit.html", user=user, form=form)

#ユーザ削除
@crud.route("/users/<user_id>/delete", methods=["POST"])
@login_required
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("crud.users"))