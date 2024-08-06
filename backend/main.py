from datetime import datetime
from contextlib import asynccontextmanager
import base64
from io import BytesIO

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from torchvision import transforms
from torch.utils.data import DataLoader

from schemas import ImageOut, Model, Score
from src.dataset import CifarDataset


def get_recent_scores(model_name):
    return [Score(**{"name": "accuracy", "score": 77.77})]

def tensor_to_base64(tensor):
    transform = transforms.ToPILImage()
    pil_image = transform(tensor)
    buffered = BytesIO()
    pil_image.save(buffered, format="PNG")
    base64_string = base64.b64encode(buffered.getvalue()).decode()
    return base64_string

models = {}
datasets = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    models["resnet18"] = "resnet18"
    models["resnet34"] = "resnet34"
    models["resnet50"] = "resnet50"
    models["resnet101"] = "resnet101"
    models["resnet152"] = "resnet152"
    datasets["cifar10_dataset"] = CifarDataset("./data/test", train=False)
    datasets["cifar10_dataloader"] = iter(DataLoader(datasets["cifar10_dataset"], batch_size=100, shuffle=True))
    yield
    models.clear()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health-check")
async def health_check():
    return {"status": "ok"}

@app.get("/models", response_model=list[Model])
async def get_models():
    model_keys = list(models.keys())
    models_ = [
        Model(model_name=model_key, 
              score=get_recent_scores(model_key), 
              last_updated=datetime.now()) 
              for model_key in model_keys
        ]
    return models_

@app.get("/images", response_model=list[ImageOut])
async def get_images():
    try:
        indexes, tensors, labels = next(datasets["cifar10_dataloader"])
        images = [ImageOut(file_name=f"test_{index}", base64=tensor_to_base64(tensor)) 
            for index, tensor in zip(indexes, tensors)]
        return images
    except StopIteration as e:
        datasets["cifar10_dataloader"] = iter(DataLoader(datasets["cifar10_dataset"], batch_size=100, shuffle=True))
        indexes, tensors, labels = next(datasets["cifar10_dataloader"])
        images = [ImageOut(file_name=f"test_{index}", base64=tensor_to_base64(tensor)) 
            for index, tensor in zip(indexes, tensors)]
        return images

@app.post("/images/{file_name}/guess")
async def guess_image():
    pass