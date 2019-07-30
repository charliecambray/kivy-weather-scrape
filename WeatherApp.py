import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from time import gmtime, strftime

from bs4 import BeautifulSoup
import requests
url = 'https://darksky.net/forecast/48.8566,2.3515/si12/en'
response = requests.get(url)
soup = BeautifulSoup(response.content,'html.parser')
spans = soup.find_all('span', {'class' : 'summary swap'})
print(spans[0].text)

Window.size = (800, 400)


class MyGrid(Widget):
    wImage = ObjectProperty(None)
    wText = ObjectProperty(None)
    tText = ObjectProperty(None)

    def wCheck(self, *args):
        
        formatT = ".png"
        cloudT = "Cloudy"
        sunT = "Clear"
        rainT = "Rain"
        wList = [cloudT,sunT,rainT]

        temptext = spans[0].text
        for item in wList:
            if item in temptext:
                self.wImage.source = "{}{}".format(item, formatT)
           
        self.wText.text = spans[0].text.replace(".", "") + ' in Paris'

    def timeCall(self, *args):
        
        timeText = str(strftime("%d/%m/%Y    %H:%M:%S", gmtime()))
        self.tText.text = timeText 
        

class WeatherApp(App):
    def build(self):
        mg = MyGrid()
        Clock.schedule_once(mg.wCheck)
        Clock.schedule_interval(mg.wCheck, 60)
        Clock.schedule_interval(mg.timeCall, 1)
        return (mg)

if __name__ == '__main__':
    WeatherApp().run()



