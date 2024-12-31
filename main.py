from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
from starlette.templating import _TemplateResponse

from random import sample

app = FastAPI()     # Create a FastAPI instance (main entry point for web app)
app.mount(path="/asset", app=StaticFiles(directory="asset"), name="asset")
templates = Jinja2Templates(directory="templates")  # Create a Jinja2 template instance

# List all JSON files
SOURCE_DIR = "./asset/card_image"

SET_FOLDER = [f for f in os.listdir(path=SOURCE_DIR) if os.path.isdir(os.path.join(SOURCE_DIR, f))]
@app.get(path="/")
async def home(request: Request) -> _TemplateResponse:
    return templates.TemplateResponse(
        name="index.html", 
        context={"request": request, "set_folder": SET_FOLDER, "set_directory": SOURCE_DIR}
        )

@app.post(path="/process")
def pick_set(set_selected: str = Form(...)):# -> dict[str, Any]:
    # Get list of downloaded images
    image_dir = f"asset/card_image/{set_selected}"
    all_card = [f for f in os.listdir(path=image_dir) if f.endswith('.jpg')]
    # Select 12 random card images as if they are opened
    opened_card = sample(population=all_card, k=min(12, len(all_card)))
    
    return {"status": "success", "set": set_selected, "images": opened_card}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, host="127.0.0.1", port=8000)
