from tkinter import *
from tkinter import filedialog
import tweepy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

PATH = "C:\Program Files\Chromedriver.exe"

#You need create a app in twitter developers
consumer_key = "Consumer Key of your App in Twitter"
consumer_secret = "Consumer Secret of your App in Twitter"

# App authorization
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
redirect_url = auth.get_authorization_url()

def click():

    def Send():

        def on_after():
            status.set("")

        if (opcion.get() == 1):
            data_text= mensajeText.get(1.0,"end-1c")
            filename = filedialog.askopenfilename()  
            data_img = api.media_upload(filename)
            api.update_status(data_text, media_ids=[data_img.media_id_string])
            status.set("OK")
            etiqueta2.configure(text=status)

            opcion.set(0)
            mensajeText.delete(1.0,"end-1c")
            etiqueta2.after(2000, on_after)

        else:
            data_text= mensajeText.get(1.0,"end-1c")
            api.update_status(data_text)
            status.set("OK")
            etiqueta2.configure(text=status)
            
            mensajeText.delete(1.0,"end-1c")
            etiqueta2.after(2000, on_after)

    #Auto-start verification (selenium)

    user_twitter = entrada_user.get()
    pass_twitter = entrada_pass.get()

    driver_tw = webdriver.Chrome(PATH)
    driver_tw.get(redirect_url)
    time.sleep(2)
    search_user = driver_tw.find_element_by_id("username_or_email")
    search_user.send_keys(user_twitter)
    search_pass = driver_tw.find_element_by_id("password")
    search_pass.send_keys(pass_twitter)
    
    search_allow_button = driver_tw.find_element_by_id("allow")
    search_allow_button.click()

    search_pin = driver_tw.find_element_by_tag_name("code")
    pin_twitter = search_pin.text

    driver_tw.close()

    auth.get_access_token(pin_twitter)
        
    ventana.destroy()

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    #post window

    App= Tk()
    App.title("Alphapruebas para Twitter")
    App.resizable(False, False)
    App.iconbitmap("Images\icontwitter.ico")
    App.config()
    frame = Frame()
    frame.pack()
    frame.config(width="640", height="480") 
    etiqueta = Label(frame, text="Que quieres Publicar?", font=("Calibri", 15))
    etiqueta.grid(column=0, row=1, columnspan=2)
    mensajeText = Text(frame, width=25, height=10)
    mensajeText.grid(column=0, row=2, columnspan=2)
    opcion = IntVar()
    boton = Radiobutton(frame, text="Subir Multimedia", variable=opcion, value= 1)
    boton.grid(pady=5, column=0, row=3, sticky=W)
    boton2 = Button(frame, text="Enviar", command=Send)
    boton2.grid(padx=5, pady=5, ipadx=20, ipady=5, column=0, row=4, columnspan=2)
    status=StringVar()
    etiqueta2 = Label(frame, textvariable=status, font=("Calibri", 15), fg='green')
    etiqueta2.grid(column=1, row=3, stick=W)

#login window
ventana = Tk()
ventana.title("Alphapruebas para Twitter")
ventana.resizable(True, True)
ventana.iconbitmap('Images\icontwitter.ico')
ventana.config()
frame = Frame()
frame.pack()
frame.config(width="640", height="480")
etiqueta = Label(frame, text="Bienvenido,debes iniciar sesion para continuar", font=("Calibri", 15))
etiqueta.grid(column=0, row=0, columnspan=2)
etiqueta_user = Label(frame, text="Usuario", font=("Calibri", 12))
etiqueta_user.grid(column=0, row=3)
entrada_user = Entry(frame, width=25)
entrada_user.grid(column=1, row=3)
etiqueta_pass = Label(frame, text="Contraseña", font=("Calibri", 12))
etiqueta_pass.grid(column=0, row=4)
entrada_pass = Entry(frame, width=25, show="*")
entrada_pass.grid(column=1, row=4)
boton = Button(frame, text="Iniciar Sesion", command=click)
boton.grid(padx=10, pady=10, ipadx=20, column=0, row=5, columnspan=2)

ventana.mainloop()