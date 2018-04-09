import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Flask, render_template, request
import json
import setting
from geneticAlgorithm.geneticApp import main

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


@app.route('/genetic')
def genetic():
    return render_template('genetic.html')


@app.route('/generate', methods=['POST'])
def generer():
    tab = request.form['tab'].split(',')

    student = []
    marks = []

    number_of_groups = int(request.form['group'])

    print(int(request.form['slidebar']))

    count = 0
    try:
        for string in tab:
            if count % 2 == 0:
                student.append(str(string))
            else:
                marks.append(float(string))
            count = count + 1
    except:
        return render_template('genetic.html', error = "Use the right syntax : example(Name : 'Marc', Mark : 18.65 )")

    if len(marks) < 4:
        return render_template('genetic.html', error="Add at least 4 students.",student=student,marks=marks)

    try:
        class_ =  main(student,marks,number_of_groups,int(request.form['slidebar']))
    except:
        messageError = "Error, check if you have the right syntax. If your syntax is right you can report me the bug via the contact tab."
        return render_template('genetic.html', error=messageError,student=student,marks=marks)

    return render_template('geneticResult.html',  groups = class_.get_groups(), classe=class_)

if __name__ == "__main__":
    app.run()

