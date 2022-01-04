import threading
import tools
from consts import HELP_TEXT, INTERVAL
from avito_parser import Parser
import keyborads

from random import randint
from time import sleep

class User:
    def __init__(self, id, urls, vkbot, is_working=False):
        self.parser = Parser()
        self.vk = vkbot
        self.id = id
        self.urls = urls
        self.is_working = is_working
        self.in_menu = False
        #self.cache = dict()
        self.cache = []
        #if self.is_working == True:
            #sleep(randint(1, 15) / 10)
        if (self.id != None):
            tools.set_interval(self.check_and_send_data, INTERVAL)

    def menu_check(self):
        while True:
            event = self.vk.check_messages()
            if event.user_id == self.id:
                return event.text

    def check_and_send_data(self):
        if len(self.cache) >= 50:
            del self.cache[0]
        if self.is_working == True and self.in_menu == False:
            #print(self.id, len(self.cache))
            for url in self.urls:
                if url != None:
                    #sleep(randint(10, 20) / 10)

                    sleep(randint(1, 15) / 10)
                    # text, text2, items_count self.cache = self.parser.update_data(url)
                    # if text != "":
                    #     self.vk.send_message(self.id, text, None)
                    #     print(f"check_and_send_data complete. ID: {self.id} Items: {items_count}")
                    # if text2 != "": self.vk.send_message(self.id, text2, None)
                    items = self.parser.update_data(url)

                    text = ""
                    for item in items:
                        if item.url not in self.cache:
                            self.cache.append(item.url)
                            if len(text) < 4096:
                                text += item.price + " " + item.title+ "\n" + item.url + "\n\n"
                        # else:
                        #     self.cache[item.url] += 1
                        #     if self.cache[item.url] >= 60 / INTERVAL:
                        #         del self.cache[item.url]
                    if text != "":
                        self.vk.send_message(self.id, text, None)


    def send_old_items(self, url):
        text = ''
        items = self.parser.update_data(url, False)
        items.reverse()
        if len(items) == 0:
            self.vk.send_message(self.id, "Бан на авито", None)
        else:
            count = 0
            for item in items:
                if len(text) < 3900:
                    text += item.price + " " + item.title+ "\n" + item.url + "\n\n"
                    #print(len(item.price + " " + item.title+ "\n" + item.url + "\n\n"))
                    count += 1
                else:
                    q = 1
            self.vk.send_message(self.id, text, None)


    def change_url_menu(self, url_id=0):
        self.vk.send_message(self.id,
                        "Перейди по адресу avito.ru, выбери город, категорию и отправь мне итоговую ссылку из браузера",
                        keyborads.change_url)
        self.in_menu = True
        while True:
            message = self.menu_check()
            if message.lower() == "отмена":
                self.vk.send_message(self.id, f"Хорошо, категория остаётся без изменений")
                self.in_menu = False
                return
            #message = tools.replace_trash(message)

            if self.parser.check_if_url_is_correct(message):
                url = message.replace("https://", "")
                url = url.replace("www.", "")
                url = url.replace("m.", "")
                self.urls[url_id] = url
                self.vk.send_message(self.id, f"Новая категория: {self.urls[url_id]}")
                self.in_menu = False
                return
            else:
                self.vk.send_message(self.id, "Неккоректная ссылка, попробуй ещё раз", keyborads.change_url)

    def manager_menu(self):
        self.in_menu = True
        urls_list = []
        for i in range(4):
            urls_list.append(self.urls[i])
            if urls_list[i] == None:
                urls_list[i] = "Не определено"

        menu_text = f"Для изменения/удаления категории нажми соответствующую ей клавишу\n\n1 - {urls_list[0]}\n2 - {urls_list[1]}\n3 - {urls_list[2]}\n4 - {urls_list[3]}\n\nОтмена - выйти из меню выбора категории"
        self.vk.send_message(self.id, menu_text, keyborads.manager_menu)
        while True:
            message = self.menu_check().lower()
            if message == "1":
                self.url_manager_menu(int(message) - 1)
                return
            elif message == "2":
                self.url_manager_menu(int(message) - 1)
                return
            elif message == "3":
                self.url_manager_menu(int(message) - 1)
                return
            elif message == "4":
                self.url_manager_menu(int(message) - 1)
                return
            elif message == "отмена":
                self.vk.send_message(self.id, HELP_TEXT)
                self.in_menu = False
                return
            else:
                self.vk.send_message(self.id, menu_text, keyborads.manager_menu)

    def url_manager_menu(self, url_id):
        manager_text = "Изменить - изменить ссылку категории\nПроверить - отправить объявления с первой страницы\nУдалить - удалить категорию"
        self.vk.send_message(self.id, manager_text, keyborads.url_manager_menu)
        while True:
            message = self.vk.check_messages().text.lower()
            if message == "изменить":
                self.change_url_menu(url_id)
                return
            elif message == "проверить":
                url = self.urls[url_id]
                if url != None:
                    self.send_old_items(url)
                else:
                    self.vk.send_message(self.id, "Нельзя проверить категорию, которой не существует", keyborads.url_manager_menu)

            elif message == "удалить":
                self.vk.send_message(self.id, f"Категория {url_id + 1} была успешно удалена")
                self.urls[url_id] = None
                self.in_menu = False
                return
            elif message == "отмена":
                self.vk.send_message(self.id, HELP_TEXT)
                self.in_menu = False
                return
            else:
                self.vk.send_message(self.id, manager_text, keyborads.url_manager_menu)


    def main_menu(self, message):
        if message != None:
            #print(f'Получено сообщение от: {from_id}\nс текстом: {message}')
 
            if self.in_menu == False:
                if message == "on":
                    self.is_working = True
                    urls_str = ""
                    for url in self.urls:
                        if url != None: urls_str += url + "\n"

                    self.vk.send_message(self.id,
                                    f"Отлично! Теперь я буду присылать тебе все новые объявления, которые будут публиковаться по ссылкам\n{urls_str}")
                    # client.check_and_send_data()

                elif message == "off":
                    self.is_working = False
                    self.vk.send_message(self.id,
                                    "Если снова захочешь чтобы я уведомлял тебя о новых объявлениях, нажми или набери ON")

                elif message == "изменить категорию":
                    t = threading.Thread(target=self.change_url_menu, name="change_url_menu")
                    t.start()
                elif message == "меню категорий":
                    t = threading.Thread(target=self.manager_menu, name="manager_menu")
                    t.start()

                # elif message == "/update_proxy":
                #     parser.proxy = tools.update_proxy()


                else:
                    self.vk.send_message(self.id, HELP_TEXT)
            # if is_client == False:
            #     if message == "start" or message == "начать":
            #         start_text = f"Для начала нужно выбрать город и категорию, для этого нажми на Изменить категорию. По умолчанию я буду использовать эту ссылку {default_url},\n объявления будут проверяться по ней\n\n" + help_text
            #         vk.send_message(from_id, start_text)
            #         users.append(User(from_id, [default_url, None, None, None]))
            #     else:
            #         vk.send_message(from_id, "Набери или нажми Start", None)



