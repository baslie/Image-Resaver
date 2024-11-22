import sys
import os
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QProgressBar
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon, QFontDatabase
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PIL import Image

class ImageProcessor(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)

    def __init__(self, files):
        super().__init__()
        self.files = files

    def run(self):
        image_count = 0
        total_images = min(len(self.files), 50)
        for index, file_path in enumerate(self.files):
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
            # Обновляем прогресс
            progress_value = int(((index + 1) / total_images) * 100)
            self.progress.emit(progress_value)
        self.finished.emit('Готово! Изображения пересохранены.')

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

        # Прогресс-бар
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #05B8CC;
                width: 20px;
            }
        """)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.progress_bar)
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
        self.label.setText('Обработка изображений...')
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)

        self.thread = ImageProcessor(files)
        self.thread.progress.connect(self.updateProgress)
        self.thread.finished.connect(self.processingFinished)
        self.thread.start()

    def updateProgress(self, value):
        self.progress_bar.setValue(value)

    def processingFinished(self, message):
        self.label.setText(message)
        self.progress_bar.setVisible(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageResaver()
    ex.show()
    sys.exit(app.exec_())
