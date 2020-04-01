from konlpy.tag import Kkma


class Tagger:
    def __init__(self, path=None):
        self.kkma = Kkma(jvmpath=path)
        print('kkma init')

    def nouns(self, text):
        return self.kkma.nouns(text)

    def pos(self, text):
        return self.kkma.pos(text)
