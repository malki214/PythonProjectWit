
import json
import os
import shutil
from Commit import Commit
import subprocess

# יצירת תקייה חדשה
def create_folder(path):
    if os.path.exists(path):
        return False
    os.mkdir(path)
    return True


# להפוך תקיה למוסתרת
def create_hidden_folder(path):
    subprocess.run(['attrib', '+h', path])


# יצירת קובץ חדש
def create_new_file(path):
    open(path, "w").close()


# העתקת קובץ או תקיה ממיקום מסוים למיקום אחר
def copy_file(src, dst):
    if os.path.isfile(src):
        shutil.copy(src, dst)
    else:
         shutil.copytree(src, dst)


# העתקת כל הקבצים והתקיות מהמקור ליעד
def copy_files(src, dst):
    files = os.listdir(src)
    for fname in files:
        # בשביל הפעולה . add שלא יעתיק את התקיה wit. שנמצאת גם היא בתקיה שלו
        if fname != ".wit":
            copy_file(os.path.join(src, fname), os.path.join(dst, fname))


# מחיקת כל הקבצים והתקיות מהניתוב שהתקבל
def delete_contents(path):
    files = os.listdir(path)
    for fname in files:
        new_path = os.path.join(path, fname)
        if os.path.isfile(new_path):
            os.remove(new_path)
        elif fname != ".wit":
            shutil.rmtree(new_path)


def list_files_in_folder(path):
    return os.listdir(path)


def get_user_name():
    return os.getlogin()


# כתיבת מילון קומיטים לתוך קובץ JSON
def write_to_json(path, dict):
    # העתקה למילון חדש שהערך יהיה מילון ולא אובייקט כדי שיהיה אפשר לכתוב ולקרוא מהקובץ
    dict2 = {}
    for k, v in dict.items():
        dict2[k] = v.convert_to_dict()
    with open(path, "w") as json_file:
        json.dump(dict2, json_file)
        json_file.close()


# קריאה מקובץ JSON והחזרת המילון
def read_from_json(path):
    with open(path, "r") as json_file:
        dict = json.load(json_file)
        json_file.close()
        # החזרת הערכים במילון שיהיו כאובייקט commit
        for k, v in dict.items():
            dict[k] = Commit(v["version_name"],v["creator_name"],v["date"])
        return dict

#שרשור ניתוב
def concat_path(path,name):
    return os.path.join(path, name)


#האם קיים הניתוב הזה
def path_exists(path):
    return os.path.exists(path)

