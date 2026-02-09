from flask import Flask, render_template, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_emails():
    data = request.json
    try:
        # هنا يتم استخدام البيانات التي أدخلتها أنت في الخانات
        server = smtplib.SMTP(data['host'], int(data['port']))
        server.starttls()
        server.login(data['user'], data['password'])
        
        emails = data['emails']
        for email in emails:
            email = email.strip()
            if email:
                msg = MIMEMultipart()
                msg['From'] = data['user']
                msg['To'] = email
                msg['Subject'] = data['subject']
                msg.attach(MIMEText(data['body'], 'html'))
                server.send_message(msg)
        
        server.quit()
        return jsonify({"status": "success", "message": "تم الإرسال بنجاح!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})