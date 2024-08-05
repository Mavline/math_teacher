import aiofiles
from fastapi import UploadFile


class FileService:
    @staticmethod
    async def save_file(file: UploadFile):
        async with aiofiles.open(f"uploads/{file.filename}", "wb") as out_file:
            content = await file.read()
            await out_file.write(content)
        return f"uploads/{file.filename}"

    @staticmethod
    async def process_file(file_path: str):
        async with aiofiles.open(file_path, "r") as file:
            content = await file.read()
        # Здесь можно добавить дополнительную обработку файла
        return content.upper()
