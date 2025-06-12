import pandas as pd
import smtplib
from email.message import EmailMessage
import getpass

def send_emails(contact_file, subject, body_template, sender_email, smtp_server, smtp_port):
    try:
        contacts = pd.read_csv(contact_file)
    except Exception as e:
        print(f"Error reading contacts: {e}")
        return

    password = getpass.getpass(f"Enter password for {sender_email}:")
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        try:
            server.login(sender_email, password)
        except smtplib.SMTPAuthenticationError:
            print("Failed to authenticate. Check email and password.")
            return

        for index, row in contacts.iterrows():
            name = row["name"]
            recipient = row["email"]

            msg = EmailMessage()
            msg["Subject"] = subject
            msg["From"] = sender_email
            msg["To"] = recipient

            personalized_body = body_template.replace("{name}", name)
            msg.set_content(personalized_body)

            try:
                server.send_message(msg)
                print(f"Sent to {name} ({recipient})")
            except Exception as e:
                print(f"Failed to send to {recipient}: {e}")
    print("All emails processed")

if __name__ == "__main__":
    #Example usage
    subject = "Your Custom Subject"
    body = "Hi {name}, \n\nThis is a test email from my Python bot.\n\nCheers!"
    send_emails("contacts.csv", subject, body, "youremail@example.com", "smtp.gmail.com", 465)
