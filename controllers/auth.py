from typing import List

from fastapi import APIRouter, status

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)