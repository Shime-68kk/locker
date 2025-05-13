
import psutil
import socket
import json
import os

# Các cổng phổ biến của công cụ điều khiển từ xa
REMOTE_PORTS = {
    3389: "Remote Desktop (RDP)",
    5938: "TeamViewer",
    7070: "AnyDesk",
    5931: "UltraVNC",
    4899: "Radmin",
    22: "SSH (possible backdoor)",
    4444: "Reverse Shell (common)",
    5555: "ADB (Android Debug Bridge)"
}

def check_open_connections():
    suspicious_connections = []
    for conn in psutil.net_connections(kind='inet'):
        if conn.status == 'ESTABLISHED' and conn.raddr:
            remote_ip, remote_port = conn.raddr
            local_port = conn.laddr.port
            proc_info = {}
            try:
                proc = psutil.Process(conn.pid)
                proc_info = {
                    "pid": conn.pid,
                    "name": proc.name(),
                    "exe": proc.exe(),
                    "cmdline": proc.cmdline()
                }
            except Exception:
                proc_info = {"pid": conn.pid, "name": "Unknown"}

            description = REMOTE_PORTS.get(remote_port, "Unknown or Uncommon Port")
            suspicious_connections.append({
                "local_port": local_port,
                "remote_ip": remote_ip,
                "remote_port": remote_port,
                "description": description,
                "process": proc_info
            })
    return suspicious_connections

def save_report(data, filename="unauthorized_access_report.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    return os.path.abspath(filename)

if __name__ == "__main__":
    print("🔍 Đang quét kết nối mạng...")
    result = check_open_connections()
    if result:
        print(f"⚠️ Phát hiện {len(result)} kết nối nghi ngờ:")
        for conn in result:
            print(f"- {conn['remote_ip']}:{conn['remote_port']} ({conn['description']}) | PID: {conn['process']['pid']}")
    else:
        print("✅ Không phát hiện kết nối trái phép nào.")
    
    report_path = save_report(result)
    print(f"📄 Báo cáo đã lưu tại: {report_path}")
