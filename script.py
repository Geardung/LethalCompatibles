import os, ujson, time

config = {
    "path_to_game": "Z:\SteamLibrary\steamapps\common\Lethal Company",
    "now_version": "0.5"
}

width = 80

server_config = {
    "label": "Санин сервер",
    
    "ip": "176.119.156.94",
    "port": 21,
    
    "user": "lethal",
    "password": "kiragay"
}

server_modpacks: list[str]
now_server: dict[str, str]
servers:list[server_config] = []

def connect_to_server(hz: dict):
    print("Устанавливаем соединение с " + hz["ip"])
    
    from ftplib import FTP
    
    with FTP(host=hz["ip"]) as ftp:
        
        ftp.login(hz["user"], hz["password"])
        ftp.cwd("modpacks")
        all_files = ftp.nlst()
        print(all_files, ftp.pwd())
        server_modpacks = [x[0:-4] for x in all_files if x.endswith(".zip")]
        print(server_modpacks)
        ftp.close()
        
    return server_modpacks
    
def select_menu(server_modpacks):
    a = "0"
    
    while True:
        cls()
        
        if a.isdigit():
            
            if a == "1": install_modpack_menu(server_modpacks)
            elif a == "2": 
                
                server_modpacks.append(create_modpack_menu())
                   
        print("#"+"".center(width, "=")+"#")
        print("#"+"  _        _   _         _    ___                      _   _ _    _         ".center(width, " ")+"#")
        print("#"+" | |   ___| |_| |_  __ _| |  / __|___ _ __  _ __  __ _| |_(_) |__| |___ ___ ".center(width, " ")+"#")
        print("#"+" | |__/ -_)  _| ' \/ _` | | | (__/ _ \ '  \| '_ \/ _` |  _| | '_ \ / -_|_-< ".center(width, " ")+"#")
        print("#"+" |____\___|\__|_||_\__,_|_|  \___\___/_|_|_| .__/\__,_|\__|_|_.__/_\___/__/ ".center(width, " ")+"#")
        print("#"+"                                           |_|                              ".center(width, " ")+"#")
        print("#"+"".center(width, "=")+"#")
        print("#"+(" Модпак сервер: " + now_server["label"]+" ").center(width, " ")+"#")
        print("#"+(" Модпаков: "+str(len(server_modpacks))+" ").center(width, " ")+"#")
        print("#"+"".center(width, "-")+"#")
        print("#"+" 1. Установить модпак ".center(width, " ")+"#")
        print("#"+" 2. Опубликовать модпак ".center(width, " ")+"#")
        print("#"+"".center(width, "=")+"#")
        
        a = input("\nВыберите действие: ")

def create_modpack_menu():
    
    import psutil
    if "Lethal Company.exe" in (p.name() for p in psutil.process_iter()):
        
        print("Пока LethalCompany запущена, я не смогу собрать сборку :(")
        if input("Завершить процесс? [Yes/No]: ").lower().startswith("y"):
            
            parent = [p for p in psutil.process_iter() if p.name() == "Lethal Company.exe"][0]
            
            
            #parent = psutil.Process([p.pid for p in psutil.process_iter() if p.name == "Lethal Company.exe"][0])
            for child in parent.children(recursive=True):  # or parent.children() for recursive=False
                child.kill()
            parent.kill()
        else: return cls()

    from packer import ModpackLoader
    
    instance = ModpackLoader(now_server["ip"],
                             now_server["user"],
                             now_server["password"])
    
    return instance.create_n_upload_new_modpack()

def install_modpack_menu(server_modpacks):
    a = "0"
    
    if len(server_modpacks) == 0: 
        print("\nОтсутствуют модпаки на текущем сервере!\n")
        time.sleep(1.5)
        return select_menu(server_modpacks)
    
    import psutil
    if "Lethal Company.exe" in (p.name() for p in psutil.process_iter()):
        
        print("Пока LethalCompany запущена, я не смогу собрать сборку :(")
        if input("Завершить процесс? [Yes/No]: ").lower().startswith("y"):
            
            parent = [p for p in psutil.process_iter() if p.name() == "Lethal Company.exe"][0]
            
            
            #parent = psutil.Process([p.pid for p in psutil.process_iter() if p.name == "Lethal Company.exe"][0])
            for child in parent.children(recursive=True):  # or parent.children() for recursive=False
                child.kill()
            parent.kill()
        else: return cls()
        
    a = ""
    
    while True:
        cls()
        
        if a.isdigit():
            from packer import ModpackLoader
            if a == "0": select_menu(server_modpacks)
            
            if a in server_modpacks: 
                ModpackLoader(now_server["ip"],
                             now_server["user"],
                             now_server["password"]).install_modpack(a)
                select_menu(server_modpacks)
            
            elif int(a)-1 in range(len(server_modpacks)): 
                ModpackLoader(now_server["ip"],
                              now_server["user"],
                              now_server["password"]).install_modpack(server_modpacks[int(a)-1])
                select_menu(server_modpacks)

        print("#"+"".center(width, "=")+"#")
        print("#"+"  __  __         _               _       ".center(width, " ")+"#")
        print("#"+" |  \/  |___  __| |_ __  __ _ __| |__ ___".center(width, " ")+"#")
        print("#"+" | |\/| / _ \/ _` | '_ \/ _` / _| / /(_-<".center(width, " ")+"#")
        print("#"+" |_|  |_\___/\__,_| .__/\__,_\__|_\_\/__/".center(width, " ")+"#")
        print("#"+"                  |_|                    ".center(width, " ")+"#")
        print("#"+"".center(width, "=")+"#")
        print("#"+(" Модпак сервер: " + now_server["label"]+" ").center(width, " ")+"#")
        print("#"+(" Модпаков: "+str(len(server_modpacks))+" ").center(width, " ")+"#")
        print("#"+"".center(width, "-")+"#")
        for ind, modpack in enumerate(server_modpacks):
            print("#"+ (" "+str(ind+1)+". " + modpack +" ").center(width, " ")+"#")
        print("#"+"".center(width, "=")+"#")
        
        a = input("\nВведите модпак для скачки (\"0\" чтобы назад): ")



def cls():
    os.system('cls' if os.name=='nt' else 'clear')

if __name__ == "__main__":
    cls()
    
    if not os.path.exists("./configs"): os.mkdir("./configs")
    
    print("Проверка главного конфига")
    
    if not os.path.exists("./configs/main.json") or open("./configs/main.json", "r", encoding="utf-8").read() == "": 
        
        print("- Отсутствует. Инициализируем новый")
        
        with open("./configs/main.json", "w", encoding="utf-8") as f:
            while True:
                
                print("Вам необходимо ввести полный путь до корневой папки Lethal Company")
                a = input("\n: ")
                if os.path.exists(a + "/Lethal Company.exe"):
                    config["path_to_game"] = a
                    break
                print("Путь не существует, попробуйте снова")
                
            f.write(ujson.dumps(config, ensure_ascii=True, encode_html_chars=True))
    else:
        print("- Присутствует")
        
        exists_json:dict = ujson.loads(open("./configs/main.json", "r", encoding="utf-8").read())
        
        print("Проверяем, нужно ли обновление зависимостей?")
        
        if float(exists_json.get("now_version", "0.1")) < float(config["now_version"]):
            print("= Версия новая, обновляем зависимости")
            os.system("py -m pip install -r reqs.txt")
            
            with open("./configs/main.json", "w", encoding="utf-8") as f:
                exists_json.__setattr__("now_version", config["now_version"])
                f.write(ujson.dumps(exists_json, ensure_ascii=True, encode_html_chars=True))
                f.close()
            
        
            
    
    if not os.path.exists("./configs/176.119.156.94.json"):
        with open("./configs/176.119.156.94.json", "w", encoding="utf-8") as f:
            f.write(ujson.dumps(server_config))
    
    ###
    ###
    ###
    
    for file in os.listdir("./configs"):
        
        if file == "main.json": continue
        
        if file.count(".") == 4 and file.endswith(".json"): 
            
            with open("./configs/" + file, "r", encoding="utf-8") as f:
                
                f:dict = ujson.loads(f.read())
                
                servers.append({
                    "label": f.get("label", "Default label"),
                    "ip": f.get("ip", "176.119.156.94"),
                    "port": f.get("port", 21),
                    
                    "user": f.get("user", "lethal"),
                    "password": f.get("password", "kiragay"),
                })

    ###
    ###
    ###
    
    if len(servers) == 0: print("Конфигов серверов нема, попробуйте удалить папку configs, чтобы синициализировался основной сервер")
    elif len(servers) == 1:
        print("Так-как сервер всего один, то подключаемся к нему...")
        now_server = servers[0]
        
    server_modpacks = connect_to_server(now_server)
    select_menu(server_modpacks)
        
    