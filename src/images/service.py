import random
import logging
import mimetypes

import cv2
import numpy as np

logger = logging.getLogger(__name__)


def find_features(image):
    pass


def match_features(kp1, kp2, desc1, desc2, img1, img2):
    pass


def calculate_homography(correspondences):
    pass


def geometric_distance(correspondence, homography):
    pass


def ransac(corr, thresh):
    pass


def guess_extension(filename: str) -> str:
    mime_type, _ = mimetypes.guess_type(filename)
    extension = mimetypes.guess_extension(type=mime_type)
    return extension or ".jpg"


def cast_array_to_bytes(dst, extension: str) -> bytes:
    ret, buffer = cv2.imencode(ext=extension, img=dst)
    return buffer.tobytes()
