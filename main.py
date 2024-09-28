import webview
import os

if __name__ == '__main__':
    os.system('python app.py &')
    webview.create_window('Hello world', 'http://0.0.0.0:5000/')
    webview.start()