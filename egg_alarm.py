import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
from playsound import playsound

# Default times (in seconds)
EGG_TIMES = {
    "Soft": 300,  # 5 minutes
    "Medium": 420,  # 7 minutes
    "Hard": 600,  # 10 minutes
}


class EggBoilerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Egg Boiler Tracker")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        self.timer_running = False
        self.remaining_time = 0

        # Egg type selector
        self.egg_type = tk.StringVar(value="Soft")
        ttk.Label(root, text="Choose Egg Type:").pack(pady=10)
        ttk.Combobox(
            root,
            textvariable=self.egg_type,
            values=list(EGG_TIMES.keys()),
            state="readonly",
        ).pack()

        # Custom time entry (optional)
        ttk.Label(root, text="Or enter time (seconds):").pack(pady=10)
        self.custom_time_entry = ttk.Entry(root)
        self.custom_time_entry.pack()

        # Start/Stop button
        self.start_button = ttk.Button(
            root, text="Start Timer", command=self.start_timer
        )
        self.start_button.pack(pady=10)

        self.stop_button = ttk.Button(
            root, text="Stop Timer", command=self.stop_timer, state="disabled"
        )
        self.stop_button.pack()

        # Progress bar
        self.progress = ttk.Progressbar(root, length=300, mode="determinate")
        self.progress.pack(pady=20)

        # Time display
        self.time_label = ttk.Label(root, text="Time Remaining: 00:00")
        self.time_label.pack()

    def start_timer(self):
        if self.timer_running:
            return

        try:
            custom_time = int(self.custom_time_entry.get())
            self.remaining_time = custom_time
        except ValueError:
            egg_choice = self.egg_type.get()
            self.remaining_time = EGG_TIMES.get(egg_choice, 300)

        self.total_time = self.remaining_time
        self.timer_running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")

        threading.Thread(target=self.run_timer).start()

    def run_timer(self):
        while self.remaining_time > 0 and self.timer_running:
            mins, secs = divmod(self.remaining_time, 60)
            self.time_label.config(text=f"Time Remaining: {mins:02}:{secs:02}")
            self.progress["value"] = (
                (self.total_time - self.remaining_time) / self.total_time * 100
            )
            time.sleep(1)
            self.remaining_time -= 1

        if self.timer_running:
            self.time_label.config(text="Boiling complete!")
            self.progress["value"] = 100
            print("\a")
            # playsound("alarm.wav")  # Replace with your alarm file
            messagebox.showinfo("Done!", "Your eggs are ready!")

        self.reset_buttons()

    def stop_timer(self):
        self.timer_running = False
        self.reset_buttons()
        self.time_label.config(text="Timer stopped.")
        self.progress["value"] = 0

    def reset_buttons(self):
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = EggBoilerApp(root)
    root.mainloop()
