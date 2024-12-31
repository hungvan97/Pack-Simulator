import helperfunction as hf
import asyncio
from os import listdir

async def get_image() -> None:
    for f in listdir(path='./asset/source_image'):
        if f.endswith('.json'):
            await hf.read_json_file(filename=f'./asset/source_image/{f}')

if __name__ == "__main__":
    asyncio.run(get_image())