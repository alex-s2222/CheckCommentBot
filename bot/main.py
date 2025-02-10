
from app import run
from util.my_db import JsonDB

if __name__ == '__main__':
    JsonDB.check_or_create_file()
    run.run_bot()
