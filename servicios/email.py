from flask import copy_current_request_context
from threading import Thread
from flask.ext.mail import Message, Mail


def send_email(mail, app, subject, sender, recipients, text_body, html_body):
	@copy_current_request_context
	def send_async_email(app, msg, mail):
		mail.send(msg)
	msg = Message(subject, sender=sender, recipients=recipients)
	msg.body = text_body
	msg.html = html_body
	thr = Thread(target=send_async_email, args=[app, msg, mail])
	thr.start()