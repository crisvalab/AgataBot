class Conversation():

    def __init__(self):
        self.base = "Hy!\nHey!\nWhat is your name?\nMy name is Agata. Can I help you?\nHello, who are you?\nI am an IA called Agata created by Cristian. How can I help you?\nWhat's your name?\nMy name is Agata\n"
        self.context = self.base

    def reset_context():
        latest = self.context.split("\n")[-5:]
        self.context = self.base
        for l in latest:
            self.append_context(l)

    def append_context(self, plus):
        self.context += f'{plus}\n'

    def __str__(self):
        return self.context