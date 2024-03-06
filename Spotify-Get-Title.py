from time import sleep
import psutil
from pywinauto import Desktop
from pystray import Icon, Menu, MenuItem
from PIL import Image
from threading import Thread, Event

app_closing_event = Event()


def menu_exit(icon):
    icon.visible = False
    icon.stop()


def fetch_title_thead():
    last_title = ''
    song_name_raw = ''
    while True:
        mylist = []
        try:
            for proc in psutil.process_iter():
                if proc.name() == 'Spotify.exe':
                    mylist.append(proc.as_dict(attrs=['pid', 'num_threads']))
            song_name_raw = [w.window_text() for w in Desktop(backend='uia').windows(process=int(max(mylist, key=lambda x: x['num_threads'])['pid']))][0]
        except:
            pass
        if song_name_raw not in ('Spotify Free', 'Spotify Premium') and last_title != song_name_raw:
            last_title = song_name_raw

            # Clean Title Format
            song_name = str(song_name_raw)
            parts = song_name.replace(' - ', "☆").split('☆')
            extra = (' [' + ', '.join(parts[2:]) + ']').replace('-', ' ') if len(parts) > 2 else ''
            song_name = f"{parts[0]} - {parts[1].replace('-', ' ')}{extra}".replace("  ", " ").strip()

            print(f'"{last_title}"  => "{song_name}"')
            with open('spotify-song-title.txt', 'w', encoding='utf-8') as o:
                o.write(song_name)
        sleep(1)
        if app_closing_event.is_set():
            break


if __name__ == '__main__':
    app = Icon(
        "Spotify Get Title",
        Image.open('SmilingNeko.ico'),
        "Spotify Get Title",
        menu=Menu(MenuItem("&Exit", menu_exit)))

    # Start the App Work Thead

    thread = Thread(target=fetch_title_thead)
    thread.start()

    # Start the App Icon
    app.run()

    # Signal the thread of termination and Wait for it
    app_closing_event.set()
    thread.join()
