import subprocess

try:
    subprocess.run("python3 bot.py & python3 greet.py & python3 fav_coin.py", shell=True)
except:
    pass
