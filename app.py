
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, request, render_template, redirect, flash, session
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # for flashing messages

# Email configuration
your_email = "simontroup27@gmail.com"
your_password = "dasl ajsq jhjh bbvb"
smtp_server = "smtp.gmail.com"
smtp_port = 587

@app.route('/')
def index():
    # Get the displayModal state from session (default to False if not set)
    displayModal = session.get('displayModal', False)
    # After rendering the page, reset the displayModal to False
    session['displayModal'] = False
    return render_template("index.html", displayModal=displayModal)

@app.route('/send_message', methods=['POST'])
def send_message():
    # Get data from the form
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    phone = request.form['phone']
    
    try:
        send_email(name=name, to_email=your_email, from_email=email, message=message, phone=phone)
        flash("Message sent successfully!", "success")
        session['displayModal'] = False  # Clear modal state after success
        return redirect('/')
    except Exception as e:
        print(f"Error sending email: {e}")
        flash("Failed to send message. Please try again later.", "danger")
        session['displayModal'] = True  # Set modal to True in case of error
        return redirect('/')

def send_email(to_email, name, from_email, message, phone):
    msg = MIMEMultipart()
    msg['From'] = to_email
    msg['To'] = to_email
    msg['Subject'] = f"{name}, has sent you a message"
    
    # Email body
    body = f"email : {from_email}, phone: {phone}, Message : {message}"
    msg.attach(MIMEText(body, 'plain'))
    
    # Send the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(your_email, your_password)
            server.sendmail(your_email, to_email, msg.as_string())
        print(f"Email sent to {name} at {to_email}")
    except Exception as e:
        print(f"Failed to send email to {name} at {to_email}. Error: {e}")
        raise e

if __name__ == '__main__':
    app.run(debug=True)
