import datetime
import colorama
import psutil
import time

colorama.init()

now = datetime.datetime.now()
hour, minute, sec = now.hour, now.minute, now.second

stdhour = 12 if hour % 12 == 0 else hour % 12
M = 'PM' if hour >= 12 else 'AM'
week_day = now.strftime("%A")

year, month, day = now.year, now.month, now.day
days_in_year = (datetime.datetime(year + 1, 1, 1) - datetime.datetime(year, 1, 1)).days
year_percent = ((now.timetuple().tm_yday - 1) + hour / 24 + minute / 1440 + sec / 86400) / days_in_year * 100

total_day_secs = 86400
seconds_passed = hour * 3600 + minute * 60 + sec
day_percent = (seconds_passed / total_day_secs) * 100

box = " ■ "
grid_size = 10
filled_boxes = int((year_percent / 100) * grid_size**2)

def get_system_stats():
    time.sleep(0.1)
    disk_info = psutil.disk_usage('/')
    return (
        f"CPU: {psutil.cpu_percent()}%, \n"
        f"Memory: {psutil.virtual_memory().percent}%, \n"
        f"Disk: {disk_info.percent}% \n"
        f"Free Space: {disk_info.free / (1024**3):.2f} GB / {disk_info.total / (1024**3):.2f} GB"
    )


grid = ""
for i in range(grid_size**2):
    grid += (colorama.Fore.GREEN if i < filled_boxes else colorama.Fore.WHITE) + box
    if (i + 1) % grid_size == 0:
        grid += "\n"

print(f"Year Progress: {year_percent:.2f}%")
print(grid + colorama.Style.RESET_ALL)
print("==============================\n")

print(f"Day Progress: {day_percent:.2f}%")

filled_boxes = int((day_percent / 100) * grid_size**2)
length = 30
prog = "|" + colorama.Fore.LIGHTGREEN_EX + "█" * int(filled_boxes / 100 * length) + colorama.Fore.WHITE + "-" * (length - int(filled_boxes / 100 * length)) + "|"
print(prog + colorama.Style.RESET_ALL + "\n")

print(f"Current Time: {stdhour:02d}:{minute:02d}:{sec:02d} {M}")
print(f"Current Date: {day} / {month} / {year} ({week_day})")
print("=====================================\n")
print(get_system_stats(), "\n")
