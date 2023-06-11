import random
import os
import smtplib
import zipfile
import getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# introtext
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

# Anzahl der Teilnehmer definieren
while True:
    try:
        teilnehmer = int(input('Wieviele Personen nehmen teil?: '))
        if teilnehmer != 1:
            break
        else:
            print("Fehler. Alleine ist wichteln schwierig.")
    except ValueError:
        print("Fehler. Nur Ganzzahlen erlaubt.")

# Name und E-Mailadresse der Teilnehmer
name_adresse = {}
for i in range(1, teilnehmer + 1):
    name = input(f"Name von Teilnehmer {i} eingeben: ")
    email = input(f"E-Mail-Adresse von Teilnehmer {i} eingeben: ")
    name_adresse[name] = email

# Zufällige Reihenfolge generieren
participants = list(name_adresse.keys())
random.shuffle(participants)

santas = participants.copy()
receivers = participants.copy()
random.shuffle(receivers)

# Sicherstellen, dass Santa + Receiver nicht dieselbe Person ist
while any(santa == receiver for santa, receiver in zip(santas, receivers)):
    random.shuffle(receivers)

# Wichtelgruppierung erstellen
santas_to_receivers = {santa: receiver for santa, receiver in zip(santas, receivers)}

ort = input("Wann und Wo wird gewichtelt?: ")
betrag = input("Wichtelbetrag in €: ")
motto = input("Motto: ")
sonstiges = input("Sonstiges?: ")

# E-Mail versenden
subject = input("E-Mail Betreff: ")
body_user = input("E-Mail Nachricht (bereits eingegebene Eckdaten werden automatisch ergänzt: ")
absender = input("Absender E-Mail eingeben: ")
smtp_server = input("Bitte SMTP Server eingeben (z.B: smtp.gmail.com): ")
port = 465

max_attempts = 3
attempts = 0

while attempts < max_attempts:
    password = getpass.getpass("SMTP-Passwort eingeben: : ")
    print("Verbindung wird hergestellt...")

    # Login auf STMP-Server
    try:
        server = smtplib.SMTP_SSL(smtp_server, port)
        _, _ = server.login(absender, password)
        server.quit()
        print("Passwort OK")
        break
    except smtplib.SMTPAuthenticationError:
        attempts += 1
        remaining_attempts = max_attempts - attempts
        print(f"Passwort falsch. Noch {remaining_attempts} Versuche.")

if attempts == max_attempts:
    print("Maximale Anzahl der Versuche erreicht. Exiting.")
    exit()


# Abschließende Bestätigung
send_acknowledge = input("Sollen die E-Mails jetzt versendet werden (Ja/Nein)?: ")

if send_acknowledge.lower() == 'ja':
    for santa, receiver in santas_to_receivers.items():

        message = MIMEMultipart()
        message['From'] = absender
        message['To'] = name_adresse[santa]
        message['Subject'] = subject

        body_gesamt = f"""{body_user}
            <br><br>Du darfst ein Geschenk besorgen fuer: <b>{receiver}!</b>
            <br><br><b>Eckdaten:</b>
            <br><b>Ort:</b> {ort}
            <br><b>Betrag:</b> € {betrag}
            <br><b>Motto:</b> {motto}
            <br><b>Sonstiges:</b> {sonstiges}
            <br><br>Viel Spaß beim wichteln!"""

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
    for santa, receiver in santas_to_receivers.items():
        file_name = f"Darf nur von {santa} geöffnet werden.txt"
        with open(file_name, "w") as file:
            content = f"Du darfst ein Geschenk besorgen für: {receiver.title()}\n"
            file.write(content)
        zip_file.write(file_name)
        os.remove(file_name)
