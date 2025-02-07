import os 
from typing import List, Optional

from dotenv import dotenv_values
import aiofiles
import asyncio

class DB:
    FILE_NAME = '/' + dotenv_values(".env").get('FILE_NAME') + '.txt'
    path = os.getcwd() + FILE_NAME


    @classmethod
    async def get_letters(cls) -> Optional[List[str]]:
        """Получение предложенний из файла"""
        file_content = None

        async with aiofiles.open(cls.path, "r", encoding="utf-8") as file:
            file_content = await file.read()

        return file_content.split(';')[:-1]
        

    @classmethod
    async def write_letter(cls, letter: str) -> None:
        """Запись предложения в файл"""

        async with aiofiles.open(cls.path, "a", encoding="utf-8") as file:
            await file.write(letter + ';')