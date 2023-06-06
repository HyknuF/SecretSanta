import os
import numpy as np
import smtplib
import zipfile
import getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

intro = """
###################################################################################################################
#
# Hi, und willkommen zum Wichtelgenerator! 
#
# Wenn du wichteln für dich und deine Freunde, Vereinsmitglieder, Kollegen, etc.. planst,
# kannst du mit diesem nützlichen Tool einfach alle Teilnehmenden mit Name und E-Mail-Adresse
# und allen Eckdaten eingeben. Danach werden automatisiert die Gruppierungen gelost und
# an alle eine entsprechende Mail versendet. Falls eine Mail mal nicht ankommen sollte,
# wird zusätzlich für jeden Teilnehmer eine Text-Datei mit Wichtelpartner erzeugt.
# Die Text-Dateien werden gesammelt in einer Zip-Datei gespeichert.
# Wenn du als Planer also nicht spickelst, kannst du auch ohne alles zu wissen mitwichteln :-)
#
# Um E-Mails versenden zu können, benötigst du neben den Empfänger-Adressen:
# - Deine Absender-Adresse
# - Den STMP-Server deines Mail-Anbieters (zur Not kurz danach googlen)
# - Dein E-Mail Passwort
#
# Keine Sorge, dein E-Mail Login ist SSL verschlüsselt!
#
# Solltest du auf einen Fehler stoßen, so freue ich mich über konstruktive Rückmeldungen.
#
# Und nun, viel Spaß beim Wichteln!
#
###################################################################################################################

"""
print(intro)

go = input("--- ENTER zum Starten --- | --- Strg+C zum Beenden --- ")
print(go)

# Get the number of participants
while True:
    try:
        teilnehmer = int(input('Wieviele Personen nehmen teil?: '))
        break
    except ValueError:
        print("Fehler. Nur Ganzzahlen erlaubt.")

# Get the name and email address of each participant
fam = {}
for i in range(1, teilnehmer + 1):
    name = input(f"Name von Teilnehmer {i} eingeben: ")
    email = input(f"E-Mail-Adresse von Teilnehmer {i} eingeben: ")
    fam[name] = email

ort = input("Wann und Wo wird gewichtelt?: ")
betrag = input("Wichtelbetrag in €: ")
motto = input("Motto: ")
sonstiges = input("Sonstiges?: ")

# SELECT SECRET SANTAS
santas = list(np.random.choice(list(fam.keys()), len(list(fam.keys())), replace=False))
receivers = [santas[k - 1] for k in range(len(santas))]

subject = input("E-Mail Betreff: ")
body_user = input("E-Mail Nachricht eingegebene (bereits eingebene Eckdaten werden automatisch ergänzt: ")

# SENDING EMAILS
absender = input("Absender E-Mail eingeben: ")
smtp_server = input("Bitte SMTP Server eingeben (z.B: smtp.gmail.com): ")
port = 465

max_attempts = 3
attempts = 0

while attempts < max_attempts:
    password = getpass.getpass("Enter the SMTP password: ")
    print("Connecting...")

    # Attempt to login to the SMTP server
    try:
        server = smtplib.SMTP_SSL(smtp_server, port)
        _, _ = server.login(absender, password)
        server.quit()
        print("Password OK")
        break
    except smtplib.SMTPAuthenticationError:
        attempts += 1
        remaining_attempts = max_attempts - attempts
        print(f"Passwort falsch. Noch {remaining_attempts} Versuche.")

if attempts == max_attempts:
    print("Maximale Anzahl der Versuche erreicht. Exiting.")
    exit()


# Ask for acknowledgment
send_acknowledge = input("Sollen die E-Mails jetzt versendet werden (Ja/Nein)?: ")

if send_acknowledge.lower() == 'ja':
    for i, name in enumerate(fam):
        santa = santas[i]

        message = MIMEMultipart()
        message['From'] = absender
        message['To'] = fam[name]
        message['Subject'] = subject

        body_gesamt = (f"{body_user} \
            <br><br>Du darfst ein Geschenk besorgen fuer: <b>{santa}!</b> \
            <br><br><b>Eckdaten:</b> \
            <br><b>Ort:</b> {ort}, \
            <br><b>Betrag in €:</b> {betrag} \
            <br><b>Motto:</b> {motto} \
            <br><b>Sonstiges:</b> {sonstiges} \
            <br><br>Viel Spaß beim wichteln!")

        message.attach(MIMEText(body_gesamt, 'html'))

        with smtplib.SMTP_SSL(smtp_server, port) as server:
            server.login(absender, password)
            server.send_message(message)
    print("E-Mails versendet! Viel Spaß beim Wichteln!")
else:
    print("E-Mail nicht versendet. Programmende.")
    exit()

zip_file_name = "secret_santa_output.zip"

with zipfile.ZipFile(zip_file_name, "w") as zip_file:
    for receiver, santa in zip(receivers, santas):
        file_name = f"Darf nur von {receiver} geöffnet werden.txt"
        with open(file_name, "w") as file:
            content = f"Dein Wichtelpartner: {santa.title()}\n"
            file.write(content)
        zip_file.write(file_name)
        os.remove(file_name)
