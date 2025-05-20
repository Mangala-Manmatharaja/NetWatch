# 🌐 NetWatch: Lightweight Network Monitoring & Alerting System 📊

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
<!-- Add more badges if you like, e.g., for build status if you set up CI/CD -->

NetWatch is a simple yet effective Python-based tool designed to monitor the health and basic performance of specified network devices and services. It stores collected data, provides basic alerting, and is intended to be extensible. This project was developed as a learning exercise to explore network programming, data storage, and scheduling in Python.

---

## ✨ Features

*   **🎯 Multi-Host Monitoring:** Monitor multiple hosts (IP addresses or domain names) simultaneously.
*   **📈 ICMP Ping Checks:**
    *   Checks host reachability using ICMP pings.
    *   Measures and records round-trip latency.
*   **🖥️ Cross-Platform:** Ping commands adjusted for Windows, Linux, and macOS.
*   **💾 Data Persistence:**
    *   Stores monitoring data (timestamp, host, status, latency) in an SQLite database (`network_monitor.db`).
*   **⚙️ User-Configurable:**
    *   Allows users to specify target hosts at runtime.
    *   Allows users to set the monitoring interval.
*   **⏲️ Scheduled Checks:** Uses the `schedule` library to perform checks at regular intervals.
*   **📝 Console Logging:** Outputs status and results to the console.
*   **💡 Extensible Design:** (Future goals - see "Future Enhancements" section)
    *   Planned support for TCP port checks.
    *   Planned support for basic HTTP health checks.
    *   Planned basic email alerting.
    *   Planned simple web dashboard for visualization.

---

## 🛠️ Technologies Used

*   **🐍 Python 3.7+**
*   **📦 Libraries:**
    *   `subprocess`: For executing external commands (ping).
    *   `sqlite3`: For database interaction.
    *   `schedule`: For task scheduling.
    *   `platform`: To determine OS for platform-specific commands.
    *   `datetime`, `time`: For time-related operations.
*   **🛢️ Database:** SQLite

---

## 🚀 Getting Started

### Prerequisites

*   Python 3.7 or higher installed on your system.
*   `pip` (Python package installer).
*   The `ping` utility must be available in your system's PATH.

### Installation & Setup

1.  **Clone the repository (or download the script):**
    ```bash
    git clone https://github.com/YOUR_USERNAME/NetWatch.git 
    # Or your project's repository URL
    cd NetWatch
    ```

2.  **Install dependencies:**
    Currently, NetWatch uses the `schedule` library, which needs to be installed.
    ```bash
    pip install schedule
    # If you plan to create a requirements.txt:
    # pip install -r requirements.txt 
    ```
    *(Optional: Consider creating a `requirements.txt` file for easier dependency management: `pip freeze > requirements.txt`)*

3.  **Run the script:**
    ```bash
    python netwatch_monitor.py 
    # Or whatever you name your main script file
    ```

### Usage

Upon running the script, you will be prompted to:

1.  **Enter target hosts:**
    Provide a comma-separated list of IP addresses or domain names you want to monitor.
    ```
    Enter target hosts to monitor (comma-separated, e.g., 8.8.8.8, google.com, 1.1.1.1): 8.8.8.8,google.com
    ```

2.  **Enter check interval:**
    Specify how often (in minutes) the checks should be performed.
    ```
    Enter check interval in minutes (e.g., 1, 5, 10): 1
    ```

The monitor will then start, performing an initial check and then subsequent checks at the specified interval. Monitoring data will be logged to the console and stored in `network_monitor.db`.

Press `Ctrl+C` to stop the monitor.

---
