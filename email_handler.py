import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import re

class EmailHandler:
    def parse_recipient(self, line):
        match = re.match(r"(.+?)\s*<(.+?)>", line.strip())
        if match:
            name, email = match.groups()
        else:
            parts = line.split()
            if len(parts) >= 2:
                name = " ".join(parts[:-1])
                email = parts[-1]
            else:
                return None, None
        return email, name

    def generate_email_content(self, name, email, template, subject_template):
        personalized_content = template.replace("{{name}}", name).replace("{{email}}", email)
        personalized_subject = subject_template.replace("{{name}}", name).replace("{{email}}", email)
        return personalized_content, personalized_subject

    def send_email(self, sender_email, sender_pass, recipient_email, subject, content, attachments):
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = recipient_email

        body = MIMEText(content, "plain")
        msg.attach(body)

        for file in attachments:
            with open(file, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={file.split('/')[-1]}"
                )
                msg.attach(part)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, sender_pass)
            smtp.send_message(msg)
