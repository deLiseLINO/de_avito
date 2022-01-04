import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from consts import TOKEN
from keyborads import main
from requests import exceptions

class VkBot:
    def __init__(self):
        self.vk = vk_api.VkApi(token=TOKEN)
        self.longpool = VkLongPoll(self.vk)

    def send_message(self, id, text, keyboard=main):
        self.vk.method("messages.send", {"peer_id": id, "random_id": 0, "message": text, "keyboard": keyboard})

    def check_messages(self):  # main method
        try:
            for event in self.longpool.listen():
                if event.type == VkEventType.MESSAGE_NEW:
                    if event.from_user != event.from_me:
                        return event
        except exceptions.ReadTimeout:
            print("Read time out error")