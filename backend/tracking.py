"""
Tracks the vid to get the tissue stuff
"""
#import os

import cv2
import pandas as pd
from scipy.spatial import distance

from crud import crud_tissue_tracking

# This just formats the boxes toi be readable by opencv trackers


def format_points(old_points):
    result = []
    for i in range(0, len(old_points), 2):
        # Multiply by 2 because of scale factopr
        x = old_points[i][0] * 2
        y = old_points[i][1] * 2
        width = old_points[i + 1][0] * 2 - x
        height = old_points[i + 1][1] * 2 - y
        result.append((x, y, width, height))
    return result


def start_trackig(db, unformated_points, calib_factor, video_object, tissues):
    # getsvidio file path from vid object
    video_file_path = video_object.save_location
    tissue_object_list = video_object.tissues
    tissue_ids = [(tissue_object.id) for tissue_object in tissue_object_list]

    # Start a opencv videostream
    videostream = cv2.VideoCapture(video_file_path)
    total_frames = int(videostream.get(cv2.CAP_PROP_FRAME_COUNT))

    # Capture the first image
    # TODO: Fail gracefully
    images = videostream.read()[1]

    # Iniate all the available opencv trackers

    OPENCV_OBJECT_TRACKERS = {
        "csrt": cv2.TrackerCSRT_create,
        "kcf": cv2.TrackerKCF_create,
        "boosting": cv2.TrackerBoosting_create,
        "mil": cv2.TrackerMIL_create,
        "tld": cv2.TrackerTLD_create,
        "medianflow": cv2.TrackerMedianFlow_create,
        "mosse": cv2.TrackerMOSSE_create
    }

    # Create a multitracker object
    trackers = cv2.MultiTracker_create()

    # Format the points for opencv
    boxes = format_points(unformated_points)

    for box in boxes:
        # Create and add a tracker to the multitracker object for each box drawn
        # tracker = OPENCV_OBJECT_TRACKERS['csrt']()
        tracker = cv2.TrackerCSRT_create()
        trackers.add(tracker, images, box)

    frame = 1
    old_percentage = 0
    # Initiate what will be a list of dataframes.
    # Each dataframe will contain the diaplacements for 1 tissue
    displacement = []

    while True:
        if (percentage := int(100 * frame / total_frames)) is not old_percentage:
            print(percentage)
        old_percentage = percentage

        # read in the next frame
        successful, image = videostream.read()
        if not successful:
            # TODO: exception error
            break
        frame += 1

        successful, posts = trackers.update(image)
        if not successful:
            break

        # Get the positions of each post
        for objectID, post in enumerate(posts):
            (x, y, w, h) = [float(i) for i in post]
            centroid = (float(x + w / 2), float(y + h / 2))

            # Divide by two because of the scale factor of the video
            def calibrate(centroids): return (
                centroids[0] * calib_factor / 2, centroids[1] * calib_factor / 2)

            if (objectID % 2) == 0:
                # Save the x, y position of the even post
                centroid_even = calibrate(centroid)
                evenID = objectID
            # If objectID is odd it has a pair so do stuff
            elif (objectID - 1) == evenID:
                # Calculate tissue number based on object ID
                relative_post_location = int((objectID - 1) / 2)

                if len(displacement) < relative_post_location + 1:
                    displacement.append([])

                # Save the x, y position of the odd post
                centroid_odd = calibrate(centroid)
                time = videostream.get(cv2.CAP_PROP_POS_MSEC) / 1000

                disp = distance.euclidean(centroid_even, centroid_odd)
                displacement[relative_post_location].append(
                    (time, disp, tissue_ids[relative_post_location], centroid_odd[0], centroid_odd[1], centroid_even[0], centroid_even[1]))

    """
    tissue_tracking_cols = ["time", "displacment",
                            "tissue_id", "odd_x", "odd_y", "even_x", "even_y"]
    [crud_tissue_tracking.create_tissue_tracking(db, pd.DataFrame(
        an, columns=tissue_tracking_cols)) for an in displacement]

    the below could proablly be shorted with list comp or map 
    but it just makes it harder to read 
    leaving it here unless i want to review

    """

    for i, tissue_tracking_info in enumerate(displacement):
        dataframe = pd.DataFrame(tissue_tracking_info, columns=[
            "time", "displacement", "tissue_id", "odd_x", "odd_y", "even_x", "even_y"])
        crud_tissue_tracking.create_tissue_tracking(
            db, tissue_ids[i], dataframe)

    """
    # deletes files in img folder
    # REVIEW: this can probally be done better
    for file in os.listdir(os.getcwd() + '/static/uploads/img'):
        os.remove(os.getcwd() + '/static/uploads/img/' + file)

    """

    return boxes
