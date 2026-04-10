import yt_dlp
import json
import os
from dotenv import load_dotenv
from git import Repo

load_dotenv()
token = os.getenv("API_TOKEN")

while True:
    id = input("Yandex Music track ID or URL: ").split('/')[-1].split('?')[0]

    print("Fetching track info...")

    from yandex_music import Client
    client = (Client(token) if token else Client()).init()
    track_info = client.tracks([id])[0]
    track_name = f'{track_info.title} - {(", ".join(track_info.artistsName()))}'
    print(f'Track name: {track_name}')
    url = input("Track URL: ")

    repo = Repo('.')
    should_download = True
    if (url):
        if not url.startswith('http'):
            import shutil
            shutil.copy(url, f'tracks/{id}')
            print(f'File copied to tracks/{id}')
        else:
            should_download = input("Download track? (y/n): ").lower() == 'y'
            if should_download:
                def download_sound(url):
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': f'tracks/{id}',
                    }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl: # type: ignore
                        ydl.download([url])

                download_sound(url)

    with open('list.json', 'r') as f:
        data = json.loads(f.read())
        data['tracks'][id] = f'https://raw.githubusercontent.com/Hazzz895/FckCensorData/refs/heads/main/tracks/{id}' if should_download else url

    with open('list.json', 'w') as f:
        json.dump(data, f, indent=4)
        
    with open('README.md', 'a', encoding='utf-8') as f:
        f.write(f'\n- [{track_name}](https://music.yandex.ru/track/{id})')

    repo.index.add(['list.json', f'tracks/{id}', "README.md"])
    repo.index.commit(f"add track «{track_name}»")
    print(f'Successfully added track {track_name}')