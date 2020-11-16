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