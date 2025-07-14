import customtkinter as ctk

# ─── Upload Section ────────────────────────────────────────────────
class UploadFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.file_entry = ctk.CTkEntry(self, width=500, placeholder_text="Pfad zur Datei")
        self.file_entry.grid(row=0, column=0, pady=10, sticky="ew")

        self.upload_button = ctk.CTkButton(self, text="Datei auswählen")
        self.upload_button.grid(row=0, column=1, padx=10, pady=10, sticky="ne")


# ─── Console & Progress Section ─────────────────────────────────────
class ConsoleFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.console_output = ctk.CTkScrollableFrame(
            self, bg_color="white", fg_color="black", corner_radius=0, height=300, width=400
        )
        self.console_output.grid(row=0, column=0, pady=5, sticky="nsew")

        self.progress_bar = ctk.CTkProgressBar(self, height=30, corner_radius=0)
        self.progress_bar.grid(row=1, column=0, pady=5, sticky="ew")

        self.grid_rowconfigure(0, weight=1)


# ─── Button Section ────────────────────────────────────────────────
class ButtonFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.btn_compress = ctk.CTkButton(self, text="Compress", command=self.compress)
        self.btn_compress.grid(row=1, column=0, padx=0, pady=20, sticky="sw")

        self.btn_stop = ctk.CTkButton(self, text="Stop process", command=self.stop_process)
        self.btn_stop.grid(row=1, column=1, padx=0, pady=20, sticky="sw")

        self.btn_close = ctk.CTkButton(self, text="Close", command=self.close)
        self.btn_close.grid(row=1, column=2, padx=20, pady=20, sticky="se")


        self.grid_columnconfigure((0, 1, 2), weight=1)

    def compress(self):
        print("compress")

    def stop_process(self):
        print("stop process")

    def close(self):
        self.master.destroy()


# ─── Main App Window ───────────────────────────────────────────────
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ffmpeg GUI")
        self.geometry("800x500")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Upload oben
        self.upload_frame = UploadFrame(self)
        self.upload_frame.grid(row=0, column=0, padx=20, pady=0, sticky="nwe")

        # Console mittig
        self.console_frame = ConsoleFrame(self)
        self.console_frame.grid(row=1, column=0, padx=20, pady=0, sticky="nsew")

        # Buttons unten
        self.button_frame = ButtonFrame(self)
        self.button_frame.grid(row=2, column=0, padx=20, pady=0, sticky="ew")


# ─── Run App ───────────────────────────────────────────────────
if __name__ == "__main__":
    app = App()
    app.mainloop()
