from flask_wtf.file import FileAllowed, FileField, FileRequired
from flask_wtf.form import FlaskForm
from wtforms.fields.simple import SubmitField

#画像アップロード機能のUploadImageFormクラスを作成
class UploadImageForm(FlaskForm):
    #ファイルフィールドに必要なバリデーションを設定
    image = FileField(
        validators=[
            FileRequired("画像ファイルを指定してください。"),
            FileAllowed(["png", "jpg", "jpeg"], "サポートされていない画像形式です。"),
        ]
    )

    submit = SubmitField("アップロード")

#物体検知機能のDetectorFormクラスを作成
class DetectorForm(FlaskForm):
    submit = SubmitField("検知")

#画像削除昨日のDeleteFormクラスを作成
class DeleteForm(FlaskForm):
    submit = SubmitField("削除")