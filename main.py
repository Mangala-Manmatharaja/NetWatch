import subprocess
import sqlite3
import time
from datetime import datetime
import schedule  # pip install schedule
import platform

DB_NAME = 'network_monitor.db'


# --- Functions (setup_database, check_host_ping, store_ping_data) remain the same as the previous corrected version ---
def setup_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ping_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            host TEXT,
            status TEXT,
            latency REAL
        )
    ''')
    conn.commit()
    conn.close()


def check_host_ping(host):
    try:
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        timeout_param_flag = '-w' if platform.system().lower() == 'windows' else '-W'
        timeout_value = '1000' if platform.system().lower() == 'windows' else '1'

        command = ['ping', param, '1', timeout_param_flag, timeout_value, host]

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(timeout=5)

        if process.returncode == 0:
            status = "UP"
            latency = None
            try:
                output_str = stdout.decode('utf-8', errors='ignore')
                if platform.system().lower() == 'windows':
                    if "Average =" in output_str:
                        latency_str = output_str.split("Average =")[1].split("ms")[0].strip()
                        latency = float(latency_str)
                    elif "time=" in output_str:
                        latency_str = output_str.split("time=")[-1].split("ms")[0].strip()
                        latency = float(latency_str)
                else:
                    if "time=" in output_str:
                        latency_str = output_str.split("time=")[1].split(" ")[0].strip()
                        latency = float(latency_str)
            except Exception:
                latency = None
            return status, latency
        else:
            return "DOWN", None
    except subprocess.TimeoutExpired:
        return "TIMEOUT", None
    except FileNotFoundError:
        print(f"Error: 'ping' command not found. Is it in your system's PATH?")
        return "ERROR_CMD_NOT_FOUND", None
    except Exception as e:
        print(f"Error pinging {host}: {type(e)._name_} - {e}")
        return "ERROR", None


def store_ping_data(host, status, latency):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    timestamp = datetime.now()
    cursor.execute('''
        INSERT INTO ping_data (timestamp, host, status, latency)
        VALUES (?, ?, ?, ?)
    ''', (timestamp, host, status, latency))
    conn.commit()
    conn.close()
    latency_display = f"{latency:.2f}" if latency is not None else 'N/A'
    print(f"{timestamp} - Host: {host}, Status: {status}, Latency: {latency_display} ms")


# --- End of unchanged functions ---

def job(target_hosts_list):  # Modified job to accept the list of hosts
    print(f"\n--- Running check at {datetime.now()} ---")
    if not target_hosts_list:
        print("No target hosts configured.")
        return

    for host in target_hosts_list:
        host = host.strip()  # Remove any leading/trailing whitespace
        if host:  # Ensure host string is not empty
            status, latency = check_host_ping(host)
            store_ping_data(host, status, latency)


if __name__ == "_main_":
    setup_database()

    # Get target hosts from user
    hosts_input_str = input("Enter target hosts to monitor (comma-separated, e.g., 8.8.8.8, google.com, 1.1.1.1): ")
    target_hosts = [h.strip() for h in hosts_input_str.split(',') if h.strip()]

    if not target_hosts:
        print("No valid target hosts entered. Exiting.")
        exit()

    # Get check interval from user
    while True:
        try:
            interval_minutes = int(input("Enter check interval in minutes (e.g., 1, 5, 10): "))
            if interval_minutes > 0:
                break
            else:
                print("Interval must be a positive number.")
        except ValueError:
            print("Invalid input. Please enter a number for the interval.")

    print(f"\nStarting network monitor for hosts: {', '.join(target_hosts)}")
    print(f"Checks will run every {interval_minutes} minute(s). Press Ctrl+C to exit.")

    # Pass the list of hosts to the job function
    # schedule.every(interval_minutes).minutes.do(job, target_hosts_list=target_hosts)
    # For more direct control and immediate first run:

    # Run the job once immediately
    job(target_hosts_list=target_hosts)

    # Schedule future jobs
    schedule.every(interval_minutes).minutes.do(job, target_hosts_list=target_hosts)

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting network monitor.")