from datetime import datetime
import os, requests, sys, shutil, time, threading, random
from pynput import keyboard
from PIL import Image
from io import BytesIO
import pygetwindow as gw


root_dir = os.path.join(os.getcwd(), "screenshots")
like_dir = os.path.join(root_dir, "like")
dislike_dir = os.path.join(root_dir, "dislike")
flag = False
name = None
janelas_iniciais = set(gw.getAllTitles())
janelas_novas = set()


def mkdir(): 
    try:
        os.mkdir(root_dir)
        os.mkdir(like_dir)
        os.mkdir(dislike_dir)
    except:
        pass

def nameJPG():
    hora = datetime.now()
    print_time = hora.strftime("%H:%M:%S")
    print_time = print_time.replace(":", "_")
    return str(os.path.join(root_dir, "screeshoot_" + print_time + ".jpg"))

def showImage(response):
    img = Image.open(BytesIO(response))
    img.show()

def getImage():
    url = "https://thispersondoesnotexist.com"
    screenshotName = nameJPG()
    response = requests.get(url)
    if response.status_code != 200:
        print("connection error")
        return
    with open(screenshotName, "wb") as file:
        file.write(response.content)
        showImage(response.content)
        return screenshotName


def delImage(name):
    try:
        os.remove(name)
    except:
        pass


def somo_amigue_o_no_somo_amigue(op, name):

    if op:
        try:
            shutil.copy(name, like_dir)
            delImage(name)
        except:
            print(f"Screen {name} not found")
    else:
        try:
            shutil.copy(name, dislike_dir)
            delImage(name)
        except:
            print(f"Screen {name} not found")

def first():
    global flag
    if flag:
        return 0
    else:
        flag = True
        return 1
        
def on_press(key):
        global name
        if key == keyboard.Key.left:
            if first():
                name = getImage()
            else:
                somo_amigue_o_no_somo_amigue(0,  name)
                unmatch()
                fechar_janelas()
                name = getImage()

        if key == keyboard.Key.right:
            if first():
                name = getImage()
            else:
                somo_amigue_o_no_somo_amigue(1, name)
                match()
                fechar_janelas()
                name = getImage()

        if key == keyboard.Key.esc:
            listener.stop()
            print("exiting...")
            sys.exit()
        else:
            pass

def monitorar_janelas():
    while True:
        janelas_atualizadas = set(gw.getAllTitles())
        novas_janelas = janelas_atualizadas - janelas_iniciais
        for janela in novas_janelas:
            if janela and janela not in janelas_novas:
                janelas_novas.add(janela)
        time.sleep(1)

def fechar_janelas():
    for janela in janelas_novas:
        try:
            win = gw.getWindowsWithTitle(janela)[0]
            if "explorer" not in win.title.lower():
                win.close()
                print(f"Fechou a janela: {janela}")
        except Exception as e:
            print(f"Não foi possível fechar a janela {janela}: {e}")


def match():
    url = "https://www.tinderpressroom.com/image/43b-matches.png"
    rand = random.randint(0,100)

    if rand > 65:
        response = requests.get(url)
        if response.status_code!= 200:
            return
        imgMatch = Image.open(BytesIO(response.content))
        imgMatch.show()

def unmatch():
    url = "https://thumbs.dreamstime.com/b/oh-no-2508033.jpg"
    rand = random.randint(0,100)

    if rand > 65:
        response = requests.get(url)
        if response.status_code!= 200:
            return
        imgMatch = Image.open(BytesIO(response.content))
        imgMatch.show()

def main():
    mkdir()
    


if __name__ == '__main__':
    main()

    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    
    monitoramento_thread = threading.Thread(target=monitorar_janelas)
    monitoramento_thread.daemon = True
    monitoramento_thread.start()

    listener.join()