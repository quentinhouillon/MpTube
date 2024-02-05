import customtkinter as tk
from tkinter import PhotoImage, messagebox
from pytube import YouTube
from datetime import datetime
from pathlib import Path
import ssl


class App(tk.CTk):
    def __init__(self, year):
        super().__init__()

        # SETTINGS WINDOWS
        self.title("MpTube")
        self.geometry("550x380")
        self.resizable(False, False)
        self.focus_force()

        # LOAD IMAGE
        logo = PhotoImage(file="img/youtube_logo.png")

        # FRAME
        self.footer = tk.CTkFrame(self, fg_color="transparent")
        self.footer.pack(side="bottom")

        # LABEL
        self.lbl_logo = tk.CTkLabel(self, image=logo, text="")
        self.lbl_logo.pack(side="top")

        self.lbl_title = tk.CTkLabel(self, text="MpTube",
                                     font=("sans serif", 30, "bold"))
        self.lbl_title.pack(side="top", anchor="n")

        self.lbl_footer = tk.CTkLabel(
            self.footer,
            text=f"© {year} - Quentin Houillon Tous droit réservé",
            text_color="grey", font=("sans serif", 10, "italic"))
        self.lbl_footer.pack(anchor="center")

        # ENTRY
        self.ent = tk.CTkEntry(self, corner_radius=50, placeholder_text="URL",
                               border_width=0)
        self.ent.pack(fill="x", padx=20, pady=10)

        # FRAME PROGRESSBAR
        self.frm_progress = tk.CTkFrame(self, fg_color="transparent",
                                        height=50)
        self.frm_progress.pack(anchor="center", padx=20, pady=10, fill="x")

        # BUTTON
        self.btn_mp3 = tk.CTkButton(self, text="Télécharger en MP3",
                                    fg_color="#e74c3c", hover_color="#e74c3c",
                                    corner_radius=50,
                                    command=lambda: self.download(
                                        url=self.ent.get(), mp3=True))
        self.btn_mp3.pack(padx=(90, 0), pady=0, side="left", anchor="n")

        self.btn_mp4 = tk.CTkButton(self, text="Télécharger en MP4",
                                    fg_color="#e74c3c", hover_color="#e74c3c",
                                    corner_radius=50,
                                    command=lambda: self.download(
                                        url=self.ent.get(), mp3=False))
        self.btn_mp4.pack(padx=(0, 90), pady=0, side="right", anchor="n")

    def download(self, url, mp3):
        if url.strip() != "":
            top = TopLevel(self)
            yt = YouTube(url.strip(), on_progress_callback=top._on_progress,
                         on_complete_callback=top._on_completed)
            try:
                if mp3:
                    stream = yt.streams.get_audio_only()  # MP3
                    extension = "mp3"
                else:
                    stream = yt.streams.get_highest_resolution()  # MP4
                    extension = "mp4"
                download_path = str(Path.home() / "Downloads")
                self.ent.delete(0, "end")
                stream.download(
                    download_path, filename=f"{yt.title}.{extension}")
            except Exception:
                messagebox.showerror(
                    "Erreur",
                    "MpTube ne parvient pas à télécharger la vidéo")


class TopLevel(tk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)

        # TITLE
        self.lbl_title = tk.CTkLabel(self, text="Téléchargement en cours")
        self.lbl_title.pack(anchor="center", padx=10, pady=10)

        # PROGRESSBAR
        self.progressbar = tk.CTkProgressBar(self)
        self.progressbar.set(0)
        self.progressbar.pack(fill="x", padx=10,  pady=5)

        # PERCENTAGE
        self.lbl_percentage = tk.CTkLabel(self, text="0%")
        self.lbl_percentage.pack(anchor="center")

    def _on_progress(self, stream, _, bytes_remaining):
        total_size = stream.filesize
        bytes_downloading = total_size - bytes_remaining
        percent = bytes_downloading/total_size*100
        per = str(int(percent))
        self.lbl_percentage.configure(text=f"{per}%")
        self.lbl_percentage.update()
        self.progressbar.set(float(percent)/100)

    def _on_completed(self, _, file):
        self.destroy()
        messagebox.showinfo("Succès", "Téléchargement terminé")


def main():
    ssl._create_default_https_context = ssl._create_stdlib_context
    date = datetime.now()
    root = App(date.year)
    root.mainloop()


if __name__ == "__main__":
    main()
