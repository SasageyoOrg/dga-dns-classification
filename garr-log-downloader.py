"""
@brief  : Python program to download log data from GARR server
@authors: Conti Edoardo, Federici Lorenzo, Melnic Andrian
@sourse : Advanced Cybersecurity for IT @ UNIVPM (2022/2023)
"""

import random
import calendar
import argparse
import paramiko
from paramiko.ssh_exception import SSHException
from argparse_range import range_action
from random import randint
from scp import SCPClient, SCPException

"""
Create an SSH connection to the server.
"""
def create_ssh_client(server_addr, port_number, username, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server_addr, port_number, username, password)

    return client

"""
Use the SCP command to download log files.
"""
def download_logs(server_addr, port_number, username, password, mpy, dpm, hpd, year, download_path):
    ssh = create_ssh_client(server_addr, port_number, username, password)
    scp = SCPClient(ssh.get_transport(), sanitize=lambda x: x)

    # check the values of 'dpm' (days per month), 'hpd' (hours per day) and 'mpy' (months per year)
    if not 1 <= mpy <= 12 or not 1 <= dpm <= 31 or not 1 <= hpd <= 24:
        raise ValueError("Invalid value(s) provided.")

    # calendar module used to get the correct number of days for the selected month
    # zfill method to add a zero in front of single digit numbers
    logs = []
    for month in sorted(random.sample(range(1, 13), k=mpy)):
        num_days = calendar.monthrange(int(year), month)[1]
        days = [random.randint(1, num_days) for i in range(dpm)]
        month = str(month).zfill(2)
        for day in days:
            day = str(day).zfill(2)
            random_hours = random.sample(range(0, 24), k=hpd)
            for hour in random_hours:
                hour = str(hour).zfill(2)
                date = f"{year}_{month}_{day}_{hour}"
                logs.append(date)
    
    for log in logs:
        scp.close()
        try:
            print(f'downloading log [{log}]...')
            scp.get(f'VOL250GB/pdns_{log}*', download_path)
        except SCPException as e:
            print(f'log [{log}] do not exist.')

    ssh.close()
    scp.close()

"""
Handles command line arguments and starts downloading log files.
"""
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip-addr', type=str)
    parser.add_argument('--port', type=int)
    parser.add_argument('--username', type=str)
    parser.add_argument('--password', type=str)
    parser.add_argument('--mpy', type=int)
    parser.add_argument('--dpm', type=int)
    parser.add_argument('--hpd', type=int)
    parser.add_argument('--year', type=str)
    parser.add_argument('--download-path', type=str)
    args = parser.parse_args()
    
    download_logs(args.ip_addr, args.port, args.username, args.password, args.mpy, args.dpm, args.hpd, args.year, args.download_path)

if __name__ == '__main__':
    main()