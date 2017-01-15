import os
import re

"""definisikan, kapan akan dilakukan live scrape lagi, 
dalam hari"""
EXPIRED_AFTER = 10 # in days

"""pengaturan untuk database, menentukan base path, database name
dan db_abs_path"""
BASE_PATH = os.path.dirname(__file__)
DB_NAME = "almaany.sqlite"
DB_ABS_PATH = os.path.join(BASE_PATH, DB_NAME)


"""definisi pattern untuk parsing di konfigurasi disini"""
MEANING_RESULT = re.compile(r"(?<=<ol class=\"meaning-results\">).+?(?=</ol>)", re.S)
NEAR_RESULT = re.compile(r"(?<=<ol id=\"near-results\" class=\"meaning-results\">).+?(?=</ol>)", re.S)
ENTITY = re.compile(r"(?<=<label>)(?P<label>.+?)(?=</label>).+?(?<=<ul>.<li>)(?P<arti>.+?)(?=</li>.</ul>)", re.S)
TAGS = re.compile(r"</?.+?/?>")
