from datetime import timedelta

def format_time(elapsed_time : timedelta):
    hours, remainder = divmod(elapsed_time.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours > 0:
        formatted_string = f"{hours} hours, {minutes} minutes, {seconds} seconds"
    elif minutes > 0:
        formatted_string = f"{minutes} minutes, {seconds} seconds"
    else:
        formatted_string = f"{seconds} seconds"
    return formatted_string

def format_time_float(elapsed_time : float):
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours > 0:
        formatted_string = f"{int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds"
    elif minutes > 0:
        formatted_string = f"{int(minutes)} minutes, {int(seconds)} seconds"
    else:
        formatted_string = f"{int(seconds)} seconds"
    return formatted_string