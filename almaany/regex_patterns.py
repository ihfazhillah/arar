import re


MEANING_RESULT = re.compile(r"(?<=<ol class=\"meaning-results\">).+?(?=</ol>)", re.S)
NEAR_RESULT = re.compile(r"(?<=<ol id=\"near-results\" class=\"meaning-results\">).+?(?=</ol>)", re.S)
ENTITY = re.compile(r"(?<=<label>)(?P<label>.+?)(?=</label>).+?(?<=<ul>.<li>)(?P<arti>.+?)(?=</li>.</ul>)", re.S)
TAGS = re.compile(r"</?.+?/?>")
