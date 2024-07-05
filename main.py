import tkinter as tk
from tkinter import ttk
import psutil
import GPUtil
from threading import Thread
from tkinter import messagebox

class SystemMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Monitor")

        self.metrics = {
            "GPU Temperature": self.get_gpu_temperature,
            "CPU Usage": self.get_cpu_usage,
            "GPU Usage": self.get_gpu_usage,
            "RAM Usage": self.get_ram_usage,
            "Disk Usage": self.get_disk_usage
        }

        self.selected_metrics = list(self.metrics.keys())
        self.create_widgets()
        self.update_metrics()

    def create_widgets(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.metric_labels = []
        for metric in self.selected_metrics:
            label = tk.Label(self.main_frame, text=f"{metric}:")
            label.pack()
            self.metric_labels.append(label)

        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.config_button = tk.Button(button_frame, text="Настроить", command=self.open_config_window)
        self.config_button.pack(side=tk.LEFT, anchor=tk.SW)

        self.info_button = tk.Button(button_frame, text="Информация", command=self.show_info)
        self.info_button.pack(side=tk.RIGHT, anchor=tk.SE)

    def update_metrics(self):
        try:
            for i, metric in enumerate(self.selected_metrics):
                value = self.metrics[metric]()
                self.metric_labels[i].config(text=f"{metric}: {value}")
        except Exception as e:
            pass

        self.root.after(5000, self.update_metrics)  # Update every 5 seconds

    def open_config_window(self):
        config_window = tk.Toplevel(self.root)
        config_window.title("Configure Metrics")

        self.check_vars = {metric: tk.BooleanVar(value=metric in self.selected_metrics) for metric in self.metrics}

        for metric, var in self.check_vars.items():
            check = tk.Checkbutton(config_window, text=metric, variable=var, command=self.update_listbox)
            check.pack(anchor=tk.W)

        # Listbox for reordering
        self.listbox = tk.Listbox(config_window, selectmode=tk.SINGLE)
        for metric in self.selected_metrics:
            self.listbox.insert(tk.END, metric)
        self.listbox.pack()

        move_up_button = tk.Button(config_window, text="Move Up", command=self.move_up)
        move_up_button.pack()

        move_down_button = tk.Button(config_window, text="Move Down", command=self.move_down)
        move_down_button.pack()

        save_button = tk.Button(config_window, text="Save", command=lambda: self.save_config(config_window))
        save_button.pack()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for metric in self.metrics:
            if self.check_vars[metric].get():
                self.listbox.insert(tk.END, metric)

    def save_config(self, config_window):
        self.selected_metrics = [self.listbox.get(idx) for idx in range(self.listbox.size())]

        for label in self.metric_labels:
            label.destroy()

        self.metric_labels = []
        for metric in self.selected_metrics:
            label = tk.Label(self.main_frame, text=f"{metric}:")
            label.pack()
            self.metric_labels.append(label)

        config_window.destroy()

    def move_up(self):
        selected = self.listbox.curselection()
        if selected:
            idx = selected[0]
            if idx > 0:
                item = self.listbox.get(idx)
                self.listbox.delete(idx)
                self.listbox.insert(idx - 1, item)
                self.listbox.selection_set(idx - 1)

    def move_down(self):
        selected = self.listbox.curselection()
        if selected:
            idx = selected[0]
            if idx < self.listbox.size() - 1:
                item = self.listbox.get(idx)
                self.listbox.delete(idx)
                self.listbox.insert(idx + 1, item)
                self.listbox.selection_set(idx + 1)

    def show_info(self):
        messagebox.showinfo("Информация", "Создатель: offach\nКонтакт: me@offach.ru")

    def get_gpu_temperature(self):
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                return f"{gpus[0].temperature}°C"
        except Exception as e:
            return "N/A"
        return "N/A"

    def get_cpu_usage(self):
        return f"{psutil.cpu_percent()}%"

    def get_gpu_usage(self):
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                return f"{gpus[0].load * 100:.1f}%"
        except Exception as e:
            return "N/A"
        return "N/A"

    def get_ram_usage(self):
        return f"{psutil.virtual_memory().percent}%"

    def get_disk_usage(self):
        return f"{psutil.disk_usage('/').percent}%"


if __name__ == "__main__":
    root = tk.Tk()
    app = SystemMonitorApp(root)
    root.mainloop()
