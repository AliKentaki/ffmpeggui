import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ffmpeg GUI")
        self.geometry("800x500")

        # (1, weight=1) -> Spalte 1 erhält Gewicht und darf "wachsen"
        # bei (2, weight=2) -> Spalte 2 erhält GEwicht und darf auch "wachsen", da weight = 2 -> wächst doppelt so viel wie Spalte 1 (weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.button = ctk.CTkButton(self, text="Close", command=self.close)
        self.button.grid(row=1, column=2, padx=20, pady=20, sticky="e")
        self.button = ctk.CTkButton(self, text="Compress", command=self.compress)
        self.button.grid(row=1, column=0, padx=20, pady=20, sticky="w")
        self.button = ctk.CTkButton(self, text="Stop process", command=self.stop_process)
        self.button.grid(row=1, column=1, padx=0, pady=20, sticky="w")

    def close(self):
        app.destroy()

    def compress(self):
        # app.compress()
        print("compress")
    
    def stop_process(self):
        # app.stoprocess()
        print("stop process")

app = App()
app.mainloop()