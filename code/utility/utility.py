from datetime import timedelta

def format_time(elapsed_time : timedelta):
    hours, remainder = divmod(elapsed_time.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours > 0:
        formatted_string = f"{hours} hours, {minutes} minutes, {seconds} seconds"
    else:
        formatted_string = f"{minutes} minutes, {seconds} seconds"
    return formatted_string