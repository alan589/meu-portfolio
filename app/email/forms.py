from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length


class ContactForm(FlaskForm):
    name = StringField('Qual é seu nome', validators=[DataRequired()], render_kw={'placeholder': 'Nome'})
    email = EmailField('Seu email', validators=[DataRequired()], render_kw={'placeholder': 'Email'})
    about_project = TextAreaField('Descreva seu projeto', validators=[DataRequired(), Length(min=10, max=2000)], render_kw={'rows':7, 'placeholder': 'Descreva seu projeto em algumas palavras.'})
    submit = SubmitField('Enviar Contato')    