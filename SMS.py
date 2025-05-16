import pandas as pd
from twilio.rest import Client
from datetime import datetime, timedelta
import time

# Twilio credentials
account_sid = 'AC70f29b788d04e6486b563dca8f0a2ea8'
auth_token = '23ecc93e6e74ac44f0903d201547a94c'
from_phone = '+17065743258'

# Initialize Twilio Client
client = Client(account_sid, auth_token)

# Load CSV containing scheduled dates and contact numbers
csv_file = "C:\\Users\\user\\Desktop\\Healthcare\\healthcare dataset.csv"  # Replace with the actual path to your CSV file
data = pd.read_csv(csv_file)

# Function to send SMS
def send_sms(to_phone, message):
    try:
        message = client.messages.create(
            body=message,
            from_=from_phone,
            to=to_phone
        )
        print(f"Message sent to {to_phone}")
    except Exception as e:
        print(f"Error sending message to {to_phone}: {e}")
        return False
    return True

# Fallback mechanism: retry sending SMS up to 3 times
def send_sms_with_retry(to_phone, message, retries=3):
    attempt = 0
    while attempt < retries:
        if send_sms(to_phone, message):
            return True
        else:
            print(f"Retrying... Attempt {attempt + 1}/{retries}")
            time.sleep(5)  # Wait before retrying
            attempt += 1
    print(f"Failed to send message to {to_phone} after {retries} attempts.")
    return False

# Function to check and send reminders based on scheduled date
def send_reminders():
    # Get today's date
    today = datetime.today()

    # Iterate through the rows in the dataset
    for index, row in data.iterrows():
        # Parse the scheduled date with dayfirst=True to handle DD-MM-YYYY format
        scheduled_date = pd.to_datetime(row['Scheduled Date'], dayfirst=True)  # Ensure the date is in datetime format
        contact_number = row.get('Contact Number')  # Safely get the contact number
        patient_name = row['Name']

        # If contact number is missing, skip sending SMS
        if not contact_number:
            print(f"Skipping {patient_name} as contact number is missing.")
            continue

        # Calculate the reminder date (1 day before the scheduled date)
        reminder_date = scheduled_date - timedelta(days=1)

        # If today is the reminder day, send the SMS
        if today.date() == reminder_date.date():
            message = f"Hello {patient_name}, this is a reminder for your appointment scheduled for tomorrow ({scheduled_date.strftime('%Y-%m-%d')})."
            send_sms_with_retry(contact_number, message)

# Run the reminder check function
send_reminders()
