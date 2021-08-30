# Project - EMD

- School project made by @Nulzn and @L00ting (FelixDev)

- This project is not open to the public, and only @Nulzn and @L00ting have authorization to download it.

- ^^ (Later on, the project can be made public for others to download. If it becomes public, we'll let you know!)
## Installation

```bash

pip install flask flask_sqlalchemy

pip install cryptography

```

## Usage

```python

# Imports the main libary of flask and needed functions.
from flask import Flask, render_template, redirect, url_for, request

# Imports the libary that handles the database
from flask_sqlalchemy import SQLAlchemy

# Imports the datetime which can be used as a timestamp for creating a user etc.
from datetime import datetime

# Imports the hasing algorithm that is used on passwords.
from cryptography.fernet import Fernet

```