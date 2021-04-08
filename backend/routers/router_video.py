from typing import List
from database import get_db
from crud import crud_video
from schemas import schema_video

from fastapi import APIRouter, Depends, HTTPException, Query

from sqlalchemy.orm import Session

router = APIRouter()


@router.get('/videos', response_model=List[schema_video.VideoInfo], tags=["Videos"])
async def get_videos(db: Session = Depends(get_db)):
    all_vids = crud_video.get_all_vids(db)
    return all_vids


@router.get('/selectedVideo/', tags=["Videos"])
async def selected_video(video_id: int = Query(...), db: Session = Depends(get_db)):
    tup_path_numTissues = get_video_info(db, video_id)

    res = jsonable_encoder({'image_path': tup_path_numTissues[0],
                            'number_tissues': tup_path_numTissues[1]})

    return JSONResponse(content=res)


@router.get("/videos_show", response_model=List[schema_video.VideoShow], tags=["Videos"])
def get_vids_reactors(db: Session = Depends(get_db)):
    videos = crud_video.get_videos(db)

    if not videos:
        raise HTTPException(status_code=404, detail="Videos not found")
    return videos


@router.delete("/video/{vid_id}", tags=["Videos"])
def delete_video(vid_id: int, db: Session = Depends(get_db)):
    return crud_video.delete_video(db, vid_id)
