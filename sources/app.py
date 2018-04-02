import smtplib
import sys
sys.path.append("..")
import setting

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/studies')
def studies():
    return render_template('studies.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/sendMail', methods=['POST'])
def send():
    fromaddr = str(request.form['author'])
    toaddr = "edwynpeignon.website@gmail.com"
    message = fromaddr + "\n" + str(request.form['message'])

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = request.form['subject']

    body = message
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(toaddr, setting.PASSWORD)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    print("done")
    server.quit()
    return render_template('contact.html')

if __name__ == "__main__":
    app.run()

