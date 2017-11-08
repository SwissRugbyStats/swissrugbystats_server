class Notification:
    """

    """

    def __init__(self, type, sender, receiver, message):
        self.type = type
        self.sender = sender
        self.receiver = receiver
        self.message = message
        self.timestamp = ''

    def send(self):
        pass