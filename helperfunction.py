import json
import requests
from pathlib import Path
import aiohttp
import timingexecution as te

async def read_json_file(filename) -> None:
    try:
        with open(file=filename, mode='r') as file:
            data = json.load(file)  # Load the JSON data   
            print("Json data loaded successfully")
        
        # Create directory structure for saving images
        parse_set = filename.split('.')[2]
        save_dir = Path(f'./asset/card_image/Set {parse_set}')
        save_dir.mkdir(parents=True, exist_ok=True)
            
        cards_to_download_images = [card for card in data['cards'] if 'images' in card and 'full' in card['images']] 
        for card in te.progressbar(it=cards_to_download_images, prefix="Downloading"):
            full_image_url = card['images']['full']
            card_id = card['id']
            card_number = card['number']
            await download_image(url=full_image_url, dir=save_dir, number=card_number, id=card_id)
        print("All images downloaded successfully")
    except FileNotFoundError:   
        print(f"Error: File '{filename}' not found")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file '{filename}'")
        return None
    
async def download_image(url, dir, number, id) -> bool:
    """Download image from URL and save it to the specified directory

    Args:
        url (str): API URL Path to access the image
        dir (str): directory to save the image
        number (str): number of the card
        id (str): unique identifier of the card

    Returns:
        bool: True if image is downloaded successfully, False otherwise
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url) as response:
                response.raise_for_status() # Raise an exception for 4xx/5xx status codes
                image_content = await response.read()

    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")
        return False
    
    filename = f'{dir}/{number}_{id}.jpg'
    with open(file=filename, mode='wb') as file:
        file.write(image_content)
        return True
