import tkinter as tk
from tkinter import messagebox, ttk
from core.fixer import reset_network_adapter, clear_icon_cache, delete_temp_files, disk_cleanup, run_sfc_scan

class WinFixerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WinFixer")
        self.root.geometry("400x450")
        self.root.resizable(False, False)  # غیرفعال کردن تغییر اندازه پنجره
        self.root.configure(bg="#f0f0f0")  # رنگ پس‌زمینه

        # بررسی دسترسی ادمین
        if not self.is_user_admin():
            messagebox.showerror("Error", "Please run this application as Administrator!")
            self.root.destroy()
            return

        # عنوان برنامه
        title_label = tk.Label(
            root, text="WinFixer", font=("Arial", 20, "bold"),
            bg="#f0f0f0", fg="#333333"
        )
        title_label.pack(pady=20)

        # فریم برای دکمه‌ها
        button_frame = tk.Frame(root, bg="#f0f0f0")
        button_frame.pack(pady=10)

        # استایل برای دکمه‌ها
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=10)

        # دکمه‌ها
        ttk.Button(button_frame, text="Reset Network", command=self.reset_network).pack(fill="x", padx=50, pady=5)
        ttk.Button(button_frame, text="Clear Icon Cache", command=self.clear_icon_cache).pack(fill="x", padx=50, pady=5)
        ttk.Button(button_frame, text="Delete Temp Files", command=self.delete_temp_files).pack(fill="x", padx=50, pady=5)
        ttk.Button(button_frame, text="Disk Cleanup", command=self.disk_cleanup).pack(fill="x", padx=50, pady=5)
        ttk.Button(button_frame, text="Run SFC Scan", command=self.run_sfc_scan).pack(fill="x", padx=50, pady=5)

    def is_user_admin(self):
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def reset_network(self):
        success, restart_required = reset_network_adapter()
        if success and not restart_required:
            messagebox.showinfo("Success", "Network reset completed successfully.")
        elif restart_required:
            messagebox.showinfo("Info", "Please restart your computer to apply the network reset changes.")
        else:
            messagebox.showerror("Error", "Failed to reset network. Check logs for details.")

    def clear_icon_cache(self):
        success, restart_required = clear_icon_cache()
        if success:
            messagebox.showinfo("Success", "Icon cache cleared successfully.")
        else:
            messagebox.showerror("Error", "Failed to clear icon cache. Check logs for details.")

    def delete_temp_files(self):
        success = delete_temp_files()
        if success:
            messagebox.showinfo("Success", "Temporary files deleted successfully.")
        else:
            messagebox.showerror("Error", "Failed to delete temporary files. Check logs for details.")

    def disk_cleanup(self):
        success = disk_cleanup()
        if success:
            messagebox.showinfo("Success", "Disk cleanup completed successfully.")
        else:
            messagebox.showerror("Error", "Disk cleanup failed. Check logs for details.")

    def run_sfc_scan(self):
        success = run_sfc_scan()
        if success:
            messagebox.showinfo("Success", "SFC scan completed successfully.")
        else:
            messagebox.showerror("Error", "SFC scan failed. Check logs for details.")

if __name__ == "__main__":
    root = tk.Tk()
    app = WinFixerApp(root)
    root.mainloop()