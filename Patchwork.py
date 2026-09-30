import tkinter as tk, random,time,pyaudio,pyautogui,pyttsx3,os,socket,speech_recognition,yagmail,requests,webbrowser
from dotenv import load_dotenv , dotenv_values


load_dotenv()
TestVar = os.getenv("Key")

def is_connected():
    try:
        
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False




class MainGui:
    def __init__(self):
        

        self.root = tk.Tk()
        self.root.title("Patchwork (Early Dev)") # Title of Gui (Temporary until image)
        self.main_frame = tk.Frame(self.root) # keep images/labels seperate from buttons
        self.main_frame.pack(padx=20, pady=20)

        self.image = tk.PhotoImage(file="Logo.png")
        self.imgHolder = tk.Label(self.main_frame, image=self.image)
        self.imgHolder.pack()

        self.icon = tk.PhotoImage(file="Logo.png") # Changes little icon
        self.root.iconphoto(True, self.icon)
        self.root.geometry("500x800") # size obviousley
        self.root.resizable(False,False) # No more resizing

        self.Label = tk.Label(self.main_frame,text = "Your Using Patchwork",font=("Arial",10)) # Not hard tbh

        self.Label.pack(pady=10) # Pady moves text on y axis padyx on x
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        # Main Gui Buttons
        tk.Button(self.button_frame,text="Email",command=lambda: EmailHandler(self.root)).grid(row=0, column=0)
        tk.Button(self.button_frame,text="Weather",command=lambda: WeatherApi(self.root)).grid(row=0, column=1)
        tk.Button(self.button_frame,text="Dictionary",command= lambda: DictionaryApi(self.root)).grid(row=0, column=2)
        tk.Button(self.button_frame,text="Smart Home",command= lambda:None).grid(row=0, column=3)
        tk.Button(self.button_frame,text="WebSearch",command= lambda:WebSearch()).grid(row=1, column=0)
        tk.Button(self.button_frame,text="Screenshot",command=lambda: Screenshot(self.root)).grid(row=1, column=1)
        tk.Button(self.button_frame,text="Force Termination",command=lambda: Force_Term(self.root)).grid(row=1, column=2)


        self.root.mainloop() # Must always be last 




class EmailHandler(tk.Toplevel):
    
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Send Email")
        self.geometry("600x450")

        self.label = tk.Label(self, text="Write the email Recipient")
        self.label.pack(pady=10)

        self.Recipient = tk.Entry(self)  
        self.Recipient.pack(pady=10)

        self.label2 = tk.Label(self, text="Write the email to be sent:")
        self.label2.pack(pady=10)

        self.Description = tk.Text(self, height=8)  
        self.Description.pack(pady=10)

        self.button = tk.Button(self, text="Send", command=self.Recive_Mail)
        self.button.pack(pady=10)

    def Recive_Mail(self):
        Sendto = self.Recipient.get()
        msg = self.Description.get("1.0", "end-1c")
        

        yag = yagmail.SMTP(os.getenv("Email"), os.getenv("Email_Pass"))
        
        yag.send(to=Sendto, subject="This email Was sent using Patchwork", contents=msg)
        pyautogui.alert("Success", "Email sent successfully!")
        time.sleep(0.1)
        self.destroy()



class DictionaryApi(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Dictionary")
        self.geometry("800x480")

        
        self.label = tk.Label(self, text="What word are you searching?:")
        self.label.pack(pady=10)

        
        self.searchbox = tk.Entry(self)
        self.searchbox.pack(pady=10)

        
        self.button = tk.Button(self, text="Search", command=self.Lookup)
        self.button.pack(pady=10)

        
        Sentence = []

        
        self.label2 = tk.Label(self, text=Sentence)  

        
        self.label2.pack(pady=10)

    def Lookup(self):
        Part = self.searchbox.get()
        Part2 = os.getenv("Api_3")
        Search = Part2 + Part.lower()
        print(Search)

        Raw_Result = requests.get(Search)
        if Raw_Result.status_code == 200:
            Response = Raw_Result.json()
            print(Response)

            
            definition_count = 0
            Sentence = []
            for entry in Response:
                for meaning in entry.get("meanings", []):
                    for definition in meaning.get("definitions", []):
                        if definition_count < 3:
                            definition_text = definition["definition"]
                            print(f"  - {definition_text}")
                            Sentence.append(definition_text)
                            definition_count += 1
                        else:
                            break
                    if definition_count >= 3:
                        break
                if definition_count >= 3:
                    break

            # update the label 
            self.label2.config(text="\n".join(Sentence))
        else:
            pyautogui.alert("Patchwork ran into a problem receiving this definition")


class WeatherApi(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Weather")
        self.geometry("800x480")
        self.configure(bg= "skyblue")

        self.resizable(False,False)
        self.label = tk.Label(self,text="Enter City Name:").pack(pady=10)
        self.Box = tk.Entry(self)
        self.Box.pack(pady=10)

        self.Forecast_Button = tk.Button(self,text="Get Forecast",command= lambda: self.RetrieveForecast())
        self.Forecast_Button.pack(pady=10)
        self.label2 = tk.Label(self,text="")
        self.label2.pack(pady=10)

        




    def RetrieveForecast(self):
        Location = self.Box.get()
        Url = f"http://api.openweathermap.org/data/2.5/weather?appid={os.getenv('Api_2')}&q={Location}&units=metric"

        response = requests.get(Url).json()

        if response.get("cod") != 200:
            if Location == "":
                self.label2.config(text="...")
                pyautogui.alert(f"Next time try TYPING something ok?")
            else:

                self.label2.config(text="Looks Like you ran into a problem! \nPlease check you spelled it correctly")
                pyautogui.alert(f"Patchwork ran itno a problem Getting the forecast for {Location}")

            
        
        try:
            weather = response["weather"][0]["description"]
            Temp = response["main"]["temp"]
            Feels_Like = response["main"]["feels_like"]
            Wind_Speed = response["wind"]["speed"]
            Humidity = response["main"]["humidity"]
        except KeyError:
            print("Oops")
        
        
        try:
            self.label2.config(text="The weather is: " + weather + "\n" + "Temprature is: " + str(Temp) + "°C" + "\n" + "It feels like: " + str(round(Feels_Like)) + "°C"+ "\n" + f"General Wind Speed in {Location}: {Wind_Speed} m/s  \n Humidity is {Humidity}%")
        except UnboundLocalError:
            print("Bruh")

class WebSearch():
    def __init__(self):
        
        Web = pyautogui.prompt("Enter the Url:")
        webbrowser.open(Web)


class Screenshot(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Screenshot")
        self.geometry("300x200")
        self.resizable(False,False)

        self.button = tk.Button(self,text="Take Screenshot",command=lambda: self.TakeScreen())
        self.button.pack(pady=10)

    def TakeScreen(self):
        self.destroy()
        
        time.sleep(0.4)
        current_time = time.time()
        filename = f"screenshot_{current_time}.png"

        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        Capture = pyautogui.screenshot()
        Capture.save(os.path.join(downloads_path, filename))
        time.sleep(0.2)
        pyautogui.alert(f"Saved to Downloads as: {filename}","Screenshot Saved")


class Force_Term(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("FORCE TERMINATION")
        self.geometry("520x200")
        self.resizable(False,False)

        self.label =tk.Label(self,text="IMPORTANT: Only use this if you have encountered an error\n Errors may occur if incorrectly used")
        self.label.pack(pady=10)
        self.button = tk.Button(self,text="Terminate Program",command=lambda: self.Termination(),width=20,bg="red")
        self.button.pack(pady=10)

    def Termination(self):
        os.abort()
        

    
       
                     
      


    
       













class NoInternetGui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("No Internet Connection")
        self.root.geometry("400x400")
        self.root.resizable(False, False)

        self.image = tk.PhotoImage(file="Gui/No_Wifi.png")  # your image
        self.img_label = tk.Label(self.root, image=self.image)
        self.img_label.pack(pady=20)

        self.retry_button = tk.Button(self.root, text="Retry", command=self.retry_connection)
        self.retry_button.pack(pady=20)

        self.root.mainloop()

    def retry_connection(self):
        if is_connected():
            self.root.destroy()
            MainGui()
        else:
            pyautogui.alert("No Connection", "Still no internet connection!")








# Check for internet
if is_connected():
    MainGui()
else:
    NoInternetGui()








