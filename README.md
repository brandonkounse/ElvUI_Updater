# ElvUI_Updater
---
### Purpose

This script will check the current version of ElvUI on the TukUI website. If the current version is newer than the version on the local PC, or if the addon is not present, this script will install it.

### How to Run

First, make sure both `Python3` and `pip` are installed on the machine. In the directory
where the script is located, execute this command in the terminal:

```bash
pip install -r requirements.txt
```

From there, simply execute the `python` command:

```bash
python3 main.py
```

If an update is required, you will see this executed when the script is ran:

![Update Required](./images/update%20required.png)

If an update is not required, you will see this instead:

![No Update Required](./images/no%20update%20required.png)