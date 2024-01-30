import customtkinter as tk
from tkinter import PhotoImage, messagebox
from pytube import YouTube
from datetime import datetime
from pathlib import Path
import ssl


def download(url, mp3):
    if url.strip() != "":
        yt = YouTube(url.strip())
        try:
            if mp3:
                stream = yt.streams.get_audio_only()  # MP3
                extension = "mp3"
            else:
                stream = yt.streams.get_highest_resolution()  # MP4
                extension = "mp4"
            download_path = str(Path.home() / "Downloads")
            stream.download(download_path, filename=f"{yt.title}.{extension}")
        except Exception:
            messagebox.showerror("Erreur",
                                "MpTube ne parvient pas à télécharger la vidéo")


def main(root, year):
    # SETTINGS WINDOWS
    root.title("MpTube")
    root.geometry("550x360")
    root.resizable(False, False)
    root.focus_force()

    # LOAD IMAGE
    logo = PhotoImage(file="youtube_logo.png")

    # FRAME
    footer = tk.CTkFrame(root, fg_color="transparent")
    footer.pack(side="bottom")

    # LABEL
    lbl_logo = tk.CTkLabel(root, image=logo, text="")
    lbl_logo.pack(side="top")

    lbl_title = tk.CTkLabel(root, text="MpTube",
                            font=("sans serif", 30, "bold"))
    lbl_title.pack(side="top", anchor="n")

    lbl_footer = tk.CTkLabel(
        footer, text=f"© {year} - Quentin Houillon Tous droit réservé",
        text_color="grey", font=("sans serif", 10, "italic"))
    lbl_footer.pack(anchor="center")

    # ENTRY
    ent = tk.CTkEntry(root, corner_radius=50, placeholder_text="URL",
                      border_width=0)
    ent.pack(fill="x", padx=20, pady=20)

    # BUTTON
    btn_mp3 = tk.CTkButton(root, text="Télécharger en MP3",
                           fg_color="#e74c3c", hover_color="#e74c3c",
                           corner_radius=50,
                           command=lambda: download(url=ent.get(), mp3=True))
    btn_mp3.pack(padx=(90, 0), pady=0, side="left", anchor="n")
    btn_mp4 = tk.CTkButton(root, text="Télécharger en MP4",
                           fg_color="#e74c3c", hover_color="#e74c3c",
                           corner_radius=50,
                           command=lambda: download(url=ent.get(), mp3=False))
    btn_mp4.pack(padx=(0, 90), pady=0, side="right", anchor="n")


if __name__ == "__main__":
    ssl._create_default_https_context = ssl._create_stdlib_context
    root = tk.CTk()
    date = datetime.now()
    main(root, date.year)
    root.mainloop()
