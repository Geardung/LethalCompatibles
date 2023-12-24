import os, datetime, ujson, time, ftplib, shutil, re
from zipfile import ZipFile


class ModpackLoader():
    
    def __init__(self, ip: str, user, password):
        
        if not os.path.exists("./modpacks"): os.makedirs("./modpacks")
        
        self._server_ip: str = ip
        
        self._user:str = user
        self._password:str = password
        
        self._main_config = ujson.loads(open("./configs/main.json", "r").read())
    
    def create_n_upload_new_modpack(self):
        
        name = self.pack_now_modpack()
        
        self.upload_modpack_on_server(name)
        
        return name
    
    def pack_now_modpack(self, name: str = str(int(datetime.datetime.now().timestamp()))):
        
        os.system('cls' if os.name=='nt' else 'clear')
        
        while True:
            a = input(f"Название модпака [Enter чтобы - {name}]: ")
            if a == "": break
            elif not (re.search('[ЁёА-я]', a)) and not(" " in a):
                name = a
                break
            else: print(f"Имя пака [{a}] содержит пробел либо нелатинские символы...")
        
        print("Начинаем создавать модпак: " + name)
        
        
        if not os.path.exists(self._main_config["path_to_game"] + "/Lethal Company.exe"): return self._on_game_path_not_exists()
        print("Путь к игре прописан верно")
        if not os.path.exists(self._main_config["path_to_game"] + "/BepInEx"): return self._on_bepinex_not_exists()
        print("Модлоадер установлен")
        
        def add_in_zip_dir(full_dir: str, local_dir: str, zip: ZipFile):
            
            zip.mkdir(local_dir)
            
            for file_n_dir in os.listdir(full_dir):
                print("| " + local_dir + "/" + file_n_dir)
                if file_n_dir.endswith(".log"): continue
                if os.path.isfile(full_dir + "/" + file_n_dir): zip.write(full_dir + "/" + file_n_dir, local_dir + "/" + file_n_dir)
                else: add_in_zip_dir(full_dir + "/" + file_n_dir, local_dir + "/" + file_n_dir, zip)
            
        with ZipFile("./modpacks/" + name + ".zip", "w", compression=2) as myzip:
            print("Начинаем упаковывать модпак в ./modpacks/" + name + ".zip")
            myzip.setpassword("Geardung".encode("utf-8"))
            
            for file_n_dir in os.listdir(self._main_config["path_to_game"] + "/BepInEx"):
                print("| " + file_n_dir)
                if file_n_dir.endswith(".log"): continue
                if os.path.isfile(self._main_config["path_to_game"] + "/BepInEx" + "/" + file_n_dir): myzip.write(self._main_config["path_to_game"] + "/BepInEx/" + file_n_dir, "BepInEx/" + file_n_dir)
                else: add_in_zip_dir(self._main_config["path_to_game"] + "/BepInEx" + "/" + file_n_dir, "/BepInEx/" + file_n_dir, myzip)
                time.sleep(0.35)
                
            print("Сохраняем сборку")
            myzip.close()
        
        return name
        
    
    def _on_bepinex_not_exists(): pass
    def _on_game_path_not_exists(): pass
    
    
    def upload_modpack_on_server(self, name):
        print("Создаём соединение с сервером...")
        with ftplib.FTP(self._server_ip) as session:
            session.login(user=self._user, passwd=self._password)
            session.cwd("modpacks")
        
            print("Подключились!\nПроверяем наличие модпака с схожим названием...")
            
            if name in [x[0:-4] for x in session.nlst("") if x.endswith(".zip")]:
                if input("Сборка с таким названием уже существует\nПерезаписать? [Yes/No]: ").lower()[0] == "y": session.delete("/home/lethal/modpacks/" + name + ".zip")
                else: return
            else: print("Отлично! Модпака с таким названием нет")
        
            session.storbinary('STOR /home/lethal/modpacks/'+name+".zip", open('./modpacks/'+name+".zip",'rb'))
            session.quit()
            
    #
    #
    #
    
    def install_modpack(self, name): 
        from downloader import download
        
        download([("http://" + self._server_ip + "/modpacks/"+ name + ".zip")],
                 dest_dir="./modpacks")
        
        def on_deletion_error(lstat, path, exc_info):
            
            print("Программа не смогла самостоятельно очистить папку BepInEx'a\nСделайте это самостоятельно, удалив " + self._main_config["path_to_game"]+"/BepInEx")
            
            while os.path.exists(self._main_config["path_to_game"]+"/BepInEx"): input("Нажмите Enter, если вы удалили папку...")
        
        if os.path.exists(self._main_config["path_to_game"]+"/BepInEx"): shutil.rmtree(self._main_config["path_to_game"]+"/BepInEx", onerror=on_deletion_error)
        
        with ZipFile("./modpacks/"+ name + ".zip", "r") as zfile: zfile.extractall(self._main_config["path_to_game"])
        
        print("""
              ⡶⠶⠂⠐⠲⠶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⡶⠶⡶⣶
              ⣗⠀⠀⠀⠀⠀⠀⠀⠉⠛⠿⠿⣿⠿⣿⣿⣿⣿⠿⠿⠿⠟⠛⠉⠁⠀⠀⠀⢠⣿
              ⣿⣷⣀⠀⠈⠛⠢⠥⠴⠟⠂⠀⠀⠀⠉⣛⠉⠁⠀⠐⠲⠤⠖⠛⠁⠀⠀⣐⣿⣿
              ⣿⣿⣿⣦⣄⡀⠀⠀⠀⠀⣀⡠⣤⣦⣿⣿⣿⣆⣴⣠⣀⣀⡀⣀⣀⣚⣿⣿⣿⢳
              ⣧⠉⠙⢿⣿⣿⣶⣶⣾⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢇⣿
              ⣿⣷⡄⠈⣿⣿⣿⣿⣯⣥⣦⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢉⣴⣿⣿
              ⣿⣿⣿⣦⣘⠋⢻⠿⢿⣿⣿⣿⣾⣭⣛⣛⣛⣯⣷⣿⣿⠿⠟⠋⠉⣴⣿⣿⣿⣿
              ⢠⠖⢲⠀⠀⡖⢲⡄⡴⠒⠆⡖⠒⠂⠀⣶⠲⡄⢰⡆⠀⡖⢦⠀⡆⢰⡆⡴⠒⣄
              ⢨⠟⢻⠀⠀⣏⣉⠇⢧⣀⡄⣏⣉⡁⠀⣿⠚⢡⠗⠺⡄⣏⣹⠆⡏⢹⡇⢧⣀⡞
              ⢰⣒⡒⠰⡄⡴⠀⡶⢲⡆⢢⣀⡖⠀⠀⡖⠒⠲⢰⠒⣦⢀⡶⡄⠒⢲⠒⢲⣆⣀
              ⠸⠤⠽⠠⠽⠁⣴⠧⠼⣧⠤⠟⠀⠀⠀⠧⠤⠤⠸⠉⠁⠞⠒⠳⠀⠸⠀⠸⠧⠼
              """)
        import subprocess
        subprocess.run("cmd /c start steam://run/1966720")
        input("Сборка установлена, нажмите Enter...")
        
        return