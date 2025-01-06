import tkinter
import tkinter.messagebox
import customtkinter
import os
from tkVideoPlayer import TkinterVideo
import json

# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("System")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("blue")


download_path = {
    "folder": "downloads",
    "audio": "downloads\\audio",
    "video": "downloads\\video"
}

class YoutubeDownloaderApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("YouTube Downloader")
        self.geometry(f"{1100}x{580}")

        self.grid_columnconfigure(1, weight=1, minsize=600)
        self.grid_columnconfigure(4, weight=1, minsize=200)
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
        self.sidebar_button_1 = customtkinter.CTkButton(
            self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(
            self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(
            self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

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

        # Download Frame - Save Directory Entry
        self.save_dir_entry = customtkinter.CTkEntry(
            self.download_frame, placeholder_text="Enter Save Directory")
        self.save_dir_entry.grid(row=1, column=0, columnspan=3, padx=(
            0, 0), pady=(5, 0), sticky="nsew")

        # Download Frame - Download Button
        self.download_button = customtkinter.CTkButton(
            self.download_frame, text="Download", command=self.download_event)
        self.download_button.grid(row=0, column=3, rowspan=2, padx=(
            20, 0), pady=(0, 0), sticky="nsew")

        # Volume Bars
        self.volume_frame = customtkinter.CTkFrame(
            self, fg_color="transparent")
        self.volume_frame.grid(row=0, column=3, padx=10,
                               pady=10, sticky="nsew")
        self.volume_frame.grid_columnconfigure(0, weight=1)
        self.volume_frame.grid_rowconfigure(0, weight=1)
        self.slider_2 = customtkinter.CTkSlider(
            self.volume_frame, orientation="vertical")
        self.slider_2.grid(row=0, column=0, padx=10, pady=10, sticky="ns")
        self.progressbar_3 = customtkinter.CTkProgressBar(
            self.volume_frame, orientation="vertical")
        self.progressbar_3.grid(row=0, column=1, padx=10, pady=10, sticky="ns")

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

        self.video_player.load("test.mp4")

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
        self.progress_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.time_elapsed_label = customtkinter.CTkLabel(
            self.progress_frame, text="00:00")
        self.time_elapsed_label.grid(row=0, column=0, padx=(10, 0), sticky="w")

        self.seek_progressbar = customtkinter.CTkSlider(
            self.progress_frame, from_=0, to=100, command=self.seek_video)
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
        self.history_tabview.add("Audio")

        self.history_tabview.tab("Video").grid_columnconfigure(0, weight=1)
        self.history_tabview.tab("Video").grid_rowconfigure(0, weight=1)
        self.history_tabview.tab("Audio").grid_columnconfigure(0, weight=1)
        self.history_tabview.tab("Audio").grid_rowconfigure(0, weight=1)

        # Download History Frame - Tabview - Scrollable Frame
        self.video_scrollable_frame = customtkinter.CTkScrollableFrame(
            self.history_tabview.tab("Video"))
        self.video_scrollable_frame.grid(
            row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.audio_scrollable_frame = customtkinter.CTkScrollableFrame(
            self.history_tabview.tab("Audio"))
        self.audio_scrollable_frame.grid(
            row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.load_history()

        # Set Default Values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")

    def download_video(self):
        url = self.url_entry.get()
        save_dir = self.save_dir_entry.get()
        # Implement the download logic here
        # After downloading, update the history
        self.update_history(url, save_dir)

    def load_history(self):
        if not os.path.exists(download_path["video"]):
            os.makedirs(download_path["video"])
        if not os.path.exists(download_path["audio"]):
            os.makedirs(download_path["audio"])

        for file in os.listdir(download_path["video"]):
            customtkinter.CTkButton(self.video_scrollable_frame, text=file, command=lambda f=file: self.play_media(
                f, "video")).grid(sticky="ew", padx=10, pady=5)
        for file in os.listdir(download_path["audio"]):
            customtkinter.CTkButton(self.audio_scrollable_frame, text=file, command=lambda f=file: self.play_media(
                f, "audio")).grid(sticky="ew", padx=10, pady=5)

    def play_media(self, file, media_type):
        # Implement logic to play the selected media file
        print(f"Playing {media_type}: {file}")

    def update_history(self, url, save_dir):
        # Implement logic to save the downloaded file info
        # Update the history tabview with new entries
        if "video" in save_dir:
            customtkinter.CTkButton(self.video_scrollable_frame, text=url, command=lambda: self.play_media(
                url, "video")).grid(sticky="ew", padx=10, pady=5)
        elif "audio" in save_dir:
            customtkinter.CTkButton(self.audio_scrollable_frame, text=url, command=lambda: self.play_media(
                url, "audio")).grid(sticky="ew", padx=10, pady=5)

    def play_video(self):
        self.video_player.play()
        self.update_progress()

    def prev_video(self):
        # Implement logic to play the previous video
        print("Previous video")

    def seek_back(self):
        self.video_player.seek(self.video_player.current_duration() - 10)

    def play_pause_video(self):
        if self.video_player.is_paused():
            self.video_player.play()
        else:
            self.video_player.pause()

    def seek_forward(self):
        self.video_player.seek(self.video_player.current_duration() + 10)

    def next_video(self):
        # Implement logic to play the next video
        print("Next video")

    def seek_video(self, value):
        self.video_player.seek(int(value))

    def update_progress(self):
        current_time = self.video_player.current_duration()
        total_time = self.video_player.video_info()["duration"]
        self.seek_progressbar.set(current_time / total_time * 100)
        self.time_elapsed_label.configure(text=self.format_time(current_time))
        self.total_time_label.configure(text=self.format_time(total_time))
        self.after(1000, self.update_progress)

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

    def download_event(self):
        self.download_video()
        self.url_entry.delete(0, "end")
        self.save_dir_entry.delete(0, "end")


if __name__ == "__main__":
    app = YoutubeDownloaderApp()
    app.mainloop()
