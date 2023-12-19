import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import psutil
import time
import subprocess
from flask import Flask, render_template
import random

# Script principal
path = '/collector/data'
log_file = 'chemin/vers/vos/logs.log'

# Configuration des destinataires d'alertes
alert_recipients = ['admin@example.com', 'sms:+1234567890']

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
vm_cpu_critical_threshold = 90  # Exemple : alerte si utilisation CPU de la VM > 90%
vm_memory_critical_threshold = 90  # Exemple : alerte si utilisation mémoire de la VM > 90%

# Historique des métriques
metrics_history = []

# Seuil de dégradation de la qualité du code
quality_threshold = 8  # Exemple : Seuil pour la complexité du code

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

# Nouveaux seuils pour l'alerte de ping
ping_alert_threshold = 1  # Exemple : alerte si le ping échoue une fois

# Fonction pour envoyer une alerte de ping
def send_ping_alert(subject, body):
    send_alert(subject, body)

# Fonction pour effectuer un ping
def check_ping(host):
    try:
        subprocess.check_output(["ping", "-c", "1", host])
        return True
    except subprocess.CalledProcessError:
        return False

# Fonction pour récupérer le nombre de logs par minute
def get_logs_per_minute(log_file):
    try:
        with open(log_file, 'r') as file:
            logs = file.readlines()
            logs_per_minute = len(logs)
        return logs_per_minute
    except FileNotFoundError:
        return 0

# Fonction pour envoyer une alerte de performances critiques
def send_performance_alert(subject, body, recipients):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = email_config['sender_email']
    msg['To'] = ', '.join(recipients)

    # Connexion au serveur SMTP
    server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
    server.starttls()
    server.login(email_config['smtp_username'], email_config['smtp_password'])

    # Envoi de l'e-mail
    server.sendmail(email_config['sender_email'], recipients, msg.as_string())

    # Fermeture de la connexion
    server.quit()

# Fonction pour surveiller les performances des VM
def monitor_vm_performance(vm_name):
    # Simulons ici l'utilisation CPU et mémoire d'une VM
    vm_cpu_percent = psutil.cpu_percent()  # Remplacez cela par la récupération réelle de l'utilisation CPU de la VM
    vm_memory_percent = psutil.virtual_memory().percent  # Remplacez cela par la récupération réelle de l'utilisation mémoire de la VM

    # Vérification des seuils d'alerte
    if vm_cpu_percent > vm_cpu_critical_threshold:
        subject = f"Alerte VM - {vm_name} - CPU Critique - {datetime.now()}"
        body = f"Utilisation CPU de la VM {vm_name} : {vm_cpu_percent}%"
        send_performance_alert(subject, body, alert_recipients)

    if vm_memory_percent > vm_memory_critical_threshold:
        subject = f"Alerte VM - {vm_name} - Mémoire Critique - {datetime.now()}"
        body = f"Utilisation mémoire de la VM {vm_name} : {vm_memory_percent}%"
        send_performance_alert(subject, body, alert_recipients)

# Fonction pour vérifier la qualité du code et déclencher des alertes
def check_code_quality(metrics):
    if metrics['complexity'] > quality_threshold:
        subject = f"Alerte Qualité du Code - {datetime.now()}"
        body = f"La complexité du code a dépassé le seuil : {metrics['complexity']}"
        send_alert(subject, body)

# Fonction pour envoyer une alerte
def send_alert(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = email_config['sender_email']
    msg['To'] = ', '.join(alert_recipients)

    # Connexion au serveur SMTP
    server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
    server.starttls()
    server.login(email_config['smtp_username'], email_config['smtp_password'])

    # Envoi de l'e-mail
    server.sendmail(email_config['sender_email'], alert_recipients, msg.as_string())

    # Fermeture de la connexion
    server.quit()

# Simulation du processus CI/CD avec mise à jour des métriques
def simulate_ci_cd_process():
    global code_metrics

    # Collecte des métriques (simulée avec des données aléatoires)
    new_metrics = {
        'complexity': random.randint(1, 10),
        'duplication': random.randint(1, 20),
        'code_coverage': random.uniform(50, 100),
    }

    # Mise à jour des métriques
    code_metrics = new_metrics

    # Vérification de la qualité du code et envoi d'alertes si nécessaire
    check_code_quality(code_metrics)

    # Ajout des métriques à l'historique
    metrics_history.append({'timestamp': datetime.now(), 'metrics': new_metrics})

while True:
    # Récupération des métriques
    logs_per_minute = get_logs_per_minute(log_file)
    cpu_percent, memory_percent, disk_percent = get_performance_metrics()

    # Vérification des seuils d'alerte pour les logs
    if logs_per_minute > log_alert_threshold:
        subject = f"Alerte Log - {datetime.now()}"
        body = f"Nombre de logs par minute : {logs_per_minute}"
        send_alert(subject, body)

    # Vérification de l'alerte de ping
    if not check_ping('example.com'):
        subject = f"Alerte Ping - {datetime.now()}"
        body = "Échec du ping vers example.com"
        send_ping_alert(subject, body)

    # Vérification des seuils d'alerte pour les performances du serveur
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

    # Surveiller les performances de la VM
    monitor_vm_performance('Nom_VM')  # Remplacez 'Nom_VM' par le nom de votre machine virtuelle

    # Simulation du processus CI/CD
    simulate_ci_cd_process()

    time.sleep(60)  # Attente d'une minute avant la prochaine vérification
