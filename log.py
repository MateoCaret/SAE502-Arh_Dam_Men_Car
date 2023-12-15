import paramiko
import csv
import time
from datetime import datetime, timedelta

def ssh_connect(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password)
    return client

def retrieve_logs(ssh_client, remote_log_path):
    _, stdout, _ = ssh_client.exec_command(f"cat {remote_log_path}")
    logs = stdout.read().decode('utf-8')
    return logs

def save_to_csv(logs, filename):
    with open(filename, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), logs])

def main():
    hostname = 'your_remote_host'
    username = 'your_username'
    password = 'your_password'
    remote_log_path = '/path/to/remote/log/file.log'

    ssh_client = ssh_connect(hostname, username, password)

    while True:
        current_time = datetime.now()
        filename = f"{current_time.strftime('%Y-%m-%d')}_logs.csv"

        logs = retrieve_logs(ssh_client, remote_log_path)
        save_to_csv(logs, filename)

        time.sleep(60)  # Sleep for 60 seconds before the next iteration

if __name__ == "__main__":
    main()
