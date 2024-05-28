from kivy.config import Config
from kivy.core.window import Window
from kivymd.uix.boxlayout import MDBoxLayout
from reqeust_orm import *
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.config import Config
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import BaseButton,MDTextButton,MDFloatingActionButton,MDFlatButton
from kivy.uix.stacklayout import StackLayout
from kivy.uix.image import AsyncImage
from kivy.uix.scrollview import ScrollView
from kivy.core.audio import SoundLoader
from Player import *
from kivy.clock import Clock
from kivymd.uix.dialog.dialog import MDDialog


class NavScreen(MDScreen):
    def build(self):
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Light"

class LoginContent(MDBoxLayout):
    pass

class RegistrContent(MDBoxLayout):
    pass

        
class MyApp(MDApp):
    def build(self):
        self.screen = NavScreen()
        self.ORM = AppORM()
        self.status_player = ''
        self.Player = PlayerMusicManager('track')
        self.height_window = Window.size[1] - 150
        if self.ORM.id_host == None:
            self.screen.ids.screen_1.add_widget(MDLabel(text='No internet connection',halign="center"))
        else:
            self.track_list = self.ORM.get_request()
            self.list_button=''
            scroll = ScrollView(size_hint=[1,None], height=self.height_window, scroll_type=['bars','content'], bar_width="10dp", pos_hint={'top':0.9,})
            self.list_of_buttns = StackLayout(orientation='lr-tb',size_hint=(1,None), height=((int(self.height_window)/8)+10)*len(self.track_list), spacing = 10)
            for track_index in range(0,len(self.track_list)):
                track_str_index ='track_num_'+ str(track_index)
                track = self.track_list[track_index]
                self.list_button= f'''
BaseButton:
    size_hint:0.95,None
    id:{track_str_index}
    height:{int(self.height_window)/8}
    line_color:1,1,1,1
    md_bg_color:1,1,1,1
    halign:'left'
    valign:'top'
    on_release:app.start_play('http://{self.ORM.host[self.ORM.id_host]}:8000{str(self.track_list[track_index]['track'])}','{self.track_list[track_index]['name']}')
    MDTextButton:
        text:'{track['name']}'
        padding:{(Window.size[0]/100)*25},0
    AsyncImage:
        source:'http://{self.ORM.host[self.ORM.id_host]}:8000/{str(track['track_img'])}'
        size_hint:.2,1
        pos_hint_x:0
        pos_hint_y:0
        keep_ratio:False
        allow_stretch:True
        fit_mode:'contain'
                '''
                self.list_of_buttns.add_widget(Builder.load_string(self.list_button))
            scroll.add_widget(self.list_of_buttns)
            self.screen.ids.screen_1.add_widget(scroll)
            print(Window.size[1])
            self.registform = RegistrContent()
            self.loginform = LoginContent()
            self.scroll_search = ScrollView(size_hint=[1,None], height=self.height_window, scroll_type=['bars','content'], bar_width="10dp", pos_hint={'top':0.9,})
            self.screen.ids.screen_2.add_widget(self.scroll_search)
            self.sign_in_dialog = MDDialog(title='Увійти',
            type='custom',
            buttons=[
            MDFlatButton(text="Закрити", 
            
            theme_text_color="Custom", 
            text_color=self.theme_cls.primary_color,
            on_release=lambda x:self.sign_in_dialog.dismiss(force=True)),
            MDFlatButton(text="Увійти", theme_text_color="Custom", on_release=lambda x:self.login_user(),
            text_color=self.theme_cls.primary_color,),],
            content_cls=self.loginform,)
            self.registr_dialog = MDDialog(title='Pеєстрація',
            content_cls=self.registform,
            type='custom',
            buttons=[
            MDFlatButton(text="Закрити", 
            theme_text_color="Custom", 
            text_color=self.theme_cls.primary_color,
            on_release=lambda x:self.registr_dialog.dismiss(force=True)),
            MDFlatButton(text="зареєструватися", theme_text_color="Custom", 
            text_color=self.theme_cls.primary_color,on_release=lambda x:self.register_user()),],
           
            )
            reg_text = MDTextButton(text="Pеєстрація")
            reg_button = BaseButton(pos_hint={'center_x':.5,'center_y':.6},size_hint=(0.4,0.1), md_bg_color=(1,.5,0,1), halign='center', valign='center', on_release=lambda x:self.registr_dialog.open())
            reg_button.add_widget(reg_text)
            sign_in_text = MDTextButton(text="Увійти")
            sign_in_button = BaseButton(size_hint=(0.4,0.1), pos_hint={'center_x':.5,'center_y':.4}, md_bg_color=(0,0,0,.3), halign='center', valign='center', on_release=lambda x:self.sign_in_dialog.open())
            sign_in_button.add_widget(sign_in_text)
            self.screen.ids.screen_3.add_widget(sign_in_button)
            self.screen.ids.screen_3.add_widget(reg_button)
        return self.screen
        
    
    def search(self):
        self.search_status = ''
        if len(self.scroll_search.children) != 0:
            self.scroll_search.remove_widget(self.scroll_search.children[0])
        if self.ORM.id_host ==  None:
            self.screen.ids.screen_2.add_widget(MDLabel(text='No internet connection',halign="center"))
        else:
            if self.screen.ids.search_field.text != "" and self.search_status == '':
                self.track_list = self.ORM.search_request(self.screen.ids.search_field.text)
                
                self.list_of_buttns_search = StackLayout(orientation='lr-tb',size_hint=(1,None), pos_hint={'top':0.9,}, height=str(int(self.height_window)/8*(len(self.track_list)))+'dp',spacing = 10)
                
                for track_index in range(0,len(self.track_list)):
                    track_str_index ='track_num_'+ str(track_index)
                    track = self.track_list[track_index]
                    list_button= f'''
BaseButton:
    size_hint:0.95,None
    id:{track_str_index}
    height:{int(self.height_window)/8}
    line_color:1,1,1,1
    md_bg_color:1,1,1,1
    halign:'left'
    valign:'top'
    on_release:app.start_play('http://{self.ORM.host[self.ORM.id_host]}:8000{str(self.track_list[track_index]['track'])}','{self.track_list[track_index]['name']}')
    MDTextButton:
        text:'{track['name']}'
        padding:{(Window.size[0]/100)*25},0
    AsyncImage:
        source:'{str(track['track_img'])}'
        size_hint:.2,1
        pos_hint_x:0
        pos_hint_y:0
        keep_ratio:False
        allow_stretch:True
        fit_mode:'contain'
                '''
                    self.list_of_buttns_search.add_widget(Builder.load_string(list_button))
                self.scroll_search.add_widget(self.list_of_buttns_search)
                
                                      
    
    def register_user(self):
        
        login = self.registform.ids.registr_login.text
        password = self.registform.ids.registr_password.text
        reset_password = self.registform.ids.registr_reset_password.text
        email = self.registform.ids.registr_email.text
        if reset_password != password: 
            print(reset_password,password)
            return print('пароль не збігається')
        responce = self.ORM.register_user(login,password,email)
        print(responce.text)
        if responce.status_code == 201:
            self.registr_dialog.dismiss(force=True)
        
    def login_user(self):
        
        login = self.loginform.ids.login_login.text
        password = self.loginform.ids.login_password.text
        responce = self.ORM.login_user(login,password)
        print(responce.text)
        if responce.status_code == 200:
            self.sign_in_dialog.dismiss(force=True)
        elif responce.status_code == 400:
            print('Podymai eshe')
        
    def start_play(self,track_adress,track_name):
        if self.status_player == 'played':
            self.sound.stop()
            self.sound.unload()
            self.sound = SoundLoader.load(self.Player.get_track(track_adress,track_name))
            self.time_track = 0
            self.sound.play()
            self.status_player = 'played'
            self.text_track.text = track_name
        else:
            player = MDFloatLayout(md_bg_color=(.95, .95, .95, 1),pos_hint={'x':.0,'y':.105},size_hint=(1,.08),radius=(10,10,0,0),line_color=(0,0,0,0))
            self.text_track = MDLabel(text=track_name,padding=(20,),pos_hint={'x':0,'y':0})
            self.action_btn = MDFloatingActionButton(icon='pause', on_press=self.action_track_stop, halign='center',pos_hint={'center_x':.95,'y':0}, icon_color='black', shadow_color=(.95, .95, .95, 1),type='standard',md_bg_color=(.95, .95, .95, 1))
            player.add_widget(self.text_track)
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
               
        
''''''


if __name__ == '__main__':
   
    MyApp().run()
