import tkinter as tk
from tkinter import filedialog
import configparser
from gytmdl import Gytmdl
import pyperclip
import os
import sys
from tkinter import ttk

__version__ = '0.0.1'
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.config = configparser.ConfigParser()
        self.load_config()
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.url_label = tk.Label(self, text="YouTube URL")
        self.url_label.pack()

        self.url_entry = tk.Entry(self,width=100)
        self.url_entry.pack()

        self.paste_button = tk.Button(self, text="URLをクリア", command=self.clear_url,font=("",18))  # ペースト用の新しいボタン
        self.paste_button.pack()

        self.paste_button = tk.Button(self, text="貼り付け", command=self.paste_clipboard,font=("",25))  # ペースト用の新しいボタン
        self.paste_button.pack()

        self.urls_txt_label = tk.Label(self, text="txtからのURL")
        self.urls_txt_label.pack()

        self.urls_txt_entry = tk.Entry(self)
        self.urls_txt_entry.insert(0, self.config.get('DEFAULT', 'urls_txt', fallback=''))
        self.urls_txt_entry.pack()

        self.urls_txt_browse_button = tk.Button(self, text="参照", command=self.browse_txt_file)
        self.urls_txt_browse_button.pack()

        self.cookies_label = tk.Label(self, text="クッキーの場所")
        self.cookies_label.pack()

        self.cookies_entry = tk.Entry(self, show='*')
        self.cookies_entry.insert(0, self.config.get('DEFAULT', 'cookies', fallback=''))
        self.cookies_entry.pack()

        self.cookies_browse_button = tk.Button(self, text="参照", command=self.browse_cookies_file)
        self.cookies_browse_button.pack()

        self.delete_cookies_button = tk.Button(self, text="クッキーを削除", command=self.delete_cookies)
        self.delete_cookies_button.pack()

        self.quality_label = tk.Label(self, text="品質 (140, 251, または 141)")
        self.quality_label.pack()

        self.quality_entry = tk.Entry(self)
        self.quality_entry.insert(0, self.config.get('DEFAULT', 'quality', fallback='140'))
        self.quality_entry.pack()

        self.download_language_label = tk.Label(self, text="ダウンロード言語 (en, ja, etc...)")
        self.download_language_label.pack()

        self.download_language_entry = tk.Entry(self)
        self.download_language_entry.insert(0, self.config.get('DEFAULT', 'download_language', fallback='ja'))
        self.download_language_entry.pack()

        self.final_path_label = tk.Label(self, text="保存先")
        self.final_path_label.pack()

        self.final_path_entry = tk.Entry(self)
        self.final_path_entry.insert(0, self.config.get('DEFAULT', 'final_path', fallback=''))
        self.final_path_entry.pack()

        self.final_path_browse_button = tk.Button(self, text="参照", command=self.browse_final_path)
        self.final_path_browse_button.pack()

        self.download_button = tk.Button(self, text="ダウンロード", fg="red", command=self.download_music,font=("",25))
        self.download_button.pack()

        self.progress_label = tk.Label(self, text="ダウンロード進行状況：")
        self.progress_label.pack()
        
        self.progress_bar = ttk.Progressbar(self, length=200, mode='determinate')
        self.progress_bar.pack()

        self.progress_status = tk.StringVar(self)
        self.progress_display = tk.Label(self,width=200,textvariable=self.progress_status)
        self.progress_display.pack(fill=tk.X, expand=True)

        self.quit = tk.Button(self, text="終了", fg="red", command=sys.exit)
        self.quit.pack()

        
    def clear_url(self):
        self.url_entry.delete(0, tk.END)
    def paste_clipboard(self):
        clipboard_content = pyperclip.paste()  # Read from clipboard
        self.url_entry.delete(0, tk.END)  # Clear Entry widget
        self.url_entry.insert(0, clipboard_content)  # Insert clipboard content into Entry widget

    def download_music(self):
        url = self.url_entry.get().strip()  # Remove any leading/trailing whitespace
        urls_txt = self.urls_txt_entry.get()
        cookies = os.path.abspath(self.cookies_entry.get())
        quality = self.quality_entry.get()
        final_path = os.path.abspath(self.final_path_entry.get())
        download_language = self.download_language_entry.get()

        self.config['DEFAULT']['urls_txt'] = urls_txt
        self.config['DEFAULT']['cookies'] = cookies
        self.config['DEFAULT']['quality'] = quality
        self.config['DEFAULT']['final_path'] = final_path
        self.config['DEFAULT']['download_language'] = download_language

        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

        temp=os.path.join(final_path,"temp")
        dl = Gytmdl(cookies, quality, final_path, temp, False, False,download_language)

        # Start with the single URL from the url_entry, if any
        urls = [url] if url else []
        # If a .txt file was specified, read and append these URLs
        if urls_txt:
            with open(urls_txt, 'r', encoding='utf8') as f:
                urls.extend(f.read().splitlines())

        # Error count
        error_count = 0

        for j, url in enumerate(urls):
            if url:  # Only proceed if the url is not empty
                download_queue = dl.get_download_queue(url.strip())
                # Process each track in the download queue
                for i, track in enumerate(download_queue):
                    try:
                        # Update the progress
                        # 全体のタスク数を計算する
                        total_task = len(download_queue) * len(urls)
                        progress_percentage = int(((i+1)*(j+1)/total_task)*100)
                        self.progress_bar['value'] = progress_percentage
                        self.progress_status.set(f'ダウンロード中 "{track["title"]}" '
                                                f'(track {i + 1}/{len(download_queue)})\n'
                                                f'from URL {j + 1}/{len(urls)}\n'
                                                f'全体の進行状況{progress_percentage}%')
                        self.update()
                        ytmusic_watch_playlist = dl.get_ytmusic_watch_playlist(track['id'])
                        if ytmusic_watch_playlist is None:
                            print("ytmusic_watch_playlist is None")
                            track['id'] = dl.search_track(track['title'])
                            ytmusic_watch_playlist = dl.get_ytmusic_watch_playlist(track['id'])
                        tags = dl.get_tags(ytmusic_watch_playlist)
                        final_location = dl.get_final_location(tags)
                        temp_location = dl.get_temp_location(track['id'])
                        dl.download(track['id'], temp_location)
                        fixed_location = dl.get_fixed_location(track['id'])
                        dl.fixup(temp_location, fixed_location)
                        dl.make_final(final_location, fixed_location, tags)
                        print(f'Downloaded "{track["title"]}" from URL {url}')
                        
                    except:
                        error_count += 1
                        self.progress_status.set(f'ダウンロード中 "{track["title"]}" '
                                                f'(track {i + 1}/{len(download_queue)})\n'
                                                f'from URL {url}')
                        self.update()
                        print(f'Error downloading "{track["title"]}" from URL {url}')
                    finally:
                        dl.cleanup()

        if error_count == 0:
            self.progress_status.set("ダウンロード完了!")
            print("ダウンロード完了!")
            self.progress_bar['value'] = 100
        else:
            self.progress_status.set(f" ダウンロード未完了 {error_count} 個のエラーがありました。もしかしたらffmpegがないかもしれません")
            print(f"ダウンロード未完了 {error_count} 個のエラーがありました。もしかしたらffmpegがないかもしれません")
            self.progress_bar['value'] = 0

    def load_config(self):
        self.config.read('config.ini')

    def delete_cookies(self):
        self.config['DEFAULT']['cookies'] = ''
        self.cookies_entry.delete(0, tk.END)
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

    def browse_txt_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        self.urls_txt_entry.delete(0, tk.END)
        self.urls_txt_entry.insert(0, file_path)

    def browse_cookies_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        self.cookies_entry.delete(0, tk.END)
        self.cookies_entry.insert(0, file_path)

    def browse_final_path(self):
        folder_path = filedialog.askdirectory()
        self.final_path_entry.delete(0, tk.END)
        self.final_path_entry.insert(0, folder_path)
    
        

root = tk.Tk()
root.title("Gytmdl GUI - Graphical YouTube Music Downloader")
root.geometry("1024x680")  # Adjust window size as needed
app = Application(master=root)
app.mainloop()
