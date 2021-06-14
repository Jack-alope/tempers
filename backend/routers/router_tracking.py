"""
Router assisted with tissue tracking
"""

from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from scipy.spatial import distance

from database import get_db
from crud import crud_video
from schemas import schema_video

from trackings.trackers import TissueTracker
router = APIRouter()


def coord_distance(coords_list):
    '''
    Accepts a list of coords
    Returns a list of those coords coverted to distance in pixel
    '''
    dist_list = []
    for i in range(1, len(coords_list), 2):
        point_one = coords_list[i - 1]
        point_two = coords_list[i]

        distance_value = float(distance.euclidean(point_one, point_two))

        dist_list.append(distance_value)

    return dist_list


@router.post('/boxCoordinates', tags=["tracking"])
async def box_coordinates(background_tasks: BackgroundTasks, post_info: schema_video.PostSelection,
                          database: Session = Depends(get_db)):
    """
    accepts the box coords and starts tracking

    """

    # Get the distance in pix of the calibration line uses [0] b
    # since there are four points to the box passed but we only care
    # care ablout the length of the diagnal line
    cal_dist_pix = coord_distance(post_info.cal_points)[0]

    cross_dist_pix = coord_distance(post_info.cross_points)

    cal_factor = post_info.calibration_distance / cal_dist_pix

    cross_dist_mm = list(map(lambda x: x * cal_factor, cross_dist_pix))

    crud_video.update_cal_cross(
        database, post_info.video_id,
        post_info.calibration_distance,
        cal_factor, cross_dist_mm)

    video_object = crud_video.get_vid_by_id(database, post_info.video_id)

    # TissueTracker(database, post_info.boxes, cal_factor, video_object)

    background_tasks.add_task(TissueTracker, database,
                              post_info.boxes, cal_factor, video_object)

    return {"ok": 200}
