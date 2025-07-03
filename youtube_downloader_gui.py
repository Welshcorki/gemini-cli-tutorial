import sys
import yt_dlp
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QFileDialog

class YouTubeDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('YouTube Downloader')
        self.setGeometry(100, 100, 400, 150)

        main_layout = QVBoxLayout()

        # URL Input
        url_layout = QHBoxLayout()
        self.url_label = QLabel('YouTube URL:')
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText('여기에 YouTube 동영상 URL을 입력하세요')
        url_layout.addWidget(self.url_label)
        url_layout.addWidget(self.url_input)
        main_layout.addLayout(url_layout)

        # Path Input
        path_layout = QHBoxLayout()
        self.path_label = QLabel('다운로드 경로:')
        self.path_input = QLineEdit(self)
        self.path_input.setPlaceholderText('다운로드할 폴더를 선택하세요')
        self.path_button = QPushButton('경로 선택', self)
        self.path_button.clicked.connect(self.select_download_path)
        path_layout.addWidget(self.path_label)
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(self.path_button)
        main_layout.addLayout(path_layout)

        # Download Button
        self.download_button = QPushButton('다운로드', self)
        self.download_button.clicked.connect(self.start_download)
        main_layout.addWidget(self.download_button)

        # Status Label
        self.status_label = QLabel('준비됨', self)
        main_layout.addWidget(self.status_label)

        self.setLayout(main_layout)

    def start_download(self):
        url = self.url_input.text()
        if not url:
            QMessageBox.warning(self, '경고', 'URL을 입력해주세요.')
            return

        self.status_label.setText('다운로드 중...')
        self.download_button.setEnabled(False) # Disable button during download

        try:
            download_path = self.path_input.text()
            if download_path:
                outtmpl = os.path.join(download_path, '%(title)s.%(ext)s')
            else:
                outtmpl = '%(title)s.%(ext)s'

            ydl_opts = {
                'format': 'best',
                'outtmpl': outtmpl,
                'noplaylist': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.status_label.setText(f'성공적으로 다운로드했습니다: {url}')
            QMessageBox.information(self, '완료', '동영상 다운로드가 완료되었습니다!')
        except Exception as e:
            self.status_label.setText(f'다운로드 중 오류가 발생했습니다: {e}')
            QMessageBox.critical(self, '오류', f'다운로드 중 오류가 발생했습니다:\n{e}')
        finally:
            self.download_button.setEnabled(True) # Re-enable button

    def select_download_path(self):
        folder_path = QFileDialog.getExistingDirectory(self, "다운로드 폴더 선택")
        if folder_path:
            self.path_input.setText(folder_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = YouTubeDownloader()
    ex.show()
    sys.exit(app.exec_())