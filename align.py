import cv2
import numpy as np
import sys

file_name = sys.argv[1]
file_path = sys.argv[2]

# Load images in color
img0 = cv2.imread(f"{file_path}/{file_name}_00.png")
img1 = cv2.imread(f"{file_path}/{file_name}_01.png")
img2 = cv2.imread(f"{file_path}/{file_name}_02.png")

# Use feature detection and matching (e.g., SIFT)
sift = cv2.SIFT_create()

kp0, des0 = sift.detectAndCompute(img0, None)
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)

# FLANN parameters
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)

flann = cv2.FlannBasedMatcher(index_params, search_params)

# Function to align images based on translation
def align_images(img_src, img_dst, kp_src, des_src, kp_dst, des_dst):
    matches = flann.knnMatch(des_src, des_dst, k=2)

    # Apply ratio test
    good_matches = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good_matches.append(m)

    # Calculate translation vector
    if len(good_matches) > 10:
        src_pts = np.float32([kp_src[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp_dst[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

        translation_matrix = cv2.estimateAffinePartial2D(src_pts, dst_pts)[0]

        # Apply translation to the source image
        aligned_img = cv2.warpAffine(img_src, translation_matrix, (img_dst.shape[1], img_dst.shape[0]))

        # Save or display the aligned image
        return aligned_img

# Align img0 to img1
aligned_img_0_to_1 = align_images(img0, img1, kp0, des0, kp1, des1)
cv2.imwrite(f"{file_path}/{file_name}_aligned_image_0_to_1.png", aligned_img_0_to_1)

# Align img2 to img1
aligned_img_2_to_1 = align_images(img2, img1, kp2, des2, kp1, des1)
cv2.imwrite(f"{file_path}/{file_name}_aligned_image_2_to_1.png", aligned_img_2_to_1)
