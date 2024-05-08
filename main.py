from kivy.config import Config
from kivy.core.window import Window
from reqeust_orm import *
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.config import Config
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import BaseButton,MDTextButton,MDFloatingActionButton
from kivy.uix.stacklayout import StackLayout
from kivy.uix.image import AsyncImage
from kivy.uix.scrollview import ScrollView
from kivy_audio_android import SoundLoader
from Player import *
from kivy.clock import Clock


class NavScreen(MDScreen):
    def build(self):
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Light"
        
class MyApp(MDApp):
    def build(self):
        self.screen = NavScreen()
        self.ORM = AppORM()
        self.status_player = ''
        self.Player = PlayerMusicManager('track')
        Config.set('graphics', 'width', '420')
        Config.set('graphics', 'height', '730')
        Config.write()
        if self.ORM.id_host == None:
            self.screen.ids.screen_1.add_widget(MDLabel(text='No internet connection',halign="center"))
        else:
            track_list = self.ORM.get_request()
            track_list.append(track_list[0])
            track_list.append(track_list[0])
            track_list.append(track_list[0])
            track_list.append(track_list[0])
            track_list.append(track_list[0])
            track_list.append(track_list[0])
            track_list.append(track_list[0])
            scroll = ScrollView(size_hint=[1,None],height=str(110*5.5)+'dp',scroll_type=['bars','content'],bar_width="10dp",pos_hint={'top':0.9,})
            list_of_buttn = StackLayout(orientation='lr-tb',size_hint=(1,None),height=str(110*(len(track_list)))+'dp',spacing = 10)
            for track in track_list:
                text = MDTextButton(text=track['name'],padding=(90,0))
                image = AsyncImage(source=f'http://{self.ORM.host[self.ORM.id_host]}:8000/'+str(track['track_img']),pos_hint={'x':None,'y':None},size_hint=(None,None),size=(80,80))
                button = BaseButton(size_hint=(None,None),size=(400,100),line_color=(1,1,1,1),
                                    md_bg_color=(1,1,1,1),halign='left',valign='top',
                                    on_release=lambda x:self.start_play(f'http://{self.ORM.host[self.ORM.id_host]}:8000'+str(track['track']),track['name']))
                button.add_widget(image)
                button.add_widget(text)
                list_of_buttn.add_widget(button)
            scroll.add_widget(list_of_buttn)
            self.screen.ids.screen_1.add_widget(scroll)
        return self.screen
    def search(self):
        if self.ORM.id_host ==  None:
            self.screen.ids.screen_2.add_widget(MDLabel(text='No internet connection',halign="center"))
        else:
            if self.screen.ids.search_field.text != "":
                track_list = self.ORM.search_request(self.screen.ids.search_field.text)
                list_of_buttn = StackLayout(orientation='lr-tb',size_hint=(1,None),pos_hint={'top':0.9,},height=str(110*(len(track_list)))+'dp',spacing = 10)
                for track in track_list:
                    text = MDTextButton(text=track['name'],padding=(90,0))
                    image = AsyncImage(source=track['track_img'],pos_hint={'x':None,'y':None},size_hint=(None,None),size=(80,80))
                    button = BaseButton(size_hint=(None,None),size=(400,100), line_color=(1,1,1,1),
                                        md_bg_color=(1,1,1,1),pos_hint={'x':.2,'y':.73},halign='left',valign='top',
                                        on_release=lambda x:self.start_play(track['track'],track['name']))
                    button.add_widget(image)
                    button.add_widget(text)
                    list_of_buttn.add_widget(button)
                self.screen.ids.screen_2.add_widget(list_of_buttn)
                                                                             
    
    def start_play(self,track_adress,track_name):
        if self.status_player == 'played':
            self.sound.stop()
            self.sound.unload()
            self.sound = SoundLoader.load(self.Player.get_track(track_adress,track_name))
            self.time_track = 0
            self.sound.play()
            self.status_player = 'played'
        else:
            player = MDFloatLayout(md_bg_color=(.95, .95, .95, 1),pos_hint={'x':.0,'y':.105},size_hint=(None,None),width=420,height=50,radius=(10,10,0,0),line_color=(0,0,0,1))
            text_track = MDLabel(text=track_name,padding=(20,),pos_hint={'x':0,'y':0})
            self.action_btn = MDFloatingActionButton(icon='pause',on_press=self.action_track_stop,halign='center',pos_hint={'x':.9,'y':.1},icon_color='black',shadow_color=(.95, .95, .95, 1),type='small',md_bg_color=(.95, .95, .95, 1))
            player.add_widget(text_track)
            player.add_widget(self.action_btn)
            self.screen.add_widget(player)
            self.sound = SoundLoader.load(self.Player.get_track(track_adress,track_name))
            self.sound_position = None
            self.sound.play()
            Clock.schedule_once(self.get_pos_sound,.1)
            self.status_player = 'played'
        return 
    
    def action_track_stop(self,dt):
        
        if self.action_btn.icon == 'pause':
            self.sound.stop()
            self.sound_position = self.sound.get_pos()
            self.action_btn.icon = 'play'
        else:
            self.sound.play()
            Clock.schedule_once(self.get_pos_sound,.23)
            self.action_btn.icon = 'pause'


    def get_pos_sound(self,dt):
        self.sound.seek(self.sound_position)
               
        



if __name__ == '__main__':
   
    MyApp().run()
