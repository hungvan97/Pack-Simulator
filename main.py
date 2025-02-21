from re import S
from threading import Timer
from cv2 import accumulate
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
from regex import E
from starlette.templating import _TemplateResponse
import random

from helperfunction import select_random_card

app = FastAPI()     # Create a FastAPI instance (main entry point for web app)
app.mount(path="/asset", app=StaticFiles(directory="asset"), name="asset")
templates = Jinja2Templates(directory="templates")  # Create a Jinja2 template instance

# Add global storage for list of accumulated cards, which has been opened
list_opened_cards = []
# List all JSON files
SOURCE_DIR = "./asset/card_image"

SET_FOLDER = [f for f in os.listdir(path=SOURCE_DIR) if os.path.isdir(os.path.join(SOURCE_DIR, f))]
@app.get(path="/")
async def home(request: Request) -> _TemplateResponse:
    del list_opened_cards[:]        # Clear the list of opened cards
    return templates.TemplateResponse(
        name="index.html", 
        context={"request": request, "set_folder": SET_FOLDER, "set_directory": SOURCE_DIR}
        )

@app.post(path="/process")
async def pick_set(set_selected: str = Form(...)):# -> dict[str, Any]:
    """ Pick 12 random cards from selected set
    
    Probabilty distribution of card rarity in a pack:
    In theory, each pack contains 12 cards based on following rule:
    - 6 common cards with probability of 100%
    - 3 uncommon cards with probability of 100%
    - 2 rare or super rare or legendary cards. Each of 2 has the following probability to be appeared:
        . 67,510% for Rare
        . 24,355% for Super Rare
        . 8,1350% for Legendary
    ** Note: The probability is calculated and normalised based on the following reddit's sub: 
        https://www.reddit.com/r/Lorcana/comments/1gra94r/azurite_sea/
    - 1 foil card with following probability:
        . 38,75% for Common
        . 38,75% for Uncommon
        . 14,50% for Rare
        . 5,000% for Super Rare
        . 2,000% for Legendary
        . 1,000% for Enchanted
    ** Note: The probability can be found in the following article:
        https://lorcanaplayer.com/lorcana-card-rarities-pull-rates-holo-foils/

    Args:
        set_selected (str, optional): _description_. Defaults to Form(...).
    Returns:
        Dictionary contain list of card and status of POST response
    """
    opened_card = []
    # Select 6 common
    opened_card.extend(await select_random_card(set_selected=set_selected, rarity="Common", number=6))
    # Select 3 uncommon
    opened_card.extend(await select_random_card(set_selected=set_selected, rarity="Uncommon", number=3))
    # Select 2 with each be either rare, super rare, or legendary
    for _ in range(2):
        RARE_PROB = 67.510
        SUPER_RARE_PROB = 24.355
        LEGENDARY_PROB = 8.135

        random_prob = random.uniform(0, 100)
        if random_prob <= RARE_PROB:
            opened_card.extend(await select_random_card(set_selected=set_selected, rarity="Rare", number=1))
        elif random_prob <= RARE_PROB + SUPER_RARE_PROB:
            opened_card.extend(await select_random_card(set_selected=set_selected, rarity="Super Rare", number=1))
        else:
            opened_card.extend(await select_random_card(set_selected=set_selected, rarity="Legendary", number=1))
    # Select 1 foil card
    COMMON_FOIL_PROB = 38.75
    UNCOMMON_FOIL_PROB = 38.75
    RARE_FOIL_PROB = 14.50
    SUPER_RARE_FOIL_PROB = 5.00
    LEGENDARY_FOIL_PROB = 2.00
    ENCHANTED_FOIL_PROB = 1.00
    random_foil_prob = random.uniform(0, 100)
    if random_foil_prob <= COMMON_FOIL_PROB:
        opened_card.extend(await select_random_card(set_selected=set_selected, rarity="Common", number=1))
    elif random_foil_prob <= COMMON_FOIL_PROB + UNCOMMON_FOIL_PROB:
        opened_card.extend(await select_random_card(set_selected=set_selected, rarity="Uncommon", number=1))
    elif random_foil_prob <= COMMON_FOIL_PROB + UNCOMMON_FOIL_PROB + RARE_FOIL_PROB:
        opened_card.extend(await select_random_card(set_selected=set_selected, rarity="Rare", number=1))
    elif random_foil_prob <= COMMON_FOIL_PROB + UNCOMMON_FOIL_PROB + RARE_FOIL_PROB + SUPER_RARE_FOIL_PROB:
        opened_card.extend(await select_random_card(set_selected=set_selected, rarity="Super Rare", number=1))
    elif random_foil_prob <= COMMON_FOIL_PROB + UNCOMMON_FOIL_PROB + RARE_FOIL_PROB + SUPER_RARE_FOIL_PROB + LEGENDARY_FOIL_PROB:
        opened_card.extend(await select_random_card(set_selected=set_selected, rarity="Legendary", number=1))
    else:
        opened_card.extend(await select_random_card(set_selected=set_selected, rarity="Enchanted", number=1))

    # Add opened cards to accumulated list
    global list_opened_cards
    list_opened_cards.extend([(set_selected, _card) for _card in opened_card])
    return {"status": "success", "set": set_selected, "images": opened_card}

## API endpoint for data fetching
@app.get(path="/api/accumulate")
def accumulate_card() -> dict[str, list]:
    return {"opened_card_images": list_opened_cards}
@app.get(path="/list")
async def show_opened_cards(request: Request) -> _TemplateResponse:
    return templates.TemplateResponse(
        name="list.html",
        context={
            "request": request,
            "set_directory": SOURCE_DIR
        }
    )
if __name__ == "__main__":
    import uvicorn
    import webbrowser
    
    # Open the browser
    def open_browser() -> None:
        webbrowser.open(url="http://127.0.0.1:8000", new=1)
    Timer(2, open_browser).start()

    # Run the server
    uvicorn.run(app=app, host="127.0.0.1", port=8000)
