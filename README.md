## Linux Kernel Tracker

A linux kernel version tracker written in python without any external dependencies.

There isn't really much to it since I wrote this as my introductory python project. So putting it out here if anyone finds it useful. And of course, PRs are welcome.

> Want to see this in action? Checkout Telegram channel [[@KernelTracker](https://t.me/kerneltracker)]. You might as well want to join the channel for ... you know ... automatic notifications (.❛ ᴗ ❛.)

### Usage
```
>>> python -m tracker -h

usage: kernel_tracker [-h] [-j [N]] [-g] [-n] [-w]

Utility to track kernel releases

optional arguments:
  -h, --help          show this help message and exit
  -j [N], --json [N]  prints kernel version release table as json (optionally
                      provide indent length N)
  -g, --get-updated   prints updated kernel versions
  -n, --notify        send notification to Telegram chat for updated kernels
  -w, --write-json    write latest releases to json file
```

### Setup
If you want to setup your own bot, you can either export `CHAT_ID` and `BOT_API` to your environment or just edit `config.py` in place:
```python
BOT_API = "abcdefg12345678990"
CHAT_ID = "123456789"
```
