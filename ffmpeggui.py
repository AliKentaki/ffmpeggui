import customtkinter as ctk

class UploadFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.uploadfield = ctk.CTkEntry(self, width=500, placeholder_text="Pfad zur Datei")
        self.uploadfield.grid(row=0, column=0, pady=10, sticky="ew")
        self.uploadfield.grid_columnconfigure(0, weight=1)

        self.uploadbutton = ctk.CTkButton(self, text="Datei auswählen")
        self.uploadbutton.grid(row=0, column=1, padx=10, pady=10, sticky="ne")



class ConsoleFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.progressbar = ctk.CTkProgressBar(self, width=400 ,height=30, corner_radius=0)
        self.progressbar.grid(row=1, column=0, pady=5, sticky="swe")

        self.console = ctk.CTkScrollableFrame(self, bg_color="white", fg_color="black", corner_radius=0, height=300)
        # muss in eigene Frame
        self.console.grid(row=0, column=0, pady=5, sticky="Nswe")
        self.console.grid_rowconfigure(0, weight=1)
        


class ProcessFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.button = ctk.CTkButton(self, text="Compress", command=self.compress)
        self.button.grid(row=1, column=0, padx=0, pady=20, sticky="swe")
        self.button = ctk.CTkButton(self, text="Stop process", command=self.stop_process)
        self.button.grid(row=1, column=1, padx=10, pady=20, sticky="swe")
    

    def compress(self):
        # app.compress()
        print("compress")
    
    def stop_process(self):
        # app.stoprocess()
        print("stop process")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ffmpeg GUI")
        self.geometry("800x500")

        # (1, weight=1) -> Spalte 1 erhält Gewicht und darf "wachsen"
        # bei (2, weight=2) -> Spalte 2 erhält GEwicht und darf auch "wachsen", da weight = 2 -> wächst doppelt so viel wie Spalte 1 (weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)


        # Frame links, breitet sich vertikal aus
        self.button_frame = ProcessFrame(self)
        self.button_frame.grid(row=2, column=0, padx=20, pady=0, sticky="ws")
        self.button_frame.grid_columnconfigure((0,1), weight=1)

        self.console_frame = ConsoleFrame(self)
        self.console_frame.grid(row=1, column=0, padx=20, pady=0, sticky="snw")
        self.console_frame.grid_rowconfigure(0, weight=1)
        # self.console_frame.configure(fg_color="transparent")
        
        self.upload_frame = UploadFrame(self)
        self.upload_frame.grid(row=0, column=0, padx=20, pady=0, sticky="nwe")



        self.button = ctk.CTkButton(self, text="Close", command=self.close)
        self.button.grid(row=1, column=1, padx=20, pady=20, sticky="se")


    def close(self):
        app.destroy()

app = App()
app.mainloop()