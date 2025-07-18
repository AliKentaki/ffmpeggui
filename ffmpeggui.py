import os
import subprocess
from tkinter import filedialog
import customtkinter as ctk

ctk.set_default_color_theme("blue")
ctk.set_appearance_mode("System")

DEFAULT_FONT = ("Roboto", 14)
WELCOME_TEXT = (
    "Hier werden die zu komprimierenden Dateien aufgelistet.\n"
    "Klicke auf 'Dateien auswählen' um Videos auszuwählen."
)


class UploadFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.counter = 1
        self.filepaths = []

        self.configure(fg_color="transparent")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.btn_select_files = ctk.CTkButton(
            self, text="Dateien auswählen",
            command=self.on_select_files,
            font=ctk.CTkFont(*DEFAULT_FONT)
        )
        self.btn_select_files.grid(row=0, column=0, columnspan=2, pady=5, sticky="ne")

        self.btn_clear = ctk.CTkButton(
            self, text="Liste leeren",
            command=self.on_clear_files,
            font=ctk.CTkFont(*DEFAULT_FONT)
        )
        self.btn_clear.grid(row=0, column=0, columnspan=2, pady=5, sticky="w")

        self.selected_files_box = ctk.CTkTextbox(
            self, bg_color="gray", state="normal",
            wrap="word", corner_radius=6,
            font=ctk.CTkFont(*DEFAULT_FONT)
        )
        self.selected_files_box.insert("end", WELCOME_TEXT)
        self.selected_files_box.configure(state="disabled")
        self.selected_files_box.grid(row=1, column=0, columnspan=2, pady=10, sticky="nswe")

        self.btn_close = ctk.CTkButton(
            self, text="Schließen",
            command=self.master.destroy,
            font=ctk.CTkFont(*DEFAULT_FONT)
        )
        self.btn_close.grid(row=2, column=1, pady=5, sticky="e")

        crf_values = ["CRF-Wert wählen (niedriger = bessere Qualität)"] + [str(x) for x in range(20, 35, 2)] + ["Selbst auswählen"]
        self.btn_compressionrate = ctk.CTkOptionMenu(
            self, values=crf_values,
            command=self.on_custom_crf,
            font=ctk.CTkFont(*DEFAULT_FONT)
        )
        self.btn_compressionrate.grid(row=2, column=0, pady=5, sticky="w")

    def on_custom_crf(self, selection):
        if selection == "Selbst auswählen":
            dialog = ctk.CTkInputDialog(
                text="Gebe einen CRF-Wert ein (max. 40)",
                title="Eigene Auswahl"
            )
            crf = dialog.get_input()
            if crf:
                values = list(self.btn_compressionrate.cget("values"))
                values.insert(-1, crf)
                self.btn_compressionrate.configure(values=values)
                self.btn_compressionrate.set(crf)

    def on_clear_files(self):
        self.selected_files_box.configure(state="normal")
        self.selected_files_box.delete("1.0", "end")
        self.selected_files_box.insert("end", WELCOME_TEXT)
        self.selected_files_box.configure(state="disabled")
        self.counter = 1
        self.filepaths.clear()

    def on_select_files(self):
        paths = filedialog.askopenfilenames(
            initialdir="/",
            title="Dateien auswählen",
            filetypes=[("Video files", "*.mp4")]
        )
        self.selected_files_box.configure(state="normal")
        self.selected_files_box.delete("1.0", "end")

        for i, path in enumerate(paths, self.counter):
            self.filepaths.append(path)
            filename = os.path.basename(path)
            self.selected_files_box.insert("end", f"{i}. {filename}\n")
            self.counter += 1

        self.selected_files_box.configure(state="disabled")


class ConsoleFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="transparent")

        self.console_output = ctk.CTkTextbox(
            self,
            bg_color="#2b2b2b",
            fg_color="#2b2b2b",
            text_color="#ffffff",
            state="disabled",
            wrap="word",
            corner_radius=6,
            font=ctk.CTkFont("Roboto Mono", 12)
        )
        self.console_output.grid(row=0, column=0, pady=5, sticky="nsew")

        self.progress_bar = ctk.CTkProgressBar(
            self,
            height=20,
            corner_radius=10
        )
        self.progress_bar.set(0)
        self.progress_bar.grid(row=1, column=0, pady=5, sticky="ew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


class ButtonFrame(ctk.CTkFrame):
    def __init__(self, master, font_style):
        super().__init__(master)
        self.configure(fg_color="transparent")
        self.process = None

        self.btn_compress = ctk.CTkButton(
            self, text="Starten",
            command=self.ffmpeg_start,
            font=font_style,
            fg_color="#4db8ff",
            hover_color="#3399cc"
        )
        self.btn_compress.grid(row=1, column=0, pady=5, sticky="w")

        self.btn_stop = ctk.CTkButton(
            self, text="Prozess stoppen",
            command=self.stop_process,
            font=font_style,
            fg_color="#ff595e",
            hover_color="#ff3030"
        )
        self.btn_stop.grid(row=1, column=0, padx=(150, 0), pady=5, sticky="w")

    def ffmpeg_start(self):
        self.process = subprocess.Popen(
            ["ffmpeg", "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("ffmpeg gestartet")

    def stop_process(self):
        if self.process:
            self.process.terminate()
            print("Prozess gestoppt")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ffmpeg GUI")
        self.geometry("1200x600")
        font_style = ctk.CTkFont(*DEFAULT_FONT)

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.console_frame = ConsoleFrame(self)
        self.console_frame.grid(row=0, column=0, padx=10, pady=0, sticky="nswe")

        self.upload_frame = UploadFrame(self)
        self.upload_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=0, sticky="nswe")

        self.button_frame = ButtonFrame(self, font_style)
        self.button_frame.grid(row=1, column=0, padx=10, pady=0, sticky="ew")


if __name__ == "__main__":
    app = App()
    app.mainloop()
