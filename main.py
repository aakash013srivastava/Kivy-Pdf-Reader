from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import os
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.window import Window
from plyer import notification, tts
#setup graphics
from kivy.config import Config
Config.set('graphics','resizable',0)
from kivy.lang import Builder
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
from kivy.uix.popup import Popup


Builder.load_string("""
<MyWidget>:
    id: my_widget
    
    FileChooserListView:
        id: filechooser
        on_selection: my_widget.talk(filechooser.selection)
""")

class MyWidget(BoxLayout):
    def open(self, path, filename):
        
        with open(os.path.join(path, filename[0])) as f:
            print f.read()

    def selected(self, filename):
        print "selected: %s" % filename[0]
 
    def notify(self):
        try:
            #this notification will pop up on ubuntu as well!'
            notification.notify(title="Kivy Notification",message="Plyer Up and Running!",
        app_name="kivy_test",app_icon="icon.png",timeout=10)
        except:
            print 'error notifiying'
   
 
    def talk(self,file_path):
        try:
            tts.speak(message=self.convert_pdf_to_txt(file_path[0]))
        except:
            print 'cant talk'
            
            
    def convert_pdf_to_txt(self,path):
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        fp = file(path, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos=set()

        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
            interpreter.process_page(page)

            text = retstr.getvalue()

        fp.close()
        device.close()
        retstr.close()
        return text



class MyApp(App):
    def build(self):
        return MyWidget()

if __name__ == '__main__':
    MyApp().run()