import datetime
import colorama
import psutil
import asyncio
import sys
import os

colorama.init(autoreset=True)

COLOR_VALUE = colorama.Fore.LIGHTCYAN_EX
COLOR_LABEL = colorama.Style.BRIGHT
COLOR_RESET = colorama.Style.RESET_ALL

def get_progress_string(percent, length=30):
    filled_length = int(length * percent / 100)
    bar = (colorama.Fore.LIGHTGREEN_EX + "█" * filled_length + 
           colorama.Fore.WHITE + "-" * (length - filled_length))
    return f"|{bar}|"

async def run():
    now = datetime.datetime.now()
    
    std_hour = now.hour % 12 or 12
    meridiem = 'PM' if now.hour >= 12 else 'AM'

    year_start = datetime.datetime(now.year, 1, 1)
    year_end = datetime.datetime(now.year + 1, 1, 1)
    total_year_seconds = (year_end - year_start).total_seconds()
    elapsed_year_seconds = (now - year_start).total_seconds()
    year_percent = (elapsed_year_seconds / total_year_seconds) * 100

    day_percent = ((now.hour * 3600 + now.minute * 60 + now.second) / 86400) * 100

    sys.stdout.write("\033[H") 

    grid_size = 10
    filled_boxes = int((year_percent / 100) * (grid_size**2))
    grid = ""
    for i in range(grid_size**2):
        grid += (colorama.Fore.GREEN if i < filled_boxes else colorama.Fore.WHITE) + " ■ "
        if (i + 1) % grid_size == 0:
            grid += "\n"

    print(f"Year Progress: {year_percent:.2f}%\n")
    print(grid)
    print("=" * 30 + "\n")

    print(f"Day Progress:  {day_percent:.2f}%\n")
    print(f"{get_progress_string(day_percent)}\n")

    print(f"Current Time: {std_hour:02d}:{now.minute:02d}:{now.second:02d} {meridiem}")
    print(f"Current Date: {now.strftime('%d / %m / %Y (%A)')}\n")
    print("=" * 37 + "\n")

    cpu_percent = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    current_disk = '/'
    if sys.platform == 'win32':
        current_disk = os.path.splitdrive(os.getcwd())[0] or 'C:'
    else:
        try:
            partitions = psutil.disk_partitions()
            for part in partitions:
                if part.mountpoint == '/':
                    device = part.device
                    if device.startswith('/dev/'):
                        current_disk = device[5:]
                    else:
                        current_disk = device
                    break
        except:
            current_disk = 'root'

    stats = (
        f"{COLOR_LABEL}CPU:{COLOR_RESET} {COLOR_VALUE}{cpu_percent:.2f}%{COLOR_RESET}, \n"
        f"{COLOR_LABEL}Memory:{COLOR_RESET} {COLOR_VALUE}{memory.percent:.2f}% ({memory.used / (1024**3):.2f}{COLOR_RESET} / {COLOR_VALUE}{memory.total / (1024**3):.2f}){COLOR_RESET} GB, \n"
        f"{COLOR_LABEL}Memory Free:{COLOR_RESET} {COLOR_VALUE}{memory.available / (1024**3):.2f}{COLOR_RESET} / {COLOR_VALUE}{memory.total / (1024**3):.2f}{COLOR_RESET}GB, \n"
        f"{COLOR_LABEL}Disk ({current_disk}):{COLOR_RESET}{COLOR_VALUE} {disk.percent:.2f}%{COLOR_RESET}, \n"
        f"{COLOR_LABEL}Disk Used ({current_disk}):{COLOR_RESET} {COLOR_VALUE}{disk.used / (1024**3):.2f}{COLOR_RESET} / {COLOR_VALUE}{disk.total / (1024**3):.2f}{COLOR_RESET} GB, \n"
        f"{COLOR_LABEL}Free Space ({current_disk}):{COLOR_RESET} {COLOR_VALUE}{disk.free / (1024**3):.2f}{COLOR_RESET} / {COLOR_VALUE}{disk.total / (1024**3):.2f}{COLOR_RESET} GB"
    )

    print(stats)
    
    sys.stdout.flush()

async def main():
    print("\033[2J")
    try:
        while True:
            await run()
            await asyncio.sleep(0.1)
    except KeyboardInterrupt:
        print(f"\n{colorama.Fore.YELLOW}Exiting dashboard...")
    finally:
        colorama.deinit()
        try:
            sys.exit(1)
        except SystemExit:
            os._exit(1)

if __name__ == "__main__":
    asyncio.run(main())
