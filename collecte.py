from flask import Flask, render_template
import paramiko


app = Flask(__name__)



@app.route('/')
def tableau_de_bord():
    vms = [
        {'id': 'VM1', 'ip': '192.168.19.227', 'username': 'user', 'password': 'bonjour'},
        #{'id': 'VM2', 'ip': '192.168.1.55', 'username': 'user', 'password': 'bonjour'},

    ]


    vm_infos = []

    for vm in vms:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(vm['ip'], username=vm['username'], password=vm['password'])

            # Récupération de l'utilisation de la mémoire
            stdin, stdout, stderr = ssh.exec_command('free -m')
            output = stdout.read().decode('utf-8')
            lines = output.split('\n')
            memory_line = lines[1].split()
            total_memory = int(memory_line[1])
            used_memory = int(memory_line[2])
            memory_usage_percentage = round((used_memory / total_memory) * 100, 2)

            # Récupération de l'utilisation du CPU
            stdin, stdout, stderr = ssh.exec_command('top -b -n1 | grep "Cpu(s)" | awk \'{print $2 + $4}\'')
            cpu_usage = (stdout.read().decode('utf-8').strip())


            # Vérification de l'état de l'interface réseau
            stdin, stdout, stderr = ssh.exec_command('ip link show enp0s3')
            network_interface_status = stdout.read().decode('utf-8').strip()
            network_interface_up = 'UP' in network_interface_status

            # Vérification de la connectivité Internet
            stdin, stdout, stderr = ssh.exec_command('ping -c 1 8.8.8.8')
            internet_connectivity = '1 packets transmitted, 1 received' in stdout.read().decode('utf-8')

            # Définition des statistiques réseau
            network_stats = {
                'network_interface_status': 'Up' if network_interface_up else 'Down',
                'internet_connectivity': 'OK' if internet_connectivity else 'NOK'
            }

            # Affichage des statistiques réseau
            network_stats = f"Interface: {network_stats['network_interface_status']}, Internet: {network_stats['internet_connectivity']}"
            print(network_stats)


            # Récupération de l'utilisation de l'espace disque
            stdin, stdout, stderr = ssh.exec_command('df -h /')
            output = stdout.read().decode('utf-8')
            lines = output.split('\n')
            disk_line = lines[1].split()
            percent_used_disk = disk_line[4]
            total_disk = disk_line[1]
            free_disk = disk_line[3]


            # Récupération de l'utilisation du disque
            # stdin, stdout, stderr = ssh.exec_command('df -h')
            # disk_usage_raw = stdout.read().decode('utf-8').strip()
            # disk_usage_lines = disk_usage_raw.split('\n')
            # disk_usage = disk_usage_lines[1:]  # Ignore the first line which is the header
            
            # # Traitement de l'utilisation du disque
            # disk_usage_info = []
            # for line in disk_usage:
            #     parts = line.split()
            #     if parts[5] == '/':  # Only consider the root filesystem
            #         disk_usage_info.append({
            #             'use%': parts[4]
            #         })

            # disk_usage = disk_usage_info[0]['use%'] if disk_usage_info else 'N/A'

            ssh.close()

            # Création d'un dictionnaire pour la machine virtuelle
            vm_info = {
            'id': vm['id'],
            'cpu_usage': f'{cpu_usage}%',
            'used_memory': memory_usage_percentage,
            'total_memory': total_memory,
            'free_memory': total_memory - used_memory,
            'network_stats': network_stats,
            'used_disk': percent_used_disk,
            'total_disk': total_disk,
            'free_disk': free_disk
            }  
            print(vm_info)

        except Exception as e:
            print(f"Error: {e}")
            vm_info = {
                'id': vm['id'],
                'cpu_usage': 'VM impossible à joindre',
                'total_memory': 'VM impossible à joindre',
                'used_memory': 'VM impossible à joindre',
                'free_memory': 'VM impossible à joindre',
                'network_stats': 'VM impossible à joindre',
                'total_disk': 'VM impossible à joindre',
                'used_disk': 'VM impossible à joindre',
                'free_disk': 'VM impossible à joindre'
            }

        vm_infos.append(vm_info)

    # Affichage du tableau de bord avec des informations détaillées sur les machines virtuelles
    return render_template('tableau_de_bord.html', machines_virtuelles=vm_infos)

if __name__ == '__main__':
    app.run(debug=True)
