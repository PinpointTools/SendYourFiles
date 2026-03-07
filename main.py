from src.front.web import startWeb
from src.back.system.history import History
from src.back.system.settings import Settings

History().checkHistory()
Settings().checkFile()

if __name__ == "__main__":
    startWeb()