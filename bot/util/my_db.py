import os 
import json
from typing import List, Optional
from collections import OrderedDict

from dotenv import dotenv_values
import asyncio


class JsonDB:
    FILE_NAME = '/' + dotenv_values(".env").get('FILE_NAME') + '.json'
    path = os.getcwd() + FILE_NAME
    

    @classmethod
    def get_dict_from_db(cls) -> Optional[dict]:
        file_content = None

        with open(cls.path, "r", encoding="utf-8") as file:
            file_content = OrderedDict(json.load(file))

        return file_content
    

    @classmethod
    def set_letter(cls, letter: str, answer: str) -> None:
        data = {}

        with open(cls.path, "r", encoding="utf-8") as file:
            data = OrderedDict(json.load(file))

        data.update({letter: answer})

        with open(cls.path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


    @classmethod
    def delete_letter(cls, id: int) -> None:
        data = None 

        with open(cls.path, "r", encoding="utf-8") as file:
            data = OrderedDict(json.load(file))
        
        for idx, key in enumerate(data.keys()):
            if idx == id:
                del data[key]

        with open(cls.path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        

    @staticmethod
    def dict_to_str(data: dict) -> List[str]:
        return [f'{key}: {value}' for key, value in data.items()]