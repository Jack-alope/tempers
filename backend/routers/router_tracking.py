"""
Router assisted with tissue tracking
"""

from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from scipy.spatial import distance

from database import get_db
from crud import crud_video, crud_calibration_set
from schemas import schema_video

from trackings.trackers import TissueTracker
router = APIRouter()


def _coord_distance(coords_list):
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
    cal_factor = 0
    cal_identifier = post_info.calibration_set_identifier

    if post_info.calibration_factor:
        print("has ident")
        cal_factor = post_info.calibration_factor
    elif post_info.calibration_distance and post_info.cal_points:
        print("has points")
        # Get the distance in pix of the calibration line uses [0] b
        # since there are four points to the box passed but we only care
        # care ablout the length of the diagnal line
        cal_dist_pix = _coord_distance(post_info.cal_points)[0]
        # Calib factor multiplied by 2 because video is scaled down orignally
        cal_factor = 2 * cal_dist_pix / post_info.calibration_distance

    cross_dist_pix = _coord_distance(post_info.cross_points)
    cross_dist_mm = list(map(lambda x: x * cal_factor, cross_dist_pix))
    crud_calibration_set.update_calibration_set(
        database, cal_identifier, cal_factor)
    crud_video.update_cal_cross(
        database, post_info.video_id,
        cal_identifier,
        cross_dist_mm)

    video_object = crud_video.get_vid_by_id(database, post_info.video_id)

    background_tasks.add_task(TissueTracker, database,
                              post_info.boxes, cal_factor, video_object)

    return {"ok": 200}
