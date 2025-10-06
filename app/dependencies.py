from fastapi import Header, HTTPException

def get_user_id(user_id: str = Header(...)) -> str:
    if not user_id:
        raise HTTPException(status_code=400, detail="Missing User-ID header")
    return user_id