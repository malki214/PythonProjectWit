class Commit:
    def __init__(self, version_name, creator_name, date):
        self.__version_name = version_name
        self.__creator_name = creator_name
        self.__date = date

    def get_name(self):
        return self.__version_name

    def convert_to_dict(self):
        return {
            "version_name": self.__version_name,
            "creator_name": self.__creator_name,
            "date": str(self.__date),
        }

    def __str__(self):
        return f"commit:\nname: {self.__version_name}\ncreator: {self.__creator_name}\ndate: {self.__date}"
