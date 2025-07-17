import customtkinter as ctk
from tkinter import filedialog
import threading
import subprocess
import os

ctk.set_default_color_theme("blue")
ctk.set_appearance_mode("System")

# --- Fileselect
class UploadFrame(ctk.CTkFrame):
    def __init__(self, master, font_style):
        super().__init__(master)

        self.counter = 1
        self.filepaths = []
        self.configure(fg_color="transparent")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.file_select = ctk.CTkButton(
            self,
            text="Dateien auswählen",
            command=self.fileselect,
            font = font_style
            )
        self.file_select.grid(row=0, column=0, columnspan=2, pady=5, sticky="ne")

        self.clearbtn = ctk.CTkButton(
            self,
            text="Liste leeren",
            command=self.clear,
            font = font_style
        )
        self.clearbtn.grid(row=0, column=0, columnspan=2, pady=5, sticky="w")


        self.selected_files = ctk.CTkTextbox(
            self,
            bg_color="gray",
            state="normal",
            wrap="word",
            corner_radius=0,
            font = font_style
            )
        self.selected_files.insert("end", "Hier werden die zu komprimierenden Dateien aufgelistet.\nKlicke auf 'Dateien auswählen' um Videos auszuwählen.")
        self.selected_files.configure(state="disabled")
        self.selected_files.grid(row=1, column=0, columnspan=2, pady=10, sticky="nswe")


        self.btn_close = ctk.CTkButton(
            self,
            text="Schließen",
            command=self.close,
            font = font_style
            )
        self.btn_close.grid(row=2, column=1, pady=5, sticky="e")

        
        self.btn_compressionrate = ctk.CTkOptionMenu(
            self,
            values = ["CRF-Wert wählen (niedriger = besser)"] + [str(x) for x in range(20,35, 2)] + ["Selbst auswählen"],
            command=self.custom_check,
            font = font_style
            )
        self.btn_compressionrate.grid(row=2, column=0, pady=5, sticky="w")

    # check für "selbst auswählen"
    def custom_check(self, auswahl):
        werte = list(self.btn_compressionrate.cget("values"))
        if auswahl == "Selbst auswählen":
            self.input = ctk.CTkInputDialog(text = "Gebe einen CRF-Wert ein, je größer der Wert, desto schlechter die Qualität. (Empfohlen höchstens 40)", title = "Eigene Auswahl")
            crf = self.input.get_input()
            if crf is not None:
                werte.insert(-1, crf)
                self.btn_compressionrate.configure(values=werte)
                self.btn_compressionrate.set(crf)


    def clear(self):
        self.selected_files.configure(state="normal")
        self.selected_files.delete("1.0", "end")
        self.selected_files.insert("end", "Hier werden die zu komprimierenden Dateien aufgelistet.\nKlicke auf 'Dateien auswählen' um Videos auszuwählen.")
        self.selected_files.configure(state="disabled")
        self.counter = 1
        self.filepaths = []

    def close(self):
        self.master.destroy()


    def fileselect(self):
        filepath = filedialog.askopenfilenames(
            initialdir= "/",
            title = "Dateien auswählen",
            filetypes = [("Video files", "*.mp4*")])
        self.selected_files.configure(state="normal")
        self.selected_files.delete("1.0", "end")


        for i, filepath in enumerate(filepath, self.counter):
            self.filepaths.append(filepath)
            filename = os.path.basename(filepath)
            self.selected_files.insert("end", f"{i}. {filename}\n")
            self.counter += 1
            
        print(self.filepaths)
        self.selected_files.configure(state="disabled")

# --- Console & Progressbar
class ConsoleFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.configure(fg_color="transparent")
        self.console_output = ctk.CTkTextbox(
            self,
            bg_color="white",
            fg_color="black",
            corner_radius=0,
            text_color="white",
            state="disabled",
            wrap="word"
        )
        self.console_output.grid(row=0, column=0, pady=5, sticky="nsew")

        self.progress_bar = ctk.CTkProgressBar(self, height=30, corner_radius=0)
        self.progress_bar.grid(row=1, column=0, pady=5, sticky="ew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

# --- Buttons
class ButtonFrame(ctk.CTkFrame):
    def __init__(self, master, font_style):
        super().__init__(master)

        self.configure(fg_color="transparent")
        self.btn_compress = ctk.CTkButton(self, text="Starten", command=self.ffmpeg_start, font = font_style)
        self.btn_compress.grid(row=1, column=0, pady=5, sticky="w")

        self.btn_stop = ctk.CTkButton(self, text="Prozess stoppen", command=self.stop_process, font = font_style)
        self.btn_stop.grid(row=1, column=0, padx=(150,0), pady=5, sticky="w")
        
# --- Process Management (ffmpeg)
    def ffmpeg_start(self):
        subprocess.run(["ffmpeg", "-version"])
        print("compress")

    def stop_process(self):
        print("stop process")

# --- Main App Window
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("ffmpeg GUI")
        self.geometry("1200x600")
        self.font_style = ctk.CTkFont(family="Roboto", size=14)

        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Upload rechts
        self.upload_frame = UploadFrame(self, self.font_style)
        self.upload_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=0, sticky="nswe")

        # Konsole links
        self.console_frame = ConsoleFrame(self)
        self.console_frame.grid(row=0, column=0, padx=10, pady=0, sticky="nswe")

        # Buttons unten
        self.button_frame = ButtonFrame(self, self.font_style)
        self.button_frame.grid(row=1, column=0, padx=10, pady=0, sticky="ew")


# --- Run App 
if __name__ == "__main__":
    app = App()
    app.mainloop()
