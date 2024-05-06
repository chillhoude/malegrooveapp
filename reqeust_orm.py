import requests

hosts_ip = ['192.168.0.195',
            '192.168.0.192']

class AppORM:
    def __init__(self):
        self.host = hosts_ip
        el = 0
        while el <= len(self.host):
            try:
                if el > len(self.host)-1:
                    el = None
                    break
            except requests.exceptions.ConnectionError:
                el = el + 1
                continue
            except requests.exceptions.ConnectTimeout:
                el = el + 1
                continue
            
            else:
                break
        self.id_host = el 
    def search_request(self,text):
        if self.id_host != None:
            response = requests.get(f'http://{self.host[self.id_host]}:8000/api/search/',params={'search':text}).json()
        else: 
            response = 'No internet conection'
        return response
    def get_request(self):
        if self.id_host != None:
            response = requests.get(f'http://{self.host[self.id_host]}:8000/api/anonimuser/').json()
        else: 
            response = 'No internet conection'
        return response
            
    


