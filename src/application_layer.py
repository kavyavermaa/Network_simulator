# src/application_layer.py

class ChatApp:
    def __init__(self, name):
        self.name = name

    def receive_segment(self, segment):
        print(f"[Application: {self.name}] Received Chat Message: {segment.data}")


class FTPMock:
    def __init__(self, name):
        self.name = name

    def receive_segment(self, segment):
        print(f"[Application: {self.name}] Received FTP Data Chunk: {segment.data}")
