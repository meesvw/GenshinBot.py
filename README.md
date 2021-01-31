# GenshinBot.py
> GenshinBot.py is a Discord RPG Bot, inspired by Genshin Impact. GenshinBot.py is made using [discord.py](https://discordpy.readthedocs.io/en/latest/index.html).

## Documentation

### Important

- **Problems with installing**
  - I try to make the installation and maintenance as easy as possible. That said it will not always be perfect. If you experience any issues join the **[Discord Server](https://discord.gg/8GMKZTT22n)**.

- **Bugs**
  - If you find any bugs please make a ticket in the **[Discord Server](https://discord.gg/8GMKZTT22n)**.

### Installation

- Requirements
  - Discord Bot Token **[Guide](https://discordpy.readthedocs.io/en/latest/discord.html)**
  - Python 3.5.3 (or higher) **[Download](https://www.python.org/downloads/)**
  - Python modules
    - dblpy **[Docs](https://pypi.org/project/dblpy/)**
    - discord.py **[Docs](https://discordpy.readthedocs.io/en/latest/intro.html)**
    - python-dotenv **[Docs](https://pypi.org/project/python-dotenv/)**

#### Ubuntu install
First you need to make sure you have the required software to start the Bot:
```
sudo apt-get update -y
sudo apt-get install -y git python3 python3-pip
```

After you have installed the requirements you need to install the modules:
```
sudo pip3 install discord.py
sudo pip3 install python-dotenv
sudo pip3 install dblpy
```

Now you will need to get the files for the bot:
```
git clone https://github.com/meesvw/GenshinBot.py.git
```

After it's done installing you want to go into the folder and run the bot:
```
cd GenshinBot.py
python3 main.py
```

#### First startup
If you started the bot for the first time you will need to configure the `.env` file.
In this file you can add your Bot token and change the prefix.

Example:
```
BOT_TOKEN=YourBotToken
BOT_PREFIX=gi!
DBL_ENABLED=False
DBL_TOKEN=YourDBLToken
DEBUG_MODE=False
```

#### Running bot in the background
If you're running a CLI environment through SSH you will want to reconnect to your server without stopping the bot.
To do that you will need to start a `screen` session.

To make a screen session you will need to go into the `GenshinBot.py` folder and do the following:
```
sudo nano start.sh
```

Put this into the file:
```
#!/bin/bash
screen -S GenshinBot.py python3 main.py
```

After that save the file(`CTRL` + `X` then `Y` and `ENTER`).
All we have to do now is make the file executable by doing the following:
```
sudo chmod +x start.sh
```

Now if you type `./start.sh` it will open a new session with the bot in it.
If you want to disconnect you simply press: `CTRL` + `A` + `D`. To reconnect just type: `screen -r GenshinBot.py`

### Updating

Coming soon.

## Support me

Coming soon.
