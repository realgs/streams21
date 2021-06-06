import datetime
import json
import smtplib


def send(currency, attachment, recipient=None):
    if attachment not in ["buy", "archives"]:
        print("No such file! Try again...")
        return

    file = open(f"data/{attachment}.json", "r")
    attachment_data = json.load(file)
    file.close()
    if currency.upper() not in attachment_data.keys():
        print("No records on this currency! Try Again...")
        return

    if currency == "all":
        pass
    else:
        attachment_data = attachment_data[currency.upper()]

    credentials_file = open("confidential.txt", "r")
    credentials = credentials_file.readlines()
    credentials_file.close()

    sender = credentials[0]
    password = credentials[1]
    if not recipient:
        recipient = credentials[2]

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(sender, password)

        subject = f"Report {currency.upper()}, generated on {datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}"

        message = f'Subject: {subject}\n\n{json.dumps(attachment_data, indent=10)}'

        smtp.sendmail(sender, recipient, message)
