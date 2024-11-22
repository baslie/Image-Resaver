import sys
import os
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon, QFontDatabase
from PyQt5.QtCore import Qt
from PIL import Image

class ImageResaver(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setAcceptDrops(True)
        self.setWindowTitle('Image Resaver')
        self.resize(400, 200)

        # Установка иконки приложения
        self.setWindowIcon(QIcon('app_icon.ico'))

        # Установка тёмного стиля
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(30, 30, 30))
        palette.setColor(QPalette.WindowText, Qt.white)
        self.setPalette(palette)

        # Проверка доступности шрифта Roboto
        available_fonts = QFontDatabase().families()
        if 'Roboto' in available_fonts:
            font = QFont('Roboto', 10)
        else:
            font = QFont('Arial', 10)  # Шрифт по умолчанию

        # Текстовое сообщение
        self.label = QLabel('Перетащите сюда изображения (поддерживаются JPG, PNG)', self)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)  # Разрешаем перенос строк для длинного текста

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
            self.label.setText('Отпустите для загрузки изображений')
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.label.setText('Перетащите сюда изображения (поддерживаются JPG, PNG)')

    def dropEvent(self, event):
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        self.processFiles(files)

    def processFiles(self, files):
        image_count = 0
        for file_path in files:
            if image_count >= 50:
                break  # Прерываем без предупреждения, если достигли 50 файлов
            if os.path.isfile(file_path):
                ext = os.path.splitext(file_path)[1].lower()
                if ext in ['.jpg', '.jpeg', '.png']:
                    try:
                        image = Image.open(file_path)
                        if ext in ['.jpg', '.jpeg']:
                            image.save(file_path, 'JPEG', quality=100)
                        elif ext == '.png':
                            image.save(file_path, 'PNG', optimize=True)
                        image_count += 1
                    except Exception:
                        pass  # Игнорируем ошибки без вывода предупреждений
                else:
                    pass  # Игнорируем неподдерживаемые файлы без предупреждений
        self.label.setText('Готово! Изображения пересохранены.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageResaver()
    ex.show()
    sys.exit(app.exec_())
