import shutil

import uvicorn
from fastapi import UploadFile, File, FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST
import json

from utils.annealing import Annealing
from utils.wagon_utils import wagons

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/dataset")
async def upload_file(file: UploadFile = File(...)):
    if file.filename.split('.')[1] == 'json':
        with open(f"files/upload.json", "wb") as f:
            shutil.copyfileobj(file.file, f)
        try:
            with open("files/upload.json", 'r', encoding="utf-8") as f:
                datas = json.loads(f.read())
            if isinstance(datas, list):
                results = []
                for situation in datas:
                    annealing = Annealing(situation)
                    annealing.main_func()
                    results.append(wagons(annealing.full_map, annealing.current_ways, situation))
            else:
                annealing = Annealing(datas)
                annealing.main_func()
                results = wagons(annealing.full_map, annealing.current_ways, datas)

        except Exception as e:
            print(e)
            return JSONResponse({'status': 'error', "detail": "Something went wrong"}, status_code=HTTP_400_BAD_REQUEST)
        else:
            return JSONResponse(results)
    else:
        return JSONResponse({'status': 'error', "detail": "Bad file"}, status_code=HTTP_400_BAD_REQUEST)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0')
