import json

def get_button(label, color):
    return {
            "action":{
                "type": "text",
                "payload": json.dumps(""),
                "label": label
            },
            "color": color
        }

def prepare_keyboard(keyboard):
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode("utf-8")
    return str(keyboard.decode("utf-8"))

main = {
    "one_time": False,
    "buttons": [
            [
            get_button(label="ON", color="positive"),
            get_button(label="OFF", color="negative"),
            ],
            [get_button(label="Изменить категорию", color="primary"), get_button(label="Меню категорий", color="primary")]

    ]
}
main = prepare_keyboard(main)

change_url = {
    "buttons": [
        [get_button("Отмена", "secondary")]
    ]
}
change_url = prepare_keyboard(change_url)

manager_menu = {
    "buttons": [
        [get_button("1", "secondary"),
        get_button("2", "secondary"),
        get_button("3", "secondary"),
        get_button("4", "secondary")],
        [get_button("Отмена", "secondary")]
    ]
}
manager_menu = prepare_keyboard(manager_menu)

url_manager_menu = {
    "buttons": [
        [get_button("Изменить", "primary"),
        get_button("Удалить", "negative")],
        [get_button("Проверить", "secondary")],
        [get_button("Отмена", "secondary")]
    ]
}
url_manager_menu = prepare_keyboard(url_manager_menu)

