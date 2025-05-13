
import psutil
import os
import platform
import ctypes
import subprocess
import socket

SUSPICIOUS_PORTS = [22, 3389, 4444, 5555, 5938, 7070, 12345]
ALERT_PROCESSES = ["netcat", "ncat", "telnet", "ngrok", "teamviewer", "anydesk", "rdpwrap", "reverse_shell"]

def detect_suspicious_connections():
    alerts = []
    for conn in psutil.net_connections(kind="inet"):
        if conn.status == "ESTABLISHED" and conn.raddr:
            remote_ip, remote_port = conn.raddr
            if remote_port in SUSPICIOUS_PORTS:
                alerts.append({
                    "remote_ip": remote_ip,
                    "remote_port": remote_port,
                    "local_port": conn.laddr.port,
                    "pid": conn.pid
                })
    return alerts

def detect_suspicious_processes():
    suspicious = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            for name in ALERT_PROCESSES:
                if name in ' '.join(proc.info['cmdline']).lower():
                    suspicious.append(proc.info)
        except Exception:
            continue
    return suspicious

def lock_workstation():
    if platform.system() == "Windows":
        ctypes.windll.user32.LockWorkStation()
    elif platform.system() == "Linux":
        subprocess.call(["gnome-screensaver-command", "-l"])
    else:
        print("Lock not supported on this OS")

def main():
    print("🔍 Đang quét hệ thống phát hiện xâm nhập...")
    conn_alerts = detect_suspicious_connections()
    proc_alerts = detect_suspicious_processes()

    if conn_alerts or proc_alerts:
        print("⚠️ PHÁT HIỆN DẤU HIỆU BỊ XÂM NHẬP!")
        if conn_alerts:
            print("📡 Kết nối nghi ngờ:")
            for alert in conn_alerts:
                print(f"- IP: {alert['remote_ip']} | Cổng: {alert['remote_port']} | PID: {alert['pid']}")
        if proc_alerts:
            print("⚙️ Tiến trình nghi ngờ:")
            for proc in proc_alerts:
                print(f"- PID: {proc['pid']} | Lệnh: {' '.join(proc['cmdline'])}")
        print("🔒 Đang khóa tạm thời máy tính...")
        lock_workstation()
    else:
        print("✅ Không phát hiện hoạt động xâm nhập bất thường.")

if __name__ == "__main__":
    main()
