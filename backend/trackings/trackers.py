"""
Tracks posts and add displacements to database
"""

import concurrent.futures
import cv2
import pandas as pd
import numpy as np
from scipy.spatial import distance
from crud import crud_tissue_tracking, crud_video


class TissueTracker:
    """Tissue class for pointfinding"""

    def __init__(self, database, un_points, calib_factor, video_object):
        video_file_path = video_object.save_location
        tissue_object_list = video_object.tissues

        self.tissue_ids = [
            tissue_object.id for tissue_object in tissue_object_list]
        self.calib_factor = calib_factor
        self.database = database
        self.times = []

        videostream = cv2.VideoCapture(video_file_path)
        self.total_frames = int(videostream.get(cv2.CAP_PROP_FRAME_COUNT))
        first_image = videostream.read()[1]

        boxes = \
            [format_box(un_points[i-1], un_points[i])
             for i in range(len(un_points)) if i % 2 == 1]

        tracks = list(map(lambda box: trackers_init(
            box, video_file_path, first_image), boxes))
        lists = np.array(tracks).T.tolist()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            post_locs = list(executor.map(self.threaded_centroid, *lists))
            executor.shutdown(wait=True)

        for index, post_info in enumerate(post_locs):
            if index % 2 == 1:
                rel_index = int((index - 1) / 2)
                self.add_to_database(post_info, post_locs[index-1], rel_index)
        crud_video.update_tracked_status(database, video_object.id, True)

    def add_to_database(self, post_locs_one, post_locs_two, rel_tiss_id):
        """Adds information to database"""
        disps = list(map(distance.euclidean, post_locs_one, post_locs_two))

        transpose_one = np.array(post_locs_one).T.tolist()
        transpose_two = np.array(post_locs_two).T.tolist()

        odd_x = transpose_one[0]
        odd_y = transpose_one[1]
        even_x = transpose_two[0]
        even_y = transpose_two[1]

        id_repeated = [self.tissue_ids[rel_tiss_id]] * len(disps)

        zipped = zip(self.times[0], disps, id_repeated,
                     odd_x, odd_y, even_x, even_y)
        dataframe = pd.DataFrame(list(zipped),
                                 columns=["time", "displacement", "tissue_id", "odd_x", "odd_y", "even_x", "even_y"])

        crud_tissue_tracking.create_tissue_tracking(
            self.database, self.tissue_ids[rel_tiss_id], dataframe)

    def threaded_centroid(self, tracker, videostream):
        """Tracks a single post through all frames"""
        frame = 0
        centroid_list = []
        timer = []
        while True:
            successful, image = videostream.read()
            if not successful:
                break
            successful, post = tracker.update(image)
            frame += 1
            print(frame/self.total_frames)

            (x_dist, y_dist, width, height) = post
            centroid = (float(x_dist + width / 2), float(y_dist + height / 2))

            if (time := videostream.get(cv2.CAP_PROP_POS_MSEC)) != 0:
                centroid_list.append(self.calibrate(centroid))
                timer.append(time / 1000)

        self.times.append(timer)
        return centroid_list

    def calibrate(self, centroids):
        """Converts the locations from pixels to mms"""
        return (centroids[0] * self.calib_factor / 2, centroids[1] * self.calib_factor / 2)


def trackers_init(box, vid_path, image):
    """Initialize a single tracker"""
    tracker = cv2.TrackerCSRT_create()
    tracker.init(image, box)
    return tracker, cv2.VideoCapture(vid_path)


def format_box(first_point, second_point):
    """Format boxes for use with openCV"""
    x_dist = first_point[0] * 2
    y_dist = first_point[1] * 2
    width = second_point[0] * 2 - x_dist
    height = second_point[1] * 2 - y_dist
    return int(x_dist), int(y_dist), int(width), int(height)
