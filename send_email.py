import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

df = pd.read_csv("C:\\Users\\user\\Desktop\\Healthcare\\healthcare dataset.csv")  # Ensure the CSV file is in the correct path

# Email Server Configuration (Gmail example)
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = "pateldp2277@gmail.com"  # Replace with your Gmail address
sender_password = "yofh wcxy vhrh pjrr"  # Use App Password if you have 2FA enabled

def send_email(recipient_email, subject, body):
    # Setting up the MIME (email structure)
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    # Attach the body (email message content)
    message.attach(MIMEText(body, "plain"))

    try:
        # Connecting to the Gmail SMTP server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
            print(f"Email sent to {recipient_email} successfully.")
    except Exception as e:
        print(f"Failed to send email to {recipient_email}: {str(e)}")

# Template for email body
template = """
Hello {patient_name},

Hope you are doing well. This is a reminder that your next appointment is scheduled on {appointment_date} at {hospital_name}.

Kind regards,
Team Healthcare
"""

# Get today's date
today = datetime.today()

# Iterate through each row in the dataset and send a personalized email
for index, row in df.iterrows():
    patient_name = row['Name']
    
    # Convert the 'Scheduled Date' from dd-mm-yyyy to datetime
    scheduled_date = pd.to_datetime(row['Scheduled Date'], format='%d-%m-%Y')
    
    # Calculate the day before the scheduled date
    day_before_appointment = scheduled_date - timedelta(days=1)
    
    # Ensure the email field is not empty
    recipient_email = row['Email']
    if pd.notna(recipient_email):
        # Check if today is the day before the scheduled date
        if today.date() == day_before_appointment.date():
            # Populate the email template with patient-specific data
            email_body = template.format(patient_name=patient_name, appointment_date=scheduled_date.strftime('%Y-%m-%d'), hospital_name=row['Hospital'])
            
            # Send the email
            send_email(recipient_email, "Appointment Reminder", email_body)
   
