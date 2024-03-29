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
    note = []
    if not text:
        return None
    if type(text) in (dict, list):
        note.append("json")
        text = json.dumps(text)
    if user:
        text = text.replace("user.name", user.name)
        text = text.replace("user.id", str(user.id))
        text = text.replace("user.mention", user.mention)
    p = re.compile(r"(rnd\{[^{}]*\})")
    random_lists = p.findall(text)
    while random_lists:
        for random_list in random_lists:
            result = choice(random_list[4:-1].split("~"))
            text = text.replace(random_list, result)
        random_lists = p.findall(text)
    if "json" in note:
        text = json.loads(text)
    return text

def format_columns(columns, headers=None, footers=None):
    """Tabulate columns (lists) into a neatly aligned table"""
    for i in range(len(columns)):
        if type(columns[i]) != list: columns[i] = list(columns[i])
        if headers: columns[i] = [headers[i]] + columns[i]
        if footers: columns[i] += [footers[i]]
    maxlens = [max(len(str(line)) for line in column) for column in columns]
    if headers:
        for i in range(len(headers)):
            if headers[i] == "EMOTE":
                maxlens[i] = 5
                break
    table = []
    for row in zip(*columns):
        line = f'{row[0]:.<{maxlens[0]}}'
        for num, value in enumerate(row[1:-1], 1):
            line += f'..{value:.^{maxlens[num]}}'
        line += f'..{row[-1]:.>{maxlens[-1]}}'
        table.append(line)
    return '\n'.join(table)
    
async def send_welcome_or_leave(channel, text, embed, member):
    text = format_message(text, guild=member.guild, user=member)
    if embed:
        embed = json.loads(embed)
        embed = discord.Embed.from_dict(
            format_message(embed, guild=member.guild, user=member)
        )
    if embed or text:
        await channel.send(content=text, embed=embed)