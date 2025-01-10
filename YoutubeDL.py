# By Jerrald J. Guiriba
# https://github.com/Jed556/CTk-YTDL

import tkinter
import tkinter.messagebox
import customtkinter
import os
import subprocess
import threading
from tkVideoPlayer import TkinterVideo
import time

# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("System")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("blue")

download_path = {
    "folder": "downloads",
    "audio": "downloads\\audio",
    "video": "downloads\\video",
    "both": "downloads\\both"
}


class YoutubeDownloaderApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("YouTube Downloader")
        self.geometry(f"{1400}x{720}")
        self.minsize(1400, 600)  # Set minimum width and height

        self.grid_columnconfigure(1, weight=1, minsize=600)
        self.grid_columnconfigure(4, weight=1, minsize=500)
        self.grid_columnconfigure(3, weight=0)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar Frame
        self.sidebar_frame = customtkinter.CTkFrame(
            self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # Sidebar Frame - Logo
        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Youtube\nDownloader", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Sidebar Frame - Buttons
        # self.sidebar_button_1 = customtkinter.CTkButton(
        #     self.sidebar_frame, command=self.sidebar_button_event)
        # self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        # self.sidebar_button_2 = customtkinter.CTkButton(
        #     self.sidebar_frame, command=self.sidebar_button_event)
        # self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        # self.sidebar_button_3 = customtkinter.CTkButton(
        #     self.sidebar_frame, command=self.sidebar_button_event)
        # self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        # Sidebar Frame - Settings
        self.appearance_mode_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=[
                                                                       "Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(
            row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # Download Frame
        self.download_frame = customtkinter.CTkFrame(
            self, fg_color="transparent")
        self.download_frame.grid(row=1, column=1, columnspan=4, padx=(
            20, 20), pady=(20, 20), sticky="nsew")
        self.download_frame.grid_columnconfigure(0, weight=1)
        self.download_frame.grid_columnconfigure(1, weight=1)
        self.download_frame.grid_columnconfigure(2, weight=1)
        self.download_frame.grid_columnconfigure(3, weight=0)

        # Download Frame - URL Entry
        self.url_entry = customtkinter.CTkEntry(
            self.download_frame, placeholder_text="Enter YouTube URL")
        self.url_entry.grid(row=0, column=0, columnspan=3,
                            padx=(0, 0), pady=(0, 5), sticky="nsew")
        self.url_entry.bind("<KeyRelease>", self.check_entries)

        # Download Frame - Save Directory
        self.save_dir_textbox = customtkinter.CTkTextbox(
            self.download_frame, height=25)
        self.save_dir_textbox.grid(row=1, column=0, columnspan=3, padx=(
            0, 0), pady=(5, 0), sticky="nsew")
        self.save_dir_textbox.configure(state="disabled")

        # Download Frame - Download Option
        self.download_option = customtkinter.CTkOptionMenu(
            self.download_frame, values=["Video", "Audio", "Both"])
        self.download_option.grid(row=0, column=3, padx=(
            20, 0), pady=(0, 5), sticky="nsew")
        self.download_option.set("Video")

        # Download Frame - Download Button
        self.download_button = customtkinter.CTkButton(
            self.download_frame, text="Download", command=self.download_event, state="disabled")
        self.download_button.grid(row=1, column=3, padx=(
            20, 0), pady=(0, 0), sticky="nsew")

        # Volume Frame
        self.volume_frame = customtkinter.CTkFrame(
            self, fg_color="transparent")
        self.volume_frame.grid(row=0, column=2, padx=10,
                               pady=10, sticky="nsew")
        self.volume_frame.grid_columnconfigure(0, weight=1)
        self.volume_frame.grid_rowconfigure(0, weight=1)

        # Volume Frame - Volume Slider
        self.slider_2 = customtkinter.CTkSlider(
            self.volume_frame, orientation="vertical", command=self.update_volume_label)
        self.slider_2.grid(row=0, column=0, padx=10, pady=10, sticky="ns")

        self.volume_label = customtkinter.CTkLabel(
            self.volume_frame, text="0%")
        self.volume_label.grid(row=1, column=0, padx=10, pady=10, sticky="n")

        # Volume Frame - Volume Gain
        self.progressbar_3 = customtkinter.CTkProgressBar(
            self.volume_frame, orientation="vertical")
        self.progressbar_3.grid(row=0, column=1, padx=10, pady=10, sticky="ns")
        self.progressbar_3.set(0)

        self.gain_label = customtkinter.CTkLabel(
            self.volume_frame, text="0 db")
        self.gain_label.grid(row=1, column=1, padx=10, pady=10, sticky="n")

        # Video Player Frame
        self.video_player_frame = customtkinter.CTkFrame(
            self, fg_color="transparent")
        self.video_player_frame.grid(row=0, column=1, padx=(
            20, 20), pady=(10, 10), sticky="nsew")
        self.video_player_frame.grid_columnconfigure(0, weight=1)
        self.video_player_frame.grid_rowconfigure((0, 2), weight=0)
        self.video_player_frame.grid_rowconfigure(1, weight=1)
        self.video_player_label = customtkinter.CTkLabel(
            self.video_player_frame, text="Video Player", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.video_player_label.grid(
            row=0, column=0, padx=20, pady=(20, 10))

        # Video Player Frame - Video Player
        self.video_player = TkinterVideo(
            master=self.video_player_frame, scaled=True)
        self.video_player.grid(row=1, column=0, padx=(
            20, 20), pady=(10, 10), sticky="nsew")

        # Video Player Frame - Controls
        self.control_frame = customtkinter.CTkFrame(
            self.video_player_frame, fg_color="transparent")
        self.control_frame.grid(row=3, column=0, columnspan=6, padx=(
            20, 20), pady=(10, 10), sticky="nsew")
        self.control_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        button_padx = (5, 5)
        button_pady = (10, 20)

        self.prev_button = customtkinter.CTkButton(
            self.control_frame, text="Previous", command=self.prev_video)
        self.prev_button.grid(
            row=0, column=0, padx=button_padx, pady=button_pady, sticky="nsew")

        self.seek_back_button = customtkinter.CTkButton(
            self.control_frame, text="Seek -10s", command=self.seek_back)
        self.seek_back_button.grid(
            row=0, column=1, padx=button_padx, pady=button_pady, sticky="nsew")

        self.play_pause_button = customtkinter.CTkButton(
            self.control_frame, text="Play/Pause", command=self.play_pause_video)
        self.play_pause_button.grid(
            row=0, column=2, padx=button_padx, pady=button_pady, sticky="nsew")

        self.seek_forward_button = customtkinter.CTkButton(
            self.control_frame, text="Seek +10s", command=self.seek_forward)
        self.seek_forward_button.grid(
            row=0, column=3, padx=button_padx, pady=button_pady, sticky="nsew")

        self.next_button = customtkinter.CTkButton(
            self.control_frame, text="Next", command=self.next_video)
        self.next_button.grid(
            row=0, column=4, padx=button_padx, pady=button_pady, sticky="nsew")

        # Video Player Frame - Progress Bar
        self.progress_frame = customtkinter.CTkFrame(
            self.video_player_frame, fg_color="transparent")
        self.progress_frame.grid(row=2, column=0, padx=(
            20, 20), pady=(10, 10), sticky="nsew")
        self.progress_frame.grid_columnconfigure(1, weight=1)

        self.time_elapsed_label = customtkinter.CTkLabel(
            self.progress_frame, text="00:00")
        self.time_elapsed_label.grid(row=0, column=0, padx=(10, 0), sticky="w")

        self.seek_progressbar = customtkinter.CTkSlider(
            self.progress_frame, from_=0, to=100, command=self.seek_video)
        self.seek_progressbar.set(0)
        self.seek_progressbar.grid(row=0, column=1, padx=(10, 10), sticky="ew")

        self.total_time_label = customtkinter.CTkLabel(
            self.progress_frame, text="00:00")
        self.total_time_label.grid(row=0, column=2, padx=(0, 10), sticky="e")

        # Download History Frame
        self.history_frame = customtkinter.CTkFrame(self)
        self.history_frame.grid(row=0, column=4, padx=(
            20, 20), pady=(20, 20), sticky="nsew")
        self.history_frame.grid_columnconfigure(0, weight=1)
        self.history_frame.grid_rowconfigure(0, weight=0)
        self.history_frame.grid_rowconfigure(1, weight=1)
        self.history_label = customtkinter.CTkLabel(
            self.history_frame, text="Download History", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.history_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Download History Frame - Tabview
        self.history_tabview = customtkinter.CTkTabview(self.history_frame)
        self.history_tabview.grid(
            row=1, column=0, padx=20, pady=(10, 20), sticky="nsew")
        self.history_tabview.add("Video")
        self.history_tabview.add("Both")
        self.history_tabview.add("Audio")

        self.history_tabview.tab("Video").grid_columnconfigure(0, weight=1)
        self.history_tabview.tab("Video").grid_rowconfigure(0, weight=1)
        self.history_tabview.tab("Both").grid_columnconfigure(0, weight=1)
        self.history_tabview.tab("Both").grid_rowconfigure(0, weight=1)
        self.history_tabview.tab("Audio").grid_columnconfigure(0, weight=1)
        self.history_tabview.tab("Audio").grid_rowconfigure(0, weight=1)

        # Download History Frame - Tabview - Scrollable Frame
        self.video_scrollable_frame = customtkinter.CTkScrollableFrame(
            self.history_tabview.tab("Video"))
        self.video_scrollable_frame.grid(
            row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.both_scrollable_frame = customtkinter.CTkScrollableFrame(
            self.history_tabview.tab("Both"))
        self.both_scrollable_frame.grid(
            row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.audio_scrollable_frame = customtkinter.CTkScrollableFrame(
            self.history_tabview.tab("Audio"))
        self.audio_scrollable_frame.grid(
            row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.load_history()

        # Set Default Values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")

        self.video_player.bind("<<Duration>>", self.update_duration)
        self.video_player.bind("<<SecondChanged>>", self.update_progress)
        self.video_player.bind("<<Ended>>", self.video_ended)

    def download_video(self):
        url = self.url_entry.get()
        download_type = self.download_option.get()
        if download_type == "Video":
            command = ["yt-dlp", url, "-o", f"{download_path['video']}\\%(title)s.%(ext)s",
                       "-f", "bv", "--recode-video", "mp4", "--add-metadata", "--embed-thumbnail"]
            save_dir = download_path["video"]
        elif download_type == "Audio":
            command = ["yt-dlp", url, "-o", f"{download_path['audio']}\\%(title)s.%(ext)s", "-f", "ba", "-x",
                       "--audio-format", "mp3", "--add-metadata", "--embed-thumbnail", "--audio-quality", "0"]
            save_dir = download_path["audio"]
        else:
            command = ["yt-dlp", url, "-o", f"{download_path['both']}\\%(title)s.%(ext)s",
                       "--recode-video", "mp4", "--add-metadata", "--embed-thumbnail"]
            save_dir = download_path["both"]

        # try:
        subprocess.run(command, check=True)
        tkinter.messagebox.showinfo(
            "Success", "Download completed successfully.")
        self.clear_history()
        self.load_history()
        self.save_dir_textbox.configure(state="normal")
        self.save_dir_textbox.delete("1.0", "end")
        self.save_dir_textbox.insert("1.0", f"Saved to {save_dir}")
        self.save_dir_textbox.configure(state="disabled")
        # except subprocess.CalledProcessError as e:
        #     print(f"Error downloading {download_type}: {e}")
        #     tkinter.messagebox.showerror(
        #         "Error", f"Failed to download {download_type}: {e}")

    def download_event(self):
        self.download_video()
        self.url_entry.delete(0, "end")

    def load_history(self):
        if not os.path.exists(download_path["video"]):
            os.makedirs(download_path["video"])
        if not os.path.exists(download_path["audio"]):
            os.makedirs(download_path["audio"])
        if not os.path.exists(download_path["both"]):
            os.makedirs(download_path["both"])

        for file in os.listdir(download_path["video"]):
            self.create_history_frame(file, "video")
        for file in os.listdir(download_path["audio"]):
            self.create_history_frame(file, "audio")
        for file in os.listdir(download_path["both"]):
            self.create_history_frame(file, "both")

    def clear_history(self):
        for widget in self.video_scrollable_frame.winfo_children():
            widget.destroy()
        for widget in self.audio_scrollable_frame.winfo_children():
            widget.destroy()
        for widget in self.both_scrollable_frame.winfo_children():
            widget.destroy()

    def create_history_frame(self, file, media_type):
        parent_frame = self.video_scrollable_frame if media_type == "video" else self.audio_scrollable_frame if media_type == "audio" else self.both_scrollable_frame
        parent_frame.grid_columnconfigure(0, weight=1)
        frame = customtkinter.CTkFrame(
            parent_frame)
        frame.grid_columnconfigure((0, 1, 2), weight=1)
        frame.grid_columnconfigure((3), weight=0)

        title_label = customtkinter.CTkLabel(
            frame, text=file, font=customtkinter.CTkFont(size=12))
        title_label.grid(row=0, column=0, padx=5, pady=(0, 2), sticky="w")

        file_path = os.path.join(download_path[media_type], file)
        creation_time = os.path.getctime(file_path)
        date_label = customtkinter.CTkLabel(
            frame, text=f"Date: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(creation_time))}", font=customtkinter.CTkFont(size=12))
        date_label.grid(row=1, column=0, padx=5, pady=0, sticky="w")

        filler = customtkinter.CTkLabel(
            frame, text="", font=customtkinter.CTkFont(size=12))
        filler.grid(row=0, column=2, padx=10, pady=5, sticky="nsew")

        self.selected_checkbox = None

        def on_checkbox_select():
            if self.selected_checkbox and self.selected_checkbox != checkbox:
                self.selected_checkbox.deselect()
            self.selected_checkbox = checkbox
            self.play_media(file, media_type)

        checkbox = customtkinter.CTkCheckBox(
            frame, text="", command=on_checkbox_select, font=customtkinter.CTkFont(size=12))
        checkbox.grid(row=0, column=3, padx=10, pady=5, sticky="e")

        frame.grid(sticky="ew", padx=10, pady=5)
        parent_frame.update_idletasks()

    def play_media(self, file, media_type):
        print(f"Playing {media_type}: {file}")
        file_path = os.path.join(download_path[media_type], file)
        if os.path.exists(file_path):
            try:
                self.video_player.stop()
                self.video_player._container = None  # Reset the container
                self.video_player.seek(0)
                if media_type == "audio":
                    self.video_player.load(file_path)
                    self.video_player.audio_only = True
                else:
                    self.video_player.load(file_path)
                    self.video_player.audio_only = False
                self.video_player.play()
                self.play_pause_button.configure(text="Pause")
                self.update_progress()
            except Exception as e:
                print(f"Error loading media: {e}")
                tkinter.messagebox.showerror(
                    "Error", f"Failed to load media: {e}")
        else:
            print(f"File not found: {file_path}")
            tkinter.messagebox.showerror(
                "Error", f"File not found: {file_path}")

    def play_video(self):
        # if self.is_audio():
        #     pygame.mixer.music.play()
        # else:
        self.video_player.play()
        self.update_progress()

    def prev_video(self):
        print("Previous video or audio")

    def seek_back(self):
        # if self.is_audio():
        #     pygame.mixer.music.rewind()
        #     pygame.mixer.music.set_pos(pygame.mixer.music.get_pos() - 10)
        # else:
        self.video_player.seek(self.video_player.current_duration() - 10)
        self.update_progress()

    def play_pause_video(self):
        # if self.is_audio():
        #     if pygame.mixer.music.get_busy():
        #         pygame.mixer.music.pause()
        #         self.play_pause_button.configure(text="Play")
        #     else:
        #         pygame.mixer.music.unpause()
        #         self.play_pause_button.configure(text="Pause")
        # else:
        if self.video_player.is_paused():
            self.video_player.play()
            self.play_pause_button.configure(text="Pause")
        else:
            self.video_player.pause()
            self.play_pause_button.configure(text="Play")

    def seek_forward(self):
        # if self.is_audio():
        #     pygame.mixer.music.set_pos(pygame.mixer.music.get_pos() + 10)
        # else:
        self.video_player.seek(self.video_player.current_duration() + 10)
        self.update_progress()

    def next_video(self):
        print("Next video or audio")

    def seek_video(self, value):
        # if self.is_audio():
        #     pygame.mixer.music.set_pos(int(value))
        # else:
        self.video_player.seek(int(value))
        self.update_progress()

    # def is_audio(self):
    #     return self.current_media_type == 'audio'

    def update_progress(self, event=None):
        try:
            current_time = self.video_player.current_duration()
            total_time = self.video_player.video_info()["duration"]
            if total_time > 0:
                self.seek_progressbar.set(current_time)
                self.time_elapsed_label.configure(
                    text=self.format_time(current_time))
                self.total_time_label.configure(
                    text=self.format_time(total_time))
                if not self.video_player.is_paused():
                    self.after(1000, self.update_progress)
        except Exception as e:
            print(f"Error updating progress: {e}")

    def format_time(self, seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02}:{seconds:02}"

    def sidebar_button_event(self):
        print("sidebar_button click")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def check_entries(self, event=None):
        if self.url_entry.get():
            self.download_button.configure(state="normal")
        else:
            self.download_button.configure(state="disabled")

    def update_volume_label(self, value):
        self.volume_label.configure(text=f"{int(value * 100)}%")

    def update_gain_label(self, value):
        self.gain_label.configure(text=f"{int(value * 100)} db")
        self.progressbar_3.set(value)

    def video_ended(self, event):
        self.seek_progressbar.set(self.seek_progressbar.cget("to"))
        self.play_pause_button.configure(text="Play")
        self.seek_progressbar.set(0)

    def update_duration(self, event):
        duration = self.video_player.video_info()["duration"]
        self.total_time_label.configure(text=self.format_time(duration))
        self.seek_progressbar.configure(to=duration)


if __name__ == "__main__":
    app = YoutubeDownloaderApp()
    app.mainloop()
