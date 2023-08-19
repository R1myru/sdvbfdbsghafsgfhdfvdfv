import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import threading
import telebot

kivy.require('1.11.1')


class TelegramBotApp(App):
    def build(self):
        self.title = 'Управление телеграм-ботом'
        self.token_entry = TextInput(hint_text='Токен бота')
        self.start_button = Button(text='Запустить бота', on_press=self.start_bot)
        self.stop_button = Button(text='Остановить бота', on_press=self.stop_bot)
        self.username_entry = TextInput(hint_text='Username получателя', multiline=False)
        self.message_entry = TextInput(hint_text='Сообщение', multiline=False)
        self.send_button = Button(text='Отправить', on_press=self.send_message)

        layout = GridLayout(cols=2, spacing=10, padding=20)
        layout.add_widget(self.token_entry)
        layout.add_widget(self.start_button)
        layout.add_widget(self.stop_button)
        layout.add_widget(self.username_entry)
        layout.add_widget(self.message_entry)
        layout.add_widget(self.send_button)

        return layout

    def start_bot(self, instance):
        threading.Thread(target=self.run_bot).start()

    def run_bot(self):
        bot_token = self.token_entry.text
        self.bot = telebot.TeleBot(bot_token)

        @self.bot.message_handler(commands=['start'])
        def handle_start(message):
            self.bot.send_message(message.chat.id, "Привет! Я бот. Приятно познакомиться.")

        self.bot.polling(none_stop=True)

    def stop_bot(self, instance):
        self.bot.stop_polling()

    def send_message(self, instance):
        username = self.username_entry.text
        message_text = self.message_entry.text
        try:
            response = self.bot.send_message(username, message_text)
            if response:
                popup = Popup(title='Отправлено', content=Label(text=f'Сообщение отправлено пользователю {username}'),
                              size_hint=(None, None), size=(300, 200))
                popup.open()
        except Exception as e:
            popup = Popup(title='Ошибка', content=Label(text=f'Ошибка при отправке сообщения: {e}'),
                          size_hint=(None, None), size=(300, 200))
            popup.open()

    def show_send_message_elements(self, instance):
        self.username_label.opacity = 1
        self.username_entry.opacity = 1
        self.message_label.opacity = 1
        self.message_entry.opacity = 1
        self.send_button.opacity = 1


if __name__ == '__main__':
    TelegramBotApp().run()
