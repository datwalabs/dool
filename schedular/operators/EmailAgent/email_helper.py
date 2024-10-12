import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

def send_email_via_zoho(subject, body, to_email, from_email, password, attachment_path):
    # Zoho SMTP server details
    smtp_server = "smtp.zoho.in"
    smtp_port = 587  # Using SSL

    try:
        # Create message container
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        # Attach the body of the email
        msg.attach(MIMEText(body, 'plain'))
        if attachment_path and os.path.isfile(attachment_path):
            attachment_name = os.path.basename(attachment_path)
            with open(attachment_path, "rb") as attachment_file:
                # Create a MIMEBase object
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment_file.read())
                
                # Encode the file in base64
                encoders.encode_base64(part)
                
                # Add header to the attachment
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {attachment_name}",
                )
                
                # Attach the part to the email
                msg.attach(part)

        # Connect to Zoho SMTP server using SSL
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Start TLS encryption

        server.login(from_email, password)  # Authenticate with Zoho Mail
        
        # Send the email
        server.sendmail(from_email, to_email, msg.as_string())
        
        # Close the connection
        server.quit()
        
        print("Email sent successfully")
        
    except Exception as e:
        print(f"Failed to send email: {e}")

# Usage
if __name__ == "__main__":
    from_email = "paresh.kumar@datwalabs.com"
    to_email = "pareshsahoo902@gmail.com"
    password = "Dcp0PBm0bCq6"  # or app-specific password
    subject = "Test Email"
    body = "This is a test email sent from Python using Zoho SMTP."
    attachment_path = "/Users/pareshsahoo/Documents/Datwa/dool/requirements.txt"  # Provide the file path for the attachment

    send_email_via_zoho(subject, body, to_email, from_email, password, attachment_path)