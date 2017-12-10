import smtplib

class Notification():

	def sendEmail(self, server, port, username, password,toEmail, subject, message, allowAuth):

		server = smtplib.SMTP(server, port)
		server.ehlo()
		server.starttls()
		server.ehlo()

		if allowAuth:
			server.login(username, password)

		server.sendmail(username, toEmail, message)