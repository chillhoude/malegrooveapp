import requests
import os


class PlayerMusicManager:
    def __init__(self,track_folder):
        self.track_folder = track_folder


    def get_track(self,url_track,track_name):
        if self.searchLocalFile(track_name) == False:
            content = requests.get(url_track,allow_redirects=True)
            open(f'{self.track_folder}/{track_name}.mp3','wb').write(content.content)
            return f'{self.track_folder}/{track_name}.mp3'
        else:
            return self.searchLocalFile(track_name)
        
    def searchLocalFile(self,track_name):
        for file in os.scandir(self.track_folder):
            if file.name == f'{track_name}.mp3':
                 return f'{self.track_folder}/{track_name}.mp3'
            else:
                 return False
        return False