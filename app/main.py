from fastapi import FastAPI
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from .bookreviewsystem import views
