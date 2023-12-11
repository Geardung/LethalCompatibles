import os, ujson, time, datetime
from ftplib import FTP
config = {
    "path_to_game": "Z:\SteamLibrary\steamapps\common\Lethal Company",
}

width = 35

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




def let_comp_path_input():
    while True:
        
        print("Вам необходимо ввести полный путь до корневой папки Lethal Company")
        a = input("\n: ")
        if os.path.exists(a + "/Lethal Company.exe"):
            config["path_to_game"] = a
            return a
        print("Путь не существует, попробуйте снова")

def select_server():
    while True:
        
        os.system("clear")

def connect_to_server(hz: dict):
    print("Устанавливаем соединение с " + hz["ip"])
    
    with FTP(hz["ip"]) as ftp:
        
        ftp.login()
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
            elif a == "2": create_modpack_menu()
        
        print("#"+"".center(width, "=")+"#")
        print("#"+" Меню синхронайзера ".center(width, "=")+"#")
        print("#"+"".center(width, "=")+"#")
        print("#"+"".center(width, "-")+"#")
        print("#"+(" Модпак сервер: " + now_server["label"]+" ").center(width, "-")+"#")
        print("#"+(" Модпаков: "+str(len(server_modpacks))+" ").center(width, "-")+"#")
        print("#"+"".center(width, "-")+"#")
        print("#"+" 1. Установить модпак ".center(width, "-")+"#")
        print("#"+" 2. Опубликовать модпак ".center(width, "-")+"#")
        print("#"+"".center(width, "-")+"#")
        print("#"+"".center(width, "=")+"#")
        
        a = input("\nВыберите действие: ")

def create_modpack_menu():
    
    from packer import ModpackLoader
    
    instance = ModpackLoader(now_server["ip"],
                             now_server["user"],
                             now_server["password"])
    
    instance.create_n_upload_new_modpack()

def install_modpack_menu(server_modpacks):
    a = "0"
    
    if len(server_modpacks) == 0: 
        print("\nОтсутствуют модпаки на текущем сервере!\n")
        time.sleep(1.5)
        return select_menu(server_modpacks)
    
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
        print("#"+" Выбор модпака ".center(width, "=")+"#")
        print("#"+"".center(width, "=")+"#")
        print("#"+"".center(width, "-")+"#")
        print("#"+(" Модпак сервер: " + now_server["label"]+" ").center(width, "-")+"#")
        print("#"+(" Модпаков: "+str(len(server_modpacks))+" ").center(width, "-")+"#")
        print("#"+"".center(width, "-")+"#")
        for ind, modpack in enumerate(server_modpacks):
            print("#"+ (" "+str(ind+1)+". " + modpack +" ").center(width, "-")+"#")
        print("#"+"".center(width, "-")+"#")
        print("#"+"".center(width, "=")+"#")
        
        a = input("Введите модпак для скачки (\"0\" чтобы назад): ")



def cls():
    os.system('cls' if os.name=='nt' else 'clear')

if __name__ == "__main__":
    cls()
    
    if not os.path.exists("./configs"): os.mkdir("./configs")
    
    print("Проверка главного конфига")
    
    if not os.path.exists("./configs/main.json"): 
        
        print("- Отсутствует. Инициализируем новый")
        
        with open("./configs/main.json", "w", encoding="utf-8") as f:
            let_comp_path_input()
            f.write(ujson.dumps(config, ensure_ascii=True, encode_html_chars=True))
    else:
        print("- Присутствует")
            
    
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
                    "password": f.get("kiragay", "Default label"),
                })

    if len(servers) == 0: print("Конфигов серверов нема, попробуйте удалить папку configs, чтобы синициализировался основной сервер")
    elif len(servers) == 1:
        print("Так-как сервер всего один, то подключаемся к нему...")
        now_server = servers[0]
        
    server_modpacks = connect_to_server(now_server)
    select_menu(server_modpacks)
        
    