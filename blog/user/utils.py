from PIL import Image
import secrets
import os
from flask import url_for, current_app
from email.message import EmailMessage
import smtplib

# def save_picture(form_picture):
#     random_hex = secrets.token_hex(8)
#     _, f_ext = os.path.splitext(form_picture.filename)
#     picture_fn = random_hex + f_ext
#     picture_path = os.path.join(current_app.root_path, 'static/picture', picture_fn)

#     output_size = (125, 125)
#     i = Image.open(form_picture)
#     i.thumbnail(output_size)
#     i.save(picture_path)

#     return picture_fn

def send_reset_email(user):
    token = user.get_token()

    with smtplib.SMTP('smtp.gmail.com',587) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login('projectflask513@gmail.com', 'nzlvnkoqkfbeyxjv')

        subject='hello'
        body = f'''\
        Click this link to rest your password and follow the instructions
        if you did not request for password rest please ignore this message.

        {url_for('end_user.RestPassword', token=token, _external=True)}
        '''

        msg=f'Subject:{subject}\n\n{body}'

        server.sendmail('projectflask513@gmail.com' , user.mail, msg)
