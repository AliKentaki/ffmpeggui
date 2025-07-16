import customtkinter as ctk
from tkinter import filedialog
import os

# --- Fileselect
class UploadFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.file_select = ctk.CTkButton(
            self,
            text="Dateien auswählen",
            command=self.fileselect
            )

        self.selected_files = ctk.CTkTextbox(
            self,
            bg_color="gray",
            state="disabled",
            wrap="word",
            corner_radius=0,
            )

        self.btn_close = ctk.CTkButton(
            self,
            text="Schließen",
            command=self.close
            )        
        
        self.file_select.grid(row=0, column=0, pady=10, sticky="ne")

        self.selected_files.grid(row=1, column=0, pady=10, sticky="nswe")

        self.btn_close.grid(row=2, column=0, pady=5, sticky="se")

    def close(self):
        self.master.destroy()


    def fileselect(self):
        filepath = filedialog.askopenfilenames(
            initialdir= "/",
            title = "Dateien auswählen",
            filetypes = [("Video files", "*.mp4*")])
        
        self.selected_files.configure(state="normal")


        for i, filepath in enumerate(filepath, start=1):
            filename = os.path.basename(filepath)
            self.selected_files.insert("end", f"{i}. {filename}\n")
        
        self.selected_files.configure(state="disabled")

# --- Console & Progressbar
class ConsoleFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

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
    def __init__(self, master):
        super().__init__(master)

        self.btn_compress = ctk.CTkButton(self, text="Starten", command=self.compress)
        self.btn_compress.grid(row=1, column=0, pady=5, sticky="w")

        self.btn_stop = ctk.CTkButton(self, text="Prozess stoppen", command=self.stop_process)
        self.btn_stop.grid(row=1, column=0, padx=(150,0), pady=5, sticky="w")



        # self.grid_columnconfigure((0, 1), weight=1)

    def compress(self):
        print("compress")

    def stop_process(self):
        print("stop process")

# --- Main App Window
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ffmpeg GUI")
        self.geometry("800x500")

        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Upload rechts
        self.upload_frame = UploadFrame(self)
        self.upload_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=0, sticky="nswe")

        # Konsole links
        self.console_frame = ConsoleFrame(self)
        self.console_frame.grid(row=0, column=0, padx=10, pady=0, sticky="nswe")

        # Buttons unten
        self.button_frame = ButtonFrame(self)
        self.button_frame.grid(row=1, column=0, padx=10, pady=0, sticky="ew")


# --- Run App 
if __name__ == "__main__":
    app = App()
    app.mainloop()
