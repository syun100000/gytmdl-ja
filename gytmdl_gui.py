import tkinter as tk
from tkinter import filedialog
import configparser
from gytmdl import Gytmdl
import pyperclip

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

        self.paste_button = tk.Button(self, text="Clear(URL)", command=self.clear_url,font=("",18))  # New Button for Paste
        self.paste_button.pack()

        self.paste_button = tk.Button(self, text="Paste", command=self.paste_clipboard,font=("",25))  # New Button for Paste
        self.paste_button.pack()

        self.urls_txt_label = tk.Label(self, text="URLs from txt")
        self.urls_txt_label.pack()

        self.urls_txt_entry = tk.Entry(self)
        self.urls_txt_entry.insert(0, self.config.get('DEFAULT', 'urls_txt', fallback=''))
        self.urls_txt_entry.pack()

        self.urls_txt_browse_button = tk.Button(self, text="Browse", command=self.browse_txt_file)
        self.urls_txt_browse_button.pack()

        self.cookies_label = tk.Label(self, text="Cookies")
        self.cookies_label.pack()

        self.cookies_entry = tk.Entry(self, show='*')
        self.cookies_entry.insert(0, self.config.get('DEFAULT', 'cookies', fallback=''))
        self.cookies_entry.pack()

        self.cookies_browse_button = tk.Button(self, text="Browse", command=self.browse_cookies_file)
        self.cookies_browse_button.pack()

        self.delete_cookies_button = tk.Button(self, text="Delete Cookies", command=self.delete_cookies)
        self.delete_cookies_button.pack()

        self.quality_label = tk.Label(self, text="Quality (140, 251, or 141)")
        self.quality_label.pack()

        self.quality_entry = tk.Entry(self)
        self.quality_entry.insert(0, self.config.get('DEFAULT', 'quality', fallback='140'))
        self.quality_entry.pack()

        self.download_language_label = tk.Label(self, text="en or ja or ...")
        self.download_language_label.pack()

        self.download_language_entry = tk.Entry(self)
        self.download_language_entry.insert(0, self.config.get('DEFAULT', 'download_language', fallback='ja'))
        self.download_language_entry.pack()

        self.final_path_label = tk.Label(self, text="Final Path")
        self.final_path_label.pack()

        self.final_path_entry = tk.Entry(self)
        self.final_path_entry.insert(0, self.config.get('DEFAULT', 'final_path', fallback=''))
        self.final_path_entry.pack()

        self.final_path_browse_button = tk.Button(self, text="Browse", command=self.browse_final_path)
        self.final_path_browse_button.pack()

        self.download_button = tk.Button(self, text="DOWNLOAD", fg="red", command=self.download_music,font=("",25))
        self.download_button.pack()

        self.progress_label = tk.Label(self, text="Download progress:")
        self.progress_label.pack()

        self.progress_status = tk.StringVar(self)
        self.progress_display = tk.Label(self,width=200,textvariable=self.progress_status)
        self.progress_display.pack(fill=tk.X, expand=True)

        self.quit = tk.Button(self, text="QUIT", fg="red", command=root.destroy)
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
        cookies = self.cookies_entry.get()
        quality = self.quality_entry.get()
        final_path = self.final_path_entry.get()
        download_language = self.download_language_entry.get()

        self.config['DEFAULT']['urls_txt'] = urls_txt
        self.config['DEFAULT']['cookies'] = cookies
        self.config['DEFAULT']['quality'] = quality
        self.config['DEFAULT']['final_path'] = final_path
        self.config['DEFAULT']['download_language'] = download_language

        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

        dl = Gytmdl(cookies, quality, final_path, 'temp', False, False,download_language)

        # Start with the single URL from the url_entry, if any
        urls = [url] if url else []
        # If a .txt file was specified, read and append these URLs
        if urls_txt:
            with open(urls_txt, 'r', encoding='utf8') as f:
                urls.extend(f.read().splitlines())

        # Error count
        error_count = 0

        for url in urls:
            if url:  # Only proceed if the url is not empty
                download_queue = dl.get_download_queue(url.strip())
                # Process each track in the download queue
                for i, track in enumerate(download_queue):
                    try:
                        # Update the progress
                        self.progress_status.set(f'Downloading "{track["title"]}" '
                                                f'(track {i + 1}/{len(download_queue)})\n'
                                                f'from URL {url}')
                        self.update()

                        ytmusic_watch_playlist = dl.get_ytmusic_watch_playlist(track['id'])
                        if ytmusic_watch_playlist is None:
                            track['id'] = dl.search_track(track['title'])
                            ytmusic_watch_playlist = dl.get_ytmusic_watch_playlist(track['id'])
                        tags = dl.get_tags(ytmusic_watch_playlist)
                        final_location = dl.get_final_location(tags)
                        temp_location = dl.get_temp_location(track['id'])
                        dl.download(track['id'], temp_location)
                        fixed_location = dl.get_fixed_location(track['id'])
                        dl.fixup(temp_location, fixed_location)
                        dl.make_final(final_location, fixed_location, tags)
                    except:
                        error_count += 1
                        self.progress_status.set(f'Downloading "{track["title"]}" '
                                                f'(track {i + 1}/{len(download_queue)})\n'
                                                f'from URL {url}')
                        self.update()
                    finally:
                        dl.cleanup()

        # Set download completed message
        if error_count == 0:
            self.progress_status.set("Download completed!")
        else:
            self.progress_status.set(f"Download completed with {error_count} error(s).")

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
