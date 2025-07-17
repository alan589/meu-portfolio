from flask import render_template
from app.email import bp


@bp.route('/email-enviado')
def enviar_email():
    return render_template('email/email_enviado.html')
