class PetitionMeta:

    def __init__(self, no, category, n_participants, date_expired, date_start, detail_url, title):
        self.__no = no
        self.__category = category
        self.__n_participants = n_participants
        self.__date_expired = date_expired
        self.__date_start = date_start
        self.__detail_url = detail_url
        self.__title = title

    def __del__(self):
        pass

    @property
    def no(self):
        return self.__no

    @property
    def category(self):
        return self.__category

    @property
    def n_participants(self):
        return self.__n_participants

    @property
    def date_expired(self):
        return self.__date_expired

    @property
    def date_start(self):
        return self.__date_start

    @property
    def detail_url(self):
        return self.__detail_url

    @property
    def title(self):
        return self.__title


class PetitionBody:

    def __init__(self, petition_meta_id, body):
        self.__petition_meta_id = petition_meta_id
        self.__body = body

    def __del__(self):
        pass

    @property
    def petition_meta_id(self):
        return self.__petition_meta_id

    @property
    def body(self):
        return self.__body


class Word:

    def __init__(self, text, morpheme, petition_meta_id, position):
        self.__text = text
        self.__morpheme = morpheme
        self.__petition_meta_id = petition_meta_id
        self.__position = position

    def __del__(self):
        pass

    def __str__(self):
        return self.__text, self.__morpheme, self.__petition_meta_id, self.__position

    @property
    def text(self):
        return self.__text

    @property
    def morpheme(self):
        return self.__morpheme

    @property
    def petition_meta_id(self):
        return self.__petition_meta_id

    @property
    def position(self):
        return self.__position
