from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner

class DropdownMenuApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Создаем Spinner (выпадающий список)
        spinner = Spinner(
            text='Выберите пункт',
            values=('Пункт 1', 'Пункт 2', 'Пункт 3'),
            size_hint=(None, None),
            size=(200, 44),
            pos_hint={'center_x': 0.5}
        )
        spinner.bind(text=self.on_spinner_select)  # Обработка выбора

        layout.add_widget(spinner)
        return layout

    def on_spinner_select(self, spinner, text):
        print(f"Выбран: {text}")

if __name__ == '__main__':
    DropdownMenuApp().run()