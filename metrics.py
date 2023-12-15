import psutil
import time
import csv
from datetime import datetime

# Fonction pour collecter les métriques de performance
def collect_metrics():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage('/').percent

    return cpu_percent, memory_percent, disk_percent

# Fonction pour enregistrer les métriques dans un fichier CSV
def save_metrics_to_csv(metrics, filename):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(filename, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([timestamp] + list(metrics))

# Configuration des seuils d'alerte
cpu_threshold = 80  # Pourcentage d'utilisation CPU
memory_threshold = 80  # Pourcentage d'utilisation de la mémoire
disk_threshold = 80  # Pourcentage d'utilisation du disque

# Nom du fichier CSV
filename = 'performance_metrics.csv'

while True:
    # Collecte des métriques de performance
    metrics = collect_metrics()

    # Enregistrement des métriques dans le fichier CSV
    save_metrics_to_csv(metrics, filename)

    # Vérification des seuils d'alerte
    if metrics[0] > cpu_threshold:
        print(f"Alerte : Utilisation CPU élevée ({metrics[0]}%)")

    if metrics[1] > memory_threshold:
        print(f"Alerte : Utilisation de la mémoire élevée ({metrics[1]}%)")

    if metrics[2] > disk_threshold:
        print(f"Alerte : Utilisation du disque élevée ({metrics[2]}%)")

    time.sleep(60)  # Attente d'une minute avant la prochaine collecte de métriques
