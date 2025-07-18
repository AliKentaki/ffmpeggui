import os
import subprocess
import threading
import json
import logging
from tkinter import filedialog
import customtkinter as ctk
from CustomTkinterMessagebox import CTkMessagebox
import re


# Logging (statt print)
logging.basicConfig(level=logging.INFO)

# Design-Konstanten
ctk.set_default_color_theme("blue")
ctk.set_appearance_mode("System")

DEFAULT_FONT = ("Roboto", 14)
FONT_MONO = ("Roboto Mono", 12)

COLOR_BUTTON_ACTIVE = "#DD9A38"
COLOR_BUTTON_HOVER = "#E1B845"
COLOR_BUTTON_PASSIVE = "#C2BFC3"
COLOR_BUTTON_HOVER_PASSIVE = "#6C6875"
COLOR_BACKGROUND = "#C2BFC3"
COLOR_CONSOLE_BG = "#3E3947"
COLOR_CONSOLE_TEXT = "#FFFFFF"
COLOR_TEXT_DARK = "#000000"
TEXTBOX_BG = "#3E3947"
TEXTBOX_FG = "#FFFFFF"

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
            font=ctk.CTkFont(*DEFAULT_FONT),
            fg_color=COLOR_BUTTON_ACTIVE,
            hover_color=COLOR_BUTTON_HOVER
        )
        self.btn_select_files.grid(row=0, column=0, columnspan=2, pady=5, sticky="ne")

        self.btn_clear = ctk.CTkButton(
            self, text="Liste leeren",
            command=self.on_clear_files,
            font=ctk.CTkFont(*DEFAULT_FONT),
            fg_color=COLOR_BUTTON_PASSIVE,
            hover_color=COLOR_BUTTON_HOVER_PASSIVE,
            text_color=COLOR_TEXT_DARK
        )
        self.btn_clear.grid(row=0, column=0, columnspan=2, pady=5, sticky="w")

        self.selected_files_box = self.create_textbox()
        self.selected_files_box.insert("end", WELCOME_TEXT)
        self.selected_files_box.tag_config("welcome", foreground=TEXTBOX_FG)
        self.selected_files_box.configure(state="disabled")
        self.selected_files_box.grid(row=1, column=0, pady=10, sticky="nswe")

        self.videostats_box = self.create_textbox()
        self.videostats_box.configure(state="disabled")
        self.videostats_box.grid(row=1, column=1, padx=0, pady=10, sticky="nswe")

        self.btn_close = ctk.CTkButton(
            self, text="Schließen",
            command=self.master.destroy,
            font=ctk.CTkFont(*DEFAULT_FONT),
            fg_color=COLOR_BUTTON_PASSIVE,
            hover_color=COLOR_BUTTON_HOVER_PASSIVE,
            text_color=COLOR_TEXT_DARK
        )
        self.btn_close.grid(row=2, column=1, pady=5, sticky="e")

        crf_values = ["CRF-Wert wählen (niedriger = bessere Qualität)"] + [str(x) for x in range(20, 35, 2)] + ["Selbst auswählen"]
        self.btn_compressionrate = ctk.CTkOptionMenu(
            self, values=crf_values,
            command=self.on_custom_crf,
            font=ctk.CTkFont(*DEFAULT_FONT),
            fg_color=COLOR_BUTTON_PASSIVE,
            button_color=COLOR_BUTTON_PASSIVE,
            button_hover_color=COLOR_BUTTON_HOVER_PASSIVE,
            text_color=COLOR_TEXT_DARK
        )
        self.btn_compressionrate.grid(row=2, column=0, pady=5, sticky="w")

    def create_textbox(self):
        return ctk.CTkTextbox(
            self,
            bg_color=TEXTBOX_BG,
            state="normal",
            wrap="word",
            corner_radius=0,
            font=ctk.CTkFont(*DEFAULT_FONT)
        )

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
        self.videostats_box.configure(state="normal")
        self.videostats_box.delete("1.0", "end")
        self.selected_files_box.delete("1.0", "end")
        self.selected_files_box.insert("end", WELCOME_TEXT, "welcome")
        self.selected_files_box.tag_config("welcome", foreground=TEXTBOX_FG)
        self.selected_files_box.configure(state="disabled")
        self.videostats_box.configure(state="disabled")
        self.counter = 1
        self.filepaths.clear()

    def on_select_files(self):
        text = self.selected_files_box.get("1.0", "end-1c")
        paths = filedialog.askopenfilenames(
            initialdir="/",
            title="Dateien auswählen",
            filetypes=[("Video files", "*.mp4")]
        )
        self.selected_files_box.configure(state="normal")
        self.videostats_box.configure(state="normal")

        if text.strip() == WELCOME_TEXT.strip() and paths:
            self.selected_files_box.delete("1.0", "end")

        for i, path in enumerate(paths, self.counter):
            self.filepaths.append(path)
            filename = os.path.basename(path)
            duration, size, seconds = self.get_video_info(path)
            self.selected_files_box.insert(f"{i}.0", f"{i}. ▶ {filename}\n")
            self.videostats_box.insert(f"{i}.0", f"{duration:<10} {size}\n")
            self.counter += 1

        self.selected_files_box.configure(state="disabled")
        self.videostats_box.configure(state="disabled")

    def get_video_info(self, file):
        # Dauer
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", file],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        seconds = float(json.loads(result.stdout)["format"]["duration"])
        minutes = int(seconds) // 60
        secs = int(seconds) % 60
        duration = f"{minutes:02d}:{secs:02d}"

        # Größe
        size_bytes = os.path.getsize(file)
        size_mb = size_bytes / (1024 * 1024)
        size = f"{size_mb:.2f} MB"

        return duration, size, seconds



class ConsoleFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="transparent")

        self.console_output = ctk.CTkTextbox(
            self,
            bg_color=COLOR_CONSOLE_BG,
            fg_color=COLOR_CONSOLE_BG,
            text_color=COLOR_CONSOLE_TEXT,
            state="disabled",
            wrap="word",
            corner_radius=6,
            font=ctk.CTkFont(*FONT_MONO)
        )
        self.console_output.grid(row=0, column=0, pady=5, sticky="nsew")

        self.progress_bar = ctk.CTkProgressBar(
            self,
            height=20,
            corner_radius=10,
            fg_color="#3E3947",
            progress_color=COLOR_BUTTON_ACTIVE
        )
        self.progress_bar.set(0)
        self.progress_bar.grid(row=1, column=0, pady=5, sticky="ew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


class ButtonFrame(ctk.CTkFrame):
    def __init__(self, master, font_style, console_frame, upload_frame):
        super().__init__(master)
        self.console_frame = console_frame
        self.upload_frame = upload_frame
        self.configure(fg_color="transparent")
        self.process = None

        self.btn_compress = ctk.CTkButton(
            self, text="Starten",
            command=self.ffmpeg_start,
            font=font_style,
            fg_color=COLOR_BUTTON_ACTIVE,
            hover_color=COLOR_BUTTON_HOVER
        )
        self.btn_compress.grid(row=1, column=0, pady=5, sticky="w")

        self.btn_stop = ctk.CTkButton(
            self, text="Prozess stoppen",
            command=self.stop_process,
            font=font_style,
            fg_color="red",
            hover_color="darkred"
        )
        self.btn_stop.grid(row=1, column=0, padx=(150, 0), pady=5, sticky="w")

    def ffmpeg_start(self):
        crf, files = self._validate_ffmpeg_input()
        if not crf:
            return
        threading.Thread(target=self._process_files, args=(crf, files), daemon=True).start()

    def _validate_ffmpeg_input(self):
        crf = self.upload_frame.btn_compressionrate.get()
        files = self.upload_frame.filepaths

        if crf == "CRF-Wert wählen (niedriger = bessere Qualität)":
            CTkMessagebox.messagebox(title="Fehler", text="Bitte CRF-Wert auswählen.") # type: ignore
            return None, None
        if not files:
            CTkMessagebox.messagebox(title="Fehler", text="Keine Dateien ausgewählt.") # type: ignore
            return None, None
        return crf, files

    def get_fps(self, file):
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=r_frame_rate", "-of", "default=noprint_wrappers=1:nokey=1", file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        fps_str = result.stdout.strip()
        if "/" in fps_str:
            num, denom = map(int, fps_str.split("/"))
            return num / denom
        else:
            return float(fps_str)


# anzahl an fps = 1106 = 60 * duration in seconds

    def _process_files(self, crf, files):
        for file in files:
            base, _ = os.path.splitext(str(file))
            output_path = base + "_komprimiert.mp4"

            # fps & duration holen
            _, _, seconds = self.upload_frame.get_video_info(file)
            fps = self.get_fps(file)
            total_frames = int(fps * seconds)

            self.process = subprocess.Popen(
                ["ffmpeg", "-i", str(file), "-vcodec", "libx264", "-crf", crf, output_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if self.process.stderr:
                for line in self.process.stderr:
                    self.console_frame.console_output.after(0, self._insert_console_output, line)

                    match = re.search(r"frame=\s*(\d+)", line)
                    if match:
                        current_frame = int(match.group(1))
                        progress = self.progress_calc(current_frame, total_frames)
                        self.console_frame.progress_bar.set(progress)
            self.process.wait()

        self.upload_frame.filepaths.clear()
        self._insert_console_output("Verarbeitung abgeschlossen.\n")


    
    def progress_calc(self, current_frame, total_frames):
        progress = current_frame / total_frames
        return round(progress, 2)





    def _insert_console_output(self, text):
        box = self.console_frame.console_output
        box.configure(state="normal")
        box.insert("end", text)
        box.see("end")
        box.configure(state="disabled")

    def stop_process(self):
        if self.process:
            self.process.terminate()
            self._insert_console_output("Prozess gestoppt\n")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ffmpeg GUI")
        self.geometry("1200x600")
        self.configure(bg_color=COLOR_BACKGROUND)
        font_style = ctk.CTkFont(*DEFAULT_FONT)

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.console_frame = ConsoleFrame(self)
        self.console_frame.grid(row=0, column=0, padx=10, pady=0, sticky="nswe")

        self.upload_frame = UploadFrame(self)
        self.upload_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=0, sticky="nswe")

        self.button_frame = ButtonFrame(self, font_style, self.console_frame, self.upload_frame)
        self.button_frame.grid(row=1, column=0, padx=10, pady=0, sticky="ew")


if __name__ == "__main__":
    app = App()
    app.mainloop()
