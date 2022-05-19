from werkzeug.routing import ValidationError
from flask_wtf import FlaskForm
from config import Config
from wtforms import StringField, TextAreaField, BooleanField, PasswordField
from wtforms.validators import DataRequired

class EntryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Content', validators=[DataRequired()])
    is_published = BooleanField('Is Published?')

class LoginForms(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    def validate_username(self, field):
        if field.data != Config.ADMIN_USERNAME:
            raise ValidationError("Invalid username")
        return field.data

    def validate_password(self, field):
        if field.data != Config.ADMIN_PASSWORD:
            raise ValidationError("Invalid password")
        return field.data

class DeleteForms(FlaskForm):
    def delete_entry(self):
        return redirect(url_for('delete_entry', entry_id=draft.id))

