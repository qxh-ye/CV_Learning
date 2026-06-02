import time

warning_history = []

def add_warning(camera_name, warning):
    warning_history.append({
        "camera": camera_name,
        "warning": warning,
        "time": time.strftime(
            "%Y-%m-%d %H:%M:%S",
            time.localtime()
        )
    })

    if len(warning_history) > 100:
        warning_history.pop(0)

def get_warnings():
    return warning_history

