from flask import Flask, render_template
import paramiko
import sqlite3
import time
from datetime import datetime
import threading
import pytz

app = Flask(__name__)

# Ouvrir une connexion à la base de données
with sqlite3.connect('collecte.db') as conn:
    c = conn.cursor()

    # Créer une table si elle n'existe pas déjà
    c.execute('''
        CREATE TABLE IF NOT EXISTS data (
            id TEXT,
            cpu_usage TEXT,
            used_memory TEXT,
            total_memory TEXT,
            free_memory TEXT,
            network_stats TEXT,
            used_disk TEXT,
            total_disk TEXT,
            free_disk TEXT,
            timestamp DATETIME
        )
    ''')
    

@app.route('/')
def tableau_de_bord():
    # Ouvrir une connexion à la base de données
    with sqlite3.connect('collecte.db') as conn:
        c = conn.cursor()

        # Récupérer les dernières informations de chaque VM de la base de données
        c.execute('''
            SELECT *
            FROM data
            WHERE (id, timestamp) IN (
                SELECT id, MAX(timestamp)
                FROM data
                GROUP BY id
            )
        ''')
        vm_infos = c.fetchall()

    # Passer les informations à votre template HTML
    return render_template('tableau_de_bord.html', machines_virtuelles=vm_infos)


# Fonction pour collecter et stocker les informations de chaque VM
def collect():
        vms = [
            {'id': 'VM1', 'ip': '192.168.1.54', 'username': 'user', 'password': 'bonjour'},
            {'id': 'VM2', 'ip': '192.168.1.73', 'username': 'user', 'password': 'bonjour'},
        ]

        all_vm_data = []

        for vm in vms:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            vm_data = {}

            try:
                ssh.connect(vm['ip'], username=vm['username'], password=vm['password'])
                #print(f"Connected to VM at {vm['ip']}")

                # Récupération de l'utilisation du CPU
                stdin, stdout, stderr = ssh.exec_command('top -b -n1 | grep "Cpu(s)" | awk \'{print $2 + $4}\'')
                cpu_usage = (stdout.read().decode('utf-8').strip())
                    
                #Récupération de l'utilisation de la mémoire
                stdin, stdout, stderr = ssh.exec_command('free -m')
                output = stdout.read().decode('utf-8')
                lines = output.split('\n')
                memory_line = lines[1].split()
                total_memory = int(memory_line[1])
                used_memory = int(memory_line[2])
                memory_usage_percentage = round((used_memory / total_memory) * 100, 2)

                #Vérification de l'état de l'interface réseau
                stdin, stdout, stderr = ssh.exec_command('ip link show enp0s3')
                network_interface_status = stdout.read().decode('utf-8').strip()
                network_interface_up = 'UP' in network_interface_status

                #Vérification de la connectivité Internet
                stdin, stdout, stderr = ssh.exec_command('ping -c 1 8.8.8.8')
                internet_connectivity = '1 packets transmitted, 1 received' in stdout.read().decode('utf-8')

                #Définition des statistiques réseau
                network_stats = {
                'network_interface_status': 'Up' if network_interface_up else 'Down',
                'internet_connectivity': 'OK' if internet_connectivity else 'NOK'
                }

                #Affichage des statistiques réseau
                network_stats = f"Interface: {network_stats['network_interface_status']}, Internet: {network_stats['internet_connectivity']}"

                #Récupération de l'utilisation de l'espace disque
                stdin, stdout, stderr = ssh.exec_command('df -h /')
                output = stdout.read().decode('utf-8')
                lines = output.split('\n')
                disk_line = lines[1].split()
                percent_used_disk = disk_line[4]
                total_disk = disk_line[1]
                free_disk = disk_line[3]
                    
                paris_timezone = pytz.timezone('Europe/Paris')
                heure_actuelle_paris = datetime.now(paris_timezone)
                paris_time_str = heure_actuelle_paris.strftime('%Y-%m-%d %H:%M:%S')

                vm_data['id'] = vm['id']
                vm_data['cpu_usage'] = cpu_usage
                vm_data['memory_usage_percentage'] = memory_usage_percentage
                vm_data['total_memory'] = total_memory
                vm_data['used_memory'] = used_memory
                vm_data['network_stats'] = network_stats
                vm_data['percent_used_disk'] = percent_used_disk
                vm_data['total_disk'] = total_disk
                vm_data['free_disk'] = free_disk
                vm_data['timestamp'] = paris_time_str

            except TimeoutError:
                print(f"Unable to connect to VM at {vm['ip']}")

            finally:
                ssh.close()

            all_vm_data.append(vm_data)
        print(all_vm_data)


        # Insérer toutes les données dans la base de données
        with sqlite3.connect('collecte.db') as conn:
            c = conn.cursor()
            for vm_data in all_vm_data:
                #print(vm_data)
                c.execute('''
                    INSERT INTO data (
                        id,
                        cpu_usage,
                        used_memory,
                        total_memory,
                        free_memory,
                        network_stats,
                        used_disk,
                        total_disk,
                        free_disk,
                        timestamp
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    vm_data['id'],
                    vm_data['cpu_usage'],
                    vm_data['memory_usage_percentage'],
                    vm_data['total_memory'],
                    vm_data['used_memory'],
                    vm_data['network_stats'],
                    vm_data['percent_used_disk'],
                    vm_data['total_disk'],
                    vm_data['free_disk'],
                    vm_data['timestamp']
                ))
            conn.commit()
            
            #print(cpu_usage, memory_usage_percentage, total_memory, total_memory - used_memory, network_stats, percent_used_disk, total_disk, free_disk)

            # Supprimer les enregistrements de plus de 24 heures
            c.execute('''DELETE FROM data WHERE timestamp < datetime('now', '-70 day')''')
            conn.commit()


if __name__ == '__main__':
    def collect_and_wait():
        while True:
            collect()  # Appel de la fonction de collecte des données
            time.sleep(30)  # Attendre 30 secondes avant la prochaine collecte

    # Lancer la collecte de données dans un thread séparé
    t = threading.Thread(target=collect_and_wait)
    t.start()

    app.run(debug=False)