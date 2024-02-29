## Setup
# Modules
from fastapi import FastAPI

import mariadb
import sys

# Connect to Database
try:
    conn = mariadb.connect(
        user="username",
        password="******",
        host="192.000.0.1",
        port=3306,
        database="db_name"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

cur = conn.cursor()

# Constantes
app = FastAPI()

## Request
from room import *

from play import *