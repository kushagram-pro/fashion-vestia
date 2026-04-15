from fastapi import APIRouter, UploadFile, File, Form

from app.services.wardrobe_service import add_item, get_user_items, delete_item

router = APIRouter()


@router.post("/upload")
def upload_clothing(
    user_id: str = Form(...),
    file: UploadFile = File(...)
):
    return add_item(user_id, file)


@router.get("/{user_id}")
def get_wardrobe(user_id: str):
    return get_user_items(user_id)


@router.delete("/{item_id}")
def remove_item(item_id: str):
    return delete_item(item_id)