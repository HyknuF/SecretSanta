import random
import os
import smtplib
import zipfile
import getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Introduction
intro = """
###################################################################################################################
#
# Hi, and welcome to the Secret Santa Generator!
#
# If you're planning a Secret Santa event for yourself and your friends, club members, colleagues, etc.,
# this useful tool allows you to enter all participants with their names, email addresses, and other details.
# Afterwards, the groups will be randomly assigned, and an email will be sent to each participant
# with the details of their assigned person. In case an email fails to be delivered,
# a text file with the recipient's assignment will be created for each participant.
# The text files will be collected and saved in a single zip file.
# If you're the organizer and want to keep it a secret, you can participate without knowing all the assignments :-)
#
# To send emails, you will need the following information in addition to the recipient addresses:
# - Your email address as the sender
# - The SMTP server of your email provider (you can quickly search for it if you're unsure)
# - Your email password
#
# Don't worry, your email login is SSL encrypted!
#
# If you encounter any errors, I appreciate constructive feedback.
#
# Now, have fun with your Secret Santa event!
#
###################################################################################################################

"""
print(intro)

go = input("--- Press ENTER to start --- | --- Ctrl+C to exit --- ")
print(go)

# Define the number of participants
while True:
    try:
        participants = int(input('How many people are participating?: '))
        if participants != 1:
            break
        else:
            print("Error. It's difficult to do Secret Santa alone.")
    except ValueError:
        print("Error. Only integers are allowed.")

# Collect names and email addresses of participants
name_email = {}
for i in range(1, participants + 1):
    name = input(f"Enter the name of participant {i}: ")
    email = input(f"Enter the email address of participant {i}: ")
    name_email[name] = email

# Generate random order
participant_list = list(name_email.keys())
random.shuffle(participant_list)

santas = participant_list.copy()
receivers = participant_list.copy()
random.shuffle(receivers)

# Make sure Santa and Receiver are not the same person
while any(santa == receiver for santa, receiver in zip(santas, receivers)):
    random.shuffle(receivers)

# Create Secret Santa assignments
santas_to_receivers = {santa: receiver for santa, receiver in zip(santas, receivers)}

location = input("When and where is the Secret Santa event taking place?: ")
amount = input("Budget for the gifts: ")
motto = input("Motto: ")
other_details = input("Other details?: ")

# Send emails
subject = input("Email subject: ")
body_user = input("Email message (previously entered details will be automatically included): ")
sender_email = input("Enter sender's email address: ")
smtp_server = input("Please enter the SMTP server (e.g., smtp.gmail.com): ")
port = 465

max_attempts = 3
attempts = 0

while attempts < max_attempts:
    password = getpass.getpass("Enter SMTP password: ")
    print("Establishing connection...")

    # Login to SMTP server
    try:
        server = smtplib.SMTP_SSL(smtp_server, port)
        _, _ = server.login(sender_email, password)
        server.quit()
        print("Password accepted")
        break
    except smtplib.SMTPAuthenticationError:
        attempts += 1
        remaining_attempts = max_attempts - attempts
        print(f"Invalid password. {remaining_attempts} attempts remaining.")

if attempts == max_attempts:
    print("Maximum number of attempts reached. Exiting.")
    exit()


# Final confirmation
send_acknowledge = input("Do you want to send the emails now? (Yes/No): ")

if send_acknowledge.lower() == 'yes':
    for santa, receiver in santas_to_receivers.items():

        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = name_email[santa]
        message['Subject'] = subject

        complete_body = f"""{body_user}
            <br><br>You have to buy a gift for: <b>{receiver}!</b>
            <br><br><b>Details:</b>
            <br><b>Location:</b> {location}
            <br><b>Budget:</b> {amount}
            <br><b>Motto:</b> {motto}
            <br><b>Other details:</b> {other_details}
            <br><br>Have fun with the Secret Santa event!"""

        message.attach(MIMEText(complete_body, 'html'))

        with smtplib.SMTP_SSL(smtp_server, port) as server:
            server.login(sender_email, password)
            server.send_message(message)
    print("Emails sent! Enjoy your Secret Santa event!")
else:
    print("Email not sent. Exiting the program.")
    exit()

zip_file_name = "secretsanta.zip"

with zipfile.ZipFile(zip_file_name, "w") as zip_file:
    for santa, receiver in santas_to_receivers.items():
        file_name = f"For {santa} Only.txt"
        with open(file_name, "w") as file:
            content = f"You have to buy a gift for: {receiver.title()}\n"
            file.write(content)
        zip_file.write(file_name)
        os.remove(file_name)
