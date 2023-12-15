import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import csv
import psutil
import paramiko
import time

# Paramètres de configuration pour l'envoi d'e-mails
email_config = {
    'sender_email': 'votre_email@gmail.com',
    'receiver_email': 'destinataire@email.com',
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'smtp_username': 'votre_email@gmail.com',
    'smtp_password': 'votre_mot_de_passe',
}

# Paramètres de seuils pour les alertes
log_alert_threshold = 10  # Exemple : alerte si plus de 10 logs par minute
cpu_alert_threshold = 80  # Exemple : alerte si utilisation CPU > 80%
memory_alert_threshold = 80  # Exemple : alerte si utilisation mémoire > 80%
disk_alert_threshold = 80  # Exemple : alerte si utilisation disque > 80%

# Fonction pour envoyer un e-mail d'alerte
def send_alert(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = email_config['sender_email']
    msg['To'] = email_config['receiver_email']

    # Connexion au serveur SMTP
    server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
    server.starttls()
    server.login(email_config['smtp_username'], email_config['smtp_password'])

    # Envoi de l'e-mail
    server.sendmail(email_config['sender_email'], email_config['receiver_email'], msg.as_string())

    # Fermeture de la connexion
    server.quit()

# Fonction pour récupérer le nombre de logs par minute
def get_logs_per_minute(log_file):
    try:
        with open(log_file, 'r') as file:
            logs = file.readlines()
            logs_per_minute = len(logs)
        return logs_per_minute
    except FileNotFoundError:
        return 0

# Fonction pour récupérer les métriques de performance
def get_performance_metrics():
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage('/').percent
    return cpu_percent, memory_percent, disk_percent

# Script principal
path = '/collector/data'
log_file = 'chemin/vers/vos/logs.log'

while True:
    # Récupération des métriques
    logs_per_minute = get_logs_per_minute(log_file)
    cpu_percent, memory_percent, disk_percent = get_performance_metrics()

    # Vérification des seuils d'alerte
    if logs_per_minute > log_alert_threshold:
        subject = f"Alerte Log - {datetime.now()}"
        body = f"Nombre de logs par minute : {logs_per_minute}"
        send_alert(subject, body)

    if cpu_percent > cpu_alert_threshold:
        subject = f"Alerte CPU - {datetime.now()}"
        body = f"Utilisation CPU : {cpu_percent}%"
        send_alert(subject, body)

    if memory_percent > memory_alert_threshold:
        subject = f"Alerte Mémoire - {datetime.now()}"
        body = f"Utilisation mémoire : {memory_percent}%"
        send_alert(subject, body)

    if disk_percent > disk_alert_threshold:
        subject = f"Alerte Disque - {datetime.now()}"
        body = f"Utilisation disque : {disk_percent}%"
        send_alert(subject, body)

    time.sleep(60)  # Attente d'une minute avant la prochaine vérification
