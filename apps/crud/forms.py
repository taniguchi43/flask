from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, length

#ユーザ新規作成とユーザ編集フォームクラス
class UserForm(FlaskForm):
    #ユーザフォームのusername属性のラベルとバリデータを設定する
    username = StringField(
        "ユーザ名",
        validators=[
            DataRequired(message="ユーザ名は必須です。"),
            length(max=30, message="30文字以内で入力してください。"),
        ],
    )

    #ユーザフォームemail属性のラベルとバリデータを設定する
    email = StringField(
        "メールアドレス",
        validators=[
            DataRequired(message="メールアドレスは必須です。"),
            Email(message="メールアドレスの形式で入力してください。"),
        ],
    )

    #ユーザフォームpassword属性のラベルとバリデータを設定する
    password = PasswordField(
        "パスワード",
        validators=[DataRequired(message="パスワードは必須です。")],
    )

    #ユーザフォームsubmitの文言を設定する
    submit = SubmitField("新規登録")