from flask import render_template, redirect, url_for
from app.email.forms import ContactForm
from app.email.email import send_email
from app.main import bp

@bp.route('/', methods=['GET', 'POST'])
def home():
    form = ContactForm()
    if form.validate_on_submit():
        subject = 'Novo Contato'
        recipients=['alancavalcante307@gmail.com']
        text_body=render_template('email/novo_contato.txt', form=form)
        html_body=render_template('email/novo_contato.html', form=form)

        send_email(subject=subject, recipients=recipients, text_body=text_body, html_body=html_body)
        
        return redirect(url_for('email.enviar_email'))
    return render_template('index.html', form=form)