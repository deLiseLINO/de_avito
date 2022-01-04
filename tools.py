import threading
import json
import requests



def update_proxy():
    with open("proxies.json") as f:
        proxies = json.load(f)
    for proxy in proxies:
        try:
            requests.get("https://www.avito.ru", proxies=proxy)
            print(proxy)
            return proxy
        except: pass

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec) 
        func()  
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

def save_users_to_json(users):
    json_list = []

    for user in users:
        u = [user.id, user.urls, user.is_working]
        json_list.append(u)

    with open("clients.json", "w") as f:
        json.dump(json_list, f)
    print("JSON saved")


def replace_trash(message):
    start = message.find('-')
    end = message.find("?")

    if start != -1:
        result = message[:start]
    else:
        result = message
    if end != -1:
        result += message[end:]

    return result


def get_proxy():
    import json

    proxy = requests.get(
        'https://gimmeproxy.com/api/getProxy?country=RU&get=true&supportsHttps=true&protocol=http')
    proxy_json = json.loads(proxy.content)
    if proxy.status_code != 200 and 'ip' not in proxy_json:
        raise requests.RequestException
    else:
        proxy = 'http://' + proxy_json['ip'] + ':' + proxy_json['port']
        print(proxy)
        return proxy
