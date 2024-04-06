import logging

import cv2
import numpy as np

logger = logging.getLogger(__name__)


def find_features(image):
    sift = cv2.SIFT_create()
    keypoints, descriptors = sift.detectAndCompute(image, None)
    return keypoints, descriptors


def match_features(desc1, desc2):
    matcher = cv2.BFMatcher(cv2.NORM_L2, True)
    matches = matcher.match(desc1, desc2)
    return matches


def stitch_images(image1: bytes, image2: bytes):
    logger.info("Decoding images from bytes to numpy arrays")
    img1 = cv2.imdecode(np.frombuffer(image1, np.uint8), 0)
    img2 = cv2.imdecode(np.frombuffer(image2, np.uint8), 0)

    img1_color = cv2.imdecode(np.frombuffer(image1, np.uint8), 1)
    img2_color = cv2.imdecode(np.frombuffer(image2, np.uint8), 1)

    im1_h, im1_w = img1.shape[:2]
    im2_h, im2_w = img2.shape[:2]
    tgt_size = 400
    max_dim_val = max(im1_h, im1_w, im2_h, im2_w)
    rescale = tgt_size / max_dim_val

    logger.info("Resizing images")
    img1 = cv2.resize(img1, (int(im1_w * rescale), int(im1_h * rescale)))
    img1_color = cv2.resize(img1_color, (int(im1_w * rescale), int(im1_h * rescale)))
    img2 = cv2.resize(img2, (int(im2_w * rescale), int(im2_h * rescale)))
    img2_color = cv2.resize(img2_color, (int(im2_w * rescale), int(im2_h * rescale)))


    # find features and keypoints
    correspondenceList = []
    if img1 is not None and img2 is not None:
        logger.info("Finding features")
        kp1, desc1 = find_features(img1)
        kp2, desc2 = find_features(img2)
        keypoints = [kp1, kp2]
        logger.info("Matching features")
        matches = match_features(desc1, desc2)

        for match in matches:
            (x1, y1) = keypoints[0][match.queryIdx].pt
            (x2, y2) = keypoints[1][match.trainIdx].pt
            correspondenceList.append([x2, y2, x1, y1])

        corrs = np.matrix(correspondenceList)
        finalH, mask = cv2.findHomography(corrs[:, :2], corrs[:, 2:], cv2.RANSAC, 15.0)
        logger.debug(f"Homography matrix: {finalH}")

        offset = 0

        h1, w1 = img1.shape[:2]
        h2, w2 = img2.shape[:2]
        pts1 = np.array(([[0, 0], [0, h1], [w1, h1], [w1, 0]]), dtype=np.float32).reshape((-1, 1, 2))
        pts2 = np.array(([[0, 0], [0, h2], [w2, h2], [w2, 0]]), dtype=np.float32).reshape((-1, 1, 2))
        pts2_ = cv2.perspectiveTransform(pts2, finalH)
        pts = np.concatenate((pts1, pts2_), axis=0)
        [xmin, ymin] = np.int32(pts.min(axis=0).ravel() - 0.5)
        [xmax, ymax] = np.int32(pts.max(axis=0).ravel() + 0.5)
        t = [-xmin, -ymin]
        Ht = np.array([[1, 0, t[0]], [0, 1, t[1]], [0, 0, 1]])  # translate

        finalH[0, 2] += offset
        finalH[1, 2] += offset

        logger.info("Perspective warping")
        dst = cv2.warpPerspective(img2_color, Ht.dot(finalH), (xmax - xmin, ymax - ymin))
        dst[t[1]:h1 + t[1], t[0]:w1 + t[0]] = img1_color

        mask = dst.sum(axis=-1) > 0
        return dst[np.ix_(mask.any(1), mask.any(0))]


def cast_array_to_bytes(dst, extension: str) -> bytes:
    ret_val, buffer = cv2.imencode(ext=extension, img=np.array(dst, dtype=np.uint8))
    if not ret_val:
        raise ValueError("Could not encode dst to bytes")
    return buffer.tobytes()
