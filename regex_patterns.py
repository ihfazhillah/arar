import re


meaning_results = re.compile(r"(?<=<ol class=\"meaning-results\">).+?(?=</ol>)", re.S)
near_results = re.compile(r"(?<=<ol id=\"near-results\" class=\"meaning-results\">).+?(?=</ol>)", re.S)
entity = re.compile(r"(?<=<label>)(?P<label>.+?)(?=</label>).+?(?<=<ul>.<li>)(?P<arti>.+?)(?=</li>.</ul>)", re.S)
