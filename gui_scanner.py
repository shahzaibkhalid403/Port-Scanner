import socket
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("Professional TCP Port Scanner")
root.geometry("700x550")
root.resizable(False, False)
root.configure(bg="#1e1e1e")

# ---------------- STYLE ----------------
style = ttk.Style()
style.theme_use("clam")

style.configure("TLabel", background="#1e1e1e", foreground="white", font=("Segoe UI", 10))
style.configure("TButton", font=("Segoe UI", 10, "bold"))
style.configure("TEntry", padding=5)

# ---------------- VARIABLES ----------------
open_ports = []
closed_ports = []
scanning = False

# ---------------- FUNCTIONS ----------------
def start_scan():
    global open_ports, closed_ports, scanning

    if scanning:
        return

    target = target_entry.get()
    start_port = start_port_entry.get()
    end_port = end_port_entry.get()

    if not target or not start_port or not end_port:
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        target = socket.gethostbyname(target)
        start_port = int(start_port)
        end_port = int(end_port)
    except:
        messagebox.showerror("Error", "Invalid input!")
        return

    if start_port < 1 or end_port > 65535 or start_port > end_port:
        messagebox.showerror("Error", "Invalid port range!")
        return

    open_ports = []
    closed_ports = []
    result_box.delete(1.0, tk.END)
    progress_bar["value"] = 0
    scanning = True

    total_ports = end_port - start_port + 1

    def scan():
        nonlocal total_ports
        count = 0

        for port in range(start_port, end_port + 1):
            if not scanning:
                break

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((target, port))

            if result == 0:
                open_ports.append(port)
                result_box.insert(tk.END, f"[OPEN]   Port {port}\n")
            else:
                closed_ports.append(port)

            sock.close()

            count += 1
            progress = (count / total_ports) * 100
            progress_bar["value"] = progress
            root.update_idletasks()

        scanning_finished()

    threading.Thread(target=scan, daemon=True).start()


def scanning_finished():
    global scanning
    scanning = False
    result_box.insert(tk.END, "\n============================\n")
    result_box.insert(tk.END, f"Scan Completed at {datetime.now()}\n")
    result_box.insert(tk.END, f"Total Open Ports  : {len(open_ports)}\n")
    result_box.insert(tk.END, f"Total Closed Ports: {len(closed_ports)}\n")
    result_box.insert(tk.END, "============================\n")


def clear_results():
    result_box.delete(1.0, tk.END)
    progress_bar["value"] = 0


# ---------------- UI LAYOUT ----------------

title = tk.Label(root, text="TCP PORT SCANNER BY SHAHZAIB", bg="#1e1e1e",
                 fg="#00ffcc", font=("Segoe UI", 18, "bold"))
title.pack(pady=10)

frame = ttk.Frame(root)
frame.pack(pady=10)

ttk.Label(frame, text="Target (IP / Domain):").grid(row=0, column=0, padx=5, pady=5)
target_entry = ttk.Entry(frame, width=20)
target_entry.insert(0, "127.0.0.1")
target_entry.grid(row=0, column=1, padx=5)

ttk.Label(frame, text="Start Port:").grid(row=1, column=0, padx=5, pady=5)
start_port_entry = ttk.Entry(frame, width=20)
start_port_entry.insert(0, "1")
start_port_entry.grid(row=1, column=1, padx=5)

ttk.Label(frame, text="End Port:").grid(row=2, column=0, padx=5, pady=5)
end_port_entry = ttk.Entry(frame, width=20)
end_port_entry.insert(0, "100")
end_port_entry.grid(row=2, column=1, padx=5)

button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

scan_button = ttk.Button(button_frame, text="Start Scan", command=start_scan)
scan_button.grid(row=0, column=0, padx=10)

clear_button = ttk.Button(button_frame, text="Clear", command=clear_results)
clear_button.grid(row=0, column=1, padx=10)

progress_bar = ttk.Progressbar(root, length=500, mode="determinate")
progress_bar.pack(pady=10)

result_box = tk.Text(root, height=15, width=80, bg="#111111",
                     fg="#00ffcc", font=("Consolas", 10))
result_box.pack(pady=10)

# ---------------- RUN ----------------
root.mainloop()

