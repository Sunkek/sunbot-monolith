import json
import re
from random import choice

MESSAGE_PLACEHOLDERS = (
    "`user.name` - replaced with the target user name, if applicable\n"
    "`user.id` - replaced with the target user ID, if applicable\n"
    "`user.mention` - replaced with the target user mention, if applicable"
    "`rnd{a~b~c}` - selects a, b or c randomly"
)

def int_convertable(string):
    """Return True if string is convertable into int"""
    try: 
        int(string)
        return True
    except (ValueError, TypeError):
        return False

def format_seconds(seconds):
    years = seconds // (60*60*24*365)
    seconds %= (60*60*24*365)
    days = seconds // (60*60*24)
    seconds %= (60*60*24)
    hours = seconds // (60*60)
    seconds %= (60*60)
    minutes = seconds // 60
    seconds %= 60
    ye = f"{int(years)}y " if years else ""
    da = f"{int(days)}d " if days else ""
    ho = f"{int(hours)}h " if hours else ""
    mi = f"{int(minutes)}m " if minutes else ""
    se = f"{int(seconds)}s"
    return f"{ye}{da}{ho}{mi}{se}"
    
def format_message(text, guild=None, user=None):
    print(text)
    print(type(text))
    note = []
    if not text:
        return None
    if type(text) in (dict, list):
        note.append("json")
        text = json.dumps(text)
    print(text)
    print(type(text))
    if user:
        text = text.replace("user.name", user.name)
        text = text.replace("user.id", str(user.id))
        text = text.replace("user.mention", user.mention)
    p = re.compile(r"(rnd\{[^{}]*\})")
    random_lists = p.findall(text)
    while random_lists:
        print(text)
        for random_list in random_lists:
            result = choice(random_list[4:-1].split("~"))
            text.replace(random_list, result)
        random_lists = p.findall(text)
    if "json" in note:
        text = json.loads(text)
    print(text)
    print(type(text))
    return text