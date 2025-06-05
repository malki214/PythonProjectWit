
from file_handeling import *
import datetime
import uuid
import requests
import json

class Repository:
    def __init__(self, path):
        # שמירת הניתובים השימושיים
        self.path = path
        self.path_wit = concat_path(self.path,".wit")
        self.path_commits = concat_path(self.path_wit ,"commits")
        self.path_commitJson = concat_path(self.path_wit , "commitsDict.json")
        self.path_staging = concat_path(self.path_wit, "staging")

        # קריאה מהקובץ את רשימת הגרסאות אם כבר עשו init
        if path_exists(self.path_wit):
            self.__commits = read_from_json(self.path_commitJson)
        # self.__commits = מילון הקומיטים שבו המפתח הוא המזהה והערך הוא אוביקט מסוג קומיט


    def init(self):
        if create_folder(self.path_wit):
            create_hidden_folder(self.path_wit)
            create_folder(self.path_commits)
            create_new_file(self.path_commitJson)
            create_folder(self.path_staging)
            self.__commits = {}
            write_to_json(self.path_commitJson, {})
            return "inited wit"
        return "wit already inited"


    def add(self, name):
        if not path_exists(self.path_wit):
            return "wit not inited, do wit init"

        if name == ".":
            copy_files(self.path,self.path_staging)
            return "add all files and folders in project to staging"

        if not path_exists(concat_path(self.path,name)):
            return "file or folder not found, please try again"

        copy_file(concat_path(self.path,name), concat_path(self.path_staging ,name))
        return "add " + name + " to staging"


    def commit(self, name):
        if not path_exists(self.path_wit):
            return "wit not inited, do wit init"
        # אם הstaging ריק אין שינוי מהגרסה הקודם
        if not bool(list_files_in_folder(self.path_staging)):
            return "no have changes that did add"

        commit_path = concat_path(self.path_commits, name)
        # יצירת תקיה לקומיט הזה ובדיקה אם קימת כבר גרסה בשם זה
        if not create_folder(commit_path):
            return f"name version {name} already exists, please try again"

        # העתקה לתקיה את הגרסה הקודמת(אם קיימת) ואת מה שנמצא בstaging וריקונו
        if bool(self.__commits):
            last_version_path = concat_path(self.path_commits,list(self.__commits.values())[-1].get_name())
            copy_files(last_version_path,commit_path)
        copy_files(self.path_staging, commit_path)
        delete_contents(self.path_staging)
        # הוספת הcommit הנוכחי למילון הקומיטים וכתיבה לקובץ
        self.__commits[str(uuid.uuid4())] = Commit(name, get_user_name(), datetime.datetime.now())
        write_to_json(self.path_commitJson, self.__commits)
        return f"created new version name {name}"


    def log(self):
        if not path_exists(self.path_wit):
            return "wit not inited, do wit init"

        if not bool(self.__commits):
            return "Not have any commits yet"
        #מעבר על המילון והוספת שורה לכל קומיט
        str_log = ""
        for key, val in self.__commits.items():
            str_log += f"{str(val)}\nid: {key}\n\n"
        return str_log


    def status(self):
        if not path_exists(self.path_wit):
            return "wit not inited, do wit init"

        str_return = ""

        # קבצים שנמצאים בstaging ועדיין לא עשו commit
        files_in_staging = list_files_in_folder(self.path_staging)
        if bool(files_in_staging):
            str_return += f"Changes to be committed:\n{str(files_in_staging)}\n"
        else:
            str_return += "nothing to commit from staging\n"

        #קבצים שנמצאים ב working ולא עשו עליהם add (לא נמצאים בגרסה האחרונה ולא בstaging)
        files_in_working = list_files_in_folder(self.path)
        dif = set(files_in_working) - {".wit"} - set(files_in_staging)
        if bool(self.__commits):
            last_version_path = concat_path(self.path_commits,list(self.__commits.values())[-1].get_name())
            dif = dif - set(list_files_in_folder(last_version_path))
        if bool(dif):
             str_return += f"Changes not staged for commit:\n{str(list(dif))}\n"
        else:
            str_return += "nothing to add to staging"

        return str_return


    def checkout(self, id, file_name = None):
        if not path_exists(self.path_wit):
            return "wit not inited, do wit init"

        if id not in self.__commits.keys():
            return f"{id} version not exists, please try again"

        version_name = self.__commits[id].get_name()
        path_version = concat_path(self.path_commits,version_name)
        # החזרה של קובץ מסוים מתוך גרסה
        if bool(file_name):
            copy_file(concat_path(path_version,file_name),self.path)
            return f"checked-out from version {version_name} file {file_name}"
        #מחיקת התכולה מהworking והעתקה לשם את הגרסה המבוקשת
        delete_contents(self.path)
        copy_files(path_version, self.path)
        return f"checked-out to version {version_name}"

    def push(self):
        """
        שולחת את הקומיט האחרון בקריאת שרת לפרויקט צד שרת של פייתון
        שמזהה בעיות נפוצות באיכות הקוד ומחזירה גרפים חזותיים ותובנות
        :return: מה שחוזר מקריאת השרת במקרה שהצליחה
        """
        if not path_exists(self.path_wit):
            return "wit not inited, do wit init"

        if not bool(self.__commits):
            return "Not have any commits yet"

        last_version_path = concat_path(self.path_commits, list(self.__commits.values())[-1].get_name())

        baseurl = "http://localhost:8000"
        data = {"path": last_version_path}
        headers = {'Content-Type': 'application/json'}
        str_return = "success push!\n"

        response = requests.post(fr"{baseurl}/analyze", data=json.dumps(data), headers=headers)
        if response.status_code != 200:
            return f"failed with status {response.status_code}"
        str_return += f"link to graphs: {response.text}\n"

        response = requests.post(fr"{baseurl}/alerts", data=json.dumps(data), headers=headers)
        if response.status_code != 200:
            return f"failed with status {response.status_code}"
        str_return += response.text.replace('\\n','\n').split("\"")[1]
        return str_return
