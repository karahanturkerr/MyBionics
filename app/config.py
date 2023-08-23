import os
from os import path, getenv
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    TARGET_FACE_ID_NAME: str = os.getenv("TARGET_FACE_ID_NAME", "Yusuf")

