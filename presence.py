#!/usr/bin/env python

"""
MIT License

Copyright (c) 2021 MUHAMMED ENES KAPLAN

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.



"""





import discord_rpc
import time,os,time,sys
from psutil import process_iter
from pathlib import  Path
import json
from shutil import move

from winshell import desktop,shortcut
import ctypes
import locale
from ctypes.wintypes import MAX_PATH
# from PySimpleGUIQt import SystemTray
# from threading import Thread
  
def CreateLog(log): #Here we keep logs in case we get any errors or for any other reason.
        with open('./log.txt', 'a') as f:
            f.write(str(time.ctime(time.time())) + " : " + log + "\n")
try:
    version = "1.0.0"

    Language = "en_US"
    try:
        Language = locale.getdefaultlocale()[0] #We find the Language of the System.
    except:
        Language = "en_US"
    
    # Language Options for Turkish and English are Available Here
    lanText = {
        "tr_TR" : {
            "sprText" : "{name} Sprite'ını Düzenliyor",
            "objText" : "{name} Objesini Düzenliyor",
            "anmcurvText" : "{name} Adlı Animasyon Eğrisini Düzenliyor",
            "fntText" : "{name} Adlı Yazı Tipini Düzenliyor",
            "scrText" : "{name} Adlı Script(Kod Dosyası) Düzenliyor",
            "seqText" : "{name} Adlı Sequence'i Düzenliyor",
            "sndText" : "{name} Adlı Ses Dosyasını Düzenliyor",
            "rmText" : "{name} Adlı Oda'yı Düzenliyor",
            "editing" : "GameMaker Studio 2",
            "projectPath" : "Proje Konumu",
            "pathIsFound" : "Verdiğiniz Konum Bulunmuştur :)",
            "pathIsNotFound" : "Verdiğiniz Konum Bulunamadı Lütfen Konumu Doğru Girdiğinizden Emin Olun Ve Çift Slash Kullanmayı Unutmayın! örnek: D:\\Documents\\",
            "restartProgram" : "Dosyalarınız Oluşturulmuştur, Programı Kapatıp, Presence.txt Dosyasını Kendinize Göre Düzenleyin ve Tekrar Başlatın. (Bu mesajı değiştirdikten sonra görüyorsanız, yolunuz yanlıştır. sıfırlandı doğru bir yol girip tekrar deneyiniz.)"
        },
        "en_US" : {
            
            "sprText" : "Editing {name} Sprite",
            "objText" : "Editing {name} Object",
            "anmcurvText" : "Editing {name} Curve",
            "fntText" : "Editing {name} Font",
            "scrText" : "Editing {name} Script",
            "seqText" : "Editing {name} Sequence",
            "sndText" : "Editing {name} Sound",
            "rmText" : "Editing {name} Room",
            "editing" : "GameMaker Studio 2",
            "projectPath" : "Project Path",
            "pathIsFound" : "Your Location Has Been Found :)",
            "pathIsNotFound" : "The Location You Provided Was Not Found Please Make Sure You Enter The Location Correctly And Don't Forget To Use Double Slash! example: D:\\Documents\\",
            "restartProgram" : "Your Files have been Created, Close the Program, Edit the Presence.txt File According to You and Start Again. (If you see this message after changing it, your path is wrong. Has been reset, enter a correct path and try again."
            
        }

    }

    try:
        value_ = lanText[Language] # If there is a problem with the language file (If we encounter an Unknown Language)
    except:
        Language = 'en_US' # We Set The Language To English.

    # FUNCTION TO CREATE A WARNING BOX
    def Mbox(title, text, style): #Alert Box is displayed.
        return ctypes.windll.user32.MessageBoxW(0, text, title, style)



    ## For Gamemaker Projects, we access the default project location.
    dll = ctypes.windll.shell32
    buf = ctypes.create_unicode_buffer(MAX_PATH + 1)
    if dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False):
        path = buf.value+"\\GameMakerStudio2"



    def WriteSettings():#open the Presence Settings File.
        f = open("./PresenceSettings.txt", "w")
        _tmp = {}
        _tmp['YOUR_PROJECTS_PATH'] = path
        _tmp['LANGUAGE'] = Language
        _tmp['STARTUP'] = 0

        # f.write("{\n"+"\"YOUR_PROJECTS_PATH\" : \"{path}\",\n\"LANGUAGE\" : \"{Language}\"".format(path = path,Language = Language)+"\n}")
        f.write(str(json.dumps(_tmp, indent=4)))
        f.close()
        exit()

    # PRESENCE SETTINGS
    if os.path.exists("./PresenceSettings.txt"):
        try:
            f = open("./PresenceSettings.txt", "r")
            data = json.load(f)
            # strr = f.read()
            path = data['YOUR_PROJECTS_PATH']
            if os.path.exists(path):
                Mbox(lanText[Language]['projectPath'], lanText[Language]['pathIsFound'],0)
                CreateLog("Path is available")
            else:
                Mbox(lanText[Language]['projectPath'], lanText[Language]['pathIsNotFound'],0)
                CreateLog("Path is unavailable, please use // in path.")
                exit()
            Language = data['LANGUAGE']
            Startup = data['STARTUP']

            f.close()
        except Exception as e:
            CreateLog(e)
            WriteSettings()

    else:
        Mbox(lanText[Language]['projectPath'],lanText[Language]['restartProgram'],0)
        CreateLog("created files. change files and restart program.")
        WriteSettings() 
        







    CreateLog("\n\n\nDiscordRich Presence Restarted")

    # Prsence File Creation
    Lappdata = os.getenv('LOCALAPPDATA')
    gmsPath = Lappdata+"\\GameMakerStudio2"
    presenceText = "\\presence.txt"

    if not os.path.exists(gmsPath+presenceText):
        # f = open(gmsPath+presenceText, "a")
        # f.write('{"YourClientId": 794303492792778772}') 
        ClientId = 794303492792778772 #Here I am writing my own client_id for Pictures And Presence. You can change it as desired.

    else:
        ClientId = 794303492792778772 #Here I am writing my own client_id for Pictures And Presence. You can change it as desired.
        # f = open(gmsPath+presenceText, "r")
        # j = json.load(f)
        # ClientId = j['YourClientId']




    ## Icons by Project.
    icons = {
        "sprites": ["sprite_icon",lanText[Language]["sprText"]],
        "objects": ["object_icon",lanText[Language]["objText"]],
        "animcurves": ["animcurve_icon",lanText[Language]["anmcurvText"]],
        "fonts": ["font_icon", lanText[Language]["fntText"]],
        "scripts": ["script_icon",lanText[Language]["scrText"]],
        "sequences": ["sequence_icon", lanText[Language]["seqText"]],
        "sounds": ["sound_icon",lanText[Language]["sndText"]],
        "rooms": ["room_icon", lanText[Language]["rmText"]]

    }

    start = time.time() #I keep a timer to see how long we spend time on the project.

    # Here, we take whatever parts of the project we changed at last.
    def GetLastChangedFile(path):
        ChangedFiles = []
        for folder in os.listdir(path):
            folderPath = str(path)+"\\"+folder
            if os.path.isdir(folderPath):
                # print(folderPath, len(os.listdir(folderPath) ))
                if len(os.listdir(folderPath) ) != 0:
                    pathInFile = sorted(Path(folderPath).iterdir(), key=os.path.getmtime)[-1]
                    # print(pathInFile)
                    ChangedFiles.append(pathInFile)
                # for folderData in os.listdir(folderPath):
                #     gameAssetsFolder = folderPath+"\\"+folderData
                #     print(folderPath)
                    # if os.path.isdir(gameAssetsFolder):
                    #     print(gameAssetsFolder)
                    #     if os.path.getsize(gameAssetsFolder):
                    #         try:
                    #             pathInFile = sorted(Path(gameAssetsFolder).iterdir(), key=os.path.getmtime)[-1]
                    #             ChangedFiles.append(pathInFile)
                    #         except:
                    #             pass
                    #         # ChangedFiles.append(pathInFile)
        changed_times = {}
        for chfiles in ChangedFiles:
            
            if os.path.exists(chfiles):
                ChangedTime = Path(chfiles).stat().st_mtime
                # changed_times.append({ChangedTime: chfiles})
                changed_times[str(chfiles)] = ChangedTime
            else:
                return False
                break

        
        
        sortedtime = sorted(changed_times.values())
        try:
            return(list(changed_times.keys())[list(changed_times.values()).index(sortedtime[-1])])
        except Exception as e:
            CreateLog("Line - "+str(e))
            exit()
            return(False)


    # menu_def = ['BLANK', ['Exit', 'About']] 


    # tray = SystemTray(menu=menu_def, filename=r'icon.ico') 

    # def Tray():
    #     print("2")  
    #     menu_item = tray.Read()  
    #     print(menu_item)  
    #     if menu_item == 'Exit':  
    #         exit()
    #     elif menu_item == 'About':
    #         Mbox("About",f"Producer:EnesKp3441#3573\nSupporters: Lord#4300 , Furkan Karabudak#2488\nVersion: {version}",0)


    while True:  # The event loop  
        
        while 1:
            # Checks if a program named Gamemaker Is Running
            isProgramRuneer = ("GameMakerStudio.exe" in (p.name() for p in process_iter()))


            # DOCUMENTS
            if(isProgramRuneer):
                
                    isFile              = os.path.isdir(path)
                    pathInFile = sorted(Path(path).iterdir(), key=os.path.getmtime)[-1]

                    ## SETTINGS FILE OF THE PROJECT TO RECEIVE GAMEMAKER INFORMATION
                    optionsFile = str(pathInFile)+"\\options\\windows\\options_windows.yy"

                    # RECEIVING THE LAST CHANGED FILE
                    LastFile = GetLastChangedFile(pathInFile)
                    while LastFile == 0:
                        LastFile = GetLastChangedFile(pathInFile)


                    # READING THE DATA OF THE SETTINGS FILE
                    with open(optionsFile, "r", encoding='utf8') as f:
                        # d = json.load(f)
                        json_str = f.read()
                        length = len(json_str)
                        json_strInd = json_str.find(",",length-5, length)
                        real_jsonstring = json_str[0 : json_strInd : ] + json_str[json_strInd + 1 : :]
                        js = json.loads(real_jsonstring)
                        # We receive Game Information from Game Maker.
                        GameName = js["option_windows_display_name"]
                        GameVersion = js["option_windows_version"]
                        GameDesc = js["option_windows_description_info"]
                        GameCompany = js["option_windows_company_info"]

                        try:
                            if LargeImageText != None:
                                # print("L",LargeImageText,"File", LastFile.split("\\")[-1])
                                if LargeImageText != LastFile.split("\\")[-1]:
                                    ffff  = LastFile.split("\\")[-1]
                                    elapseTime = time.gmtime(time.time()-start)
                                    sec = elapseTime.tm_sec
                                    hour = elapseTime.tm_hour
                                    min_ = elapseTime.tm_min
                                    print("KOD: 2202")
                                    CreateLog(f"Duration of use: {LargeImageText}"+f"   Time [ Second : {sec}, Miniute: {min_}, Hour : {hour} ]")
                                    CreateLog(f"New Work: {ffff}")
                                    start = time.time()
                        except :
                            pass

                        LargeImageKey = 'sprite_icon'
                        LargeImageText = ''
                        SmallImageKey = ''
                        SmallImageText = ''
                        GameState = GameDesc +" | "+GameCompany
                        GameDetails = GameName+" | "+str(GameVersion)
  

                    # IF YOU ARE EDITING AN OBJECT OR ANYTHING THIS SECTION WILL CHANGE HIS WRITING
                    for key,value in  icons.items():
                        if LastFile.split("\\")[-2].lower() == key.lower():
                            

                            LargeImageKey = value[0]
                            SmallImageKey = 'logo'

                            SmallImageText = lanText[Language]["editing"]
                            GameState      = value[1].format(name = LastFile.split("\\")[-1])
                            LargeImageText = LastFile.split("\\")[-1]
                            GameDetails = GameName


                    if __name__ == '__main__':
                        def readyCallback(current_user):
                            print('Our user: {}'.format(current_user))

                        def disconnectedCallback(codeno, codemsg):
                            print('Discord rich presence connection failed error. Code {}: {}'.format(
                                codeno, codemsg
                            ))
                            if codemsg == "Invalid Client ID":
                                # Mbox('Client id is not correct.', 'Please fill in the Client ID. \"%localappdata% > Gamemaker Studio 2 > presence.txt\", Fix and Restart', 0)
                                CreateLog("Client id is not correct. Please fill in the Client ID. localappdata > Gamemaker Studio 2 > presence.txt")

                        def errorCallback(errno, errmsg):
                            print('An error occurred! Error {}: {}'.format(
                                errno, errmsg
                            ))

                        # Note: 'event_name': callback
                        callbacks = {
                            'ready': readyCallback,
                            'disconnected': disconnectedCallback,
                            'error': errorCallback,
                        }
                        discord_rpc.initialize(str(ClientId), callbacks=callbacks, log=False)

                        discord_rpc.update_presence(
                            **{
                                'details': GameDetails,
                                'start_timestamp': start,
                                'state': GameState,
                                'large_image_key': LargeImageKey,
                                'small_image_key': SmallImageKey,
                                'large_image_text': LargeImageText,
                                'small_image_text': SmallImageText
                            }
                        )

                        

                        discord_rpc.update_connection()
                        time.sleep(2)
                        discord_rpc.run_callbacks()
                        


                        

                        
            else:
                discord_rpc.shutdown()
        
        # Tray()

    discord_rpc.shutdown()
except Exception as e:
    CreateLog("ERROR : "+str(e))


            
            
