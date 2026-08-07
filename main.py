import datetime
import colorama
import psutil
import sys
import time
import os

colorama.init(autoreset=True)

COLOR_VALUE = colorama.Fore.LIGHTCYAN_EX
COLOR_LABEL = colorama.Style.BRIGHT
COLOR_RESET = colorama.Style.RESET_ALL
COLOR_HELP = colorama.Fore.LIGHTGREEN_EX
CLEAR_LINE = "\033[K"

def get_disk_label():
    if sys.platform == 'win32':
        return os.path.splitdrive(os.getcwd())[0] or 'C:'
    try:
        for part in psutil.disk_partitions():
            if part.mountpoint == '/':
                return part.device.replace('/dev/', '')
    except:
        pass
    return 'root'

DISK_NAME = get_disk_label()

def get_progress_string(percent, length=30):
    filled_length = int(length * percent / 100)
    bar = (colorama.Fore.LIGHTGREEN_EX + "█" * filled_length + 
           colorama.Fore.WHITE + "-" * (length - filled_length))
    return f"|{bar}|"

def run(last_net_io, last_time):
    sys.stdout.write('\033[H\033[?25l')

    now = datetime.datetime.now()
    std_hour = now.hour % 12 or 12
    meridiem = 'PM' if now.hour >= 12 else 'AM'

    current_time = time.perf_counter()
    elapsed = max(current_time - last_time, 0.001)

    year_start = datetime.datetime(now.year, 1, 1)
    year_end = datetime.datetime(now.year + 1, 1, 1)
    total_year_seconds = (year_end - year_start).total_seconds()
    year_percent = ((now - year_start).total_seconds() / total_year_seconds) * 100
    day_percent = ((now.hour * 3600 + now.minute * 60 + now.second) / 86400) * 100

    print(f"{COLOR_LABEL}Year Progress: {COLOR_VALUE}{year_percent:.4f}%{COLOR_RESET}{CLEAR_LINE}")

    grid_size = 10
    filled_boxes = int((year_percent / 100) * (grid_size**2)) 
    for i in range(grid_size**2): 
        color = colorama.Fore.GREEN if i < filled_boxes else colorama.Fore.WHITE
        sys.stdout.write(f"{color} ■ {colorama.Style.RESET_ALL}")
        if (i + 1) % grid_size == 0:
            sys.stdout.write(f"{CLEAR_LINE}\n")

    print(f"{'=' * 30}{CLEAR_LINE}\n{CLEAR_LINE}")

    print(f"{COLOR_LABEL}Day Progress:  {COLOR_VALUE}{day_percent:.2f}%{COLOR_RESET}{CLEAR_LINE}")
    print(f"{get_progress_string(day_percent)}{CLEAR_LINE}\n{CLEAR_LINE}")

    print(f"{COLOR_LABEL}Time: {COLOR_VALUE}{std_hour:02d}:{now.minute:02d}:{now.second:02d} {meridiem}{COLOR_RESET}{CLEAR_LINE}")
    print(f"{COLOR_LABEL}Date: {COLOR_VALUE}{now.strftime('%d / %m (%B / %b) / %Y (%A)')}{COLOR_RESET}{CLEAR_LINE}")
    print(f"{'=' * 37}{CLEAR_LINE}\n{CLEAR_LINE}")

    cpu_percent = psutil.cpu_percent(interval=None)
    disk = psutil.disk_usage('/')
    net_io = psutil.net_io_counters()
    memory = psutil.virtual_memory()

    print(f"{COLOR_LABEL}CPU: {COLOR_VALUE}{cpu_percent:>5.1f}%{COLOR_RESET}{CLEAR_LINE}")
    print(f"{COLOR_LABEL}RAM: {COLOR_VALUE}{memory.percent:.1f}% ({memory.used/1024**3:.2f} / {memory.total/1024**3:.2f} GB){COLOR_RESET}{CLEAR_LINE}")
    print(f"{COLOR_LABEL}Disk ({DISK_NAME}): {COLOR_VALUE}{disk.percent:.1f}% ({disk.used/1024**3:.2f} / {disk.total/1024**3:.2f} GB){COLOR_RESET}{CLEAR_LINE}")
    print(f"{'-' * 37}{CLEAR_LINE}")

    up_speed = ((net_io.bytes_sent - last_net_io.bytes_sent) / (1024**2)) / elapsed
    down_speed = ((net_io.bytes_recv - last_net_io.bytes_recv) / (1024**2)) / elapsed

    print(f"{COLOR_LABEL}NET UP:   {COLOR_VALUE}{up_speed:6.2f} MB/s {COLOR_RESET}| {COLOR_LABEL}Errors Out: {COLOR_VALUE}{net_io.errout}{COLOR_RESET}{CLEAR_LINE}")
    print(f"{COLOR_LABEL}NET DOWN: {COLOR_VALUE}{down_speed:6.2f} MB/s {COLOR_RESET}| {COLOR_LABEL}Errors In:  {COLOR_VALUE}{net_io.errin}{COLOR_RESET}{CLEAR_LINE}")
    print(f"{COLOR_LABEL}Packets: {COLOR_HELP} Sent:{COLOR_VALUE} {net_io.packets_sent} {COLOR_HELP} Recv:{COLOR_VALUE}  {net_io.packets_recv}{COLOR_RESET}{CLEAR_LINE}")
    print(f"{COLOR_LABEL}Drops:    {colorama.Fore.LIGHTBLUE_EX}In:{COLOR_VALUE}  {net_io.dropin} | {colorama.Fore.LIGHTBLUE_EX}Out:{COLOR_VALUE} {net_io.dropout}{COLOR_RESET}{CLEAR_LINE}")

    sys.stdout.flush()
    return net_io, current_time

def main():
    sys.stdout.write('\033[2J\033[H') 
    psutil.cpu_percent(interval=None)
    last_net_io = psutil.net_io_counters()
    t = time.perf_counter()
    
    try:
        while True:
            last_net_io, t = run(last_net_io, t)
            time.sleep(0.2)
    except KeyboardInterrupt:
        sys.stdout.write('\033[?25h')
        print(f"\n{colorama.Fore.YELLOW}Exiting dashboard...")
    finally:
        colorama.deinit()

if __name__ == "__main__":
    main()
