import os
import cv2
import numpy as np
import glob

def run():
    # Step 1: Capture Images
    # Load images
    path = os.path.dirname(os.path.realpath(__file__))
    path += "/images/"
    image_names = [os.path.basename(f) for f in glob.glob(f"{path}*.jpg")]
    images = []

    for image_name in image_names:
        img = cv2.imread(f'{path}{image_name}')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        images.append((image_name, img))

    for i in range(len(images) - 1):
        img1 = images[i][1]
        img2 = images[i+1][1]

        # Step 2: Extract SIFT Features
        # Convert to grayscale
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        # Initialize SIFT detector
        sift = cv2.SIFT_create()

        # Find the keypoints and descriptors with SIFT
        kp1, des1 = sift.detectAndCompute(gray1, None)
        kp2, des2 = sift.detectAndCompute(gray2, None)

        # Step 3: Match Features
        # FLANN parameters
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)

        # Use FLANN to find best matches
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(des1, des2, k=2)

        # Step 4: Filter Good Matches
        good_matches = []
        for m, n in matches:
            if m.distance < 0.5 * n.distance:
                good_matches.append(m)

        # Draw matches
        img_matches = cv2.drawMatches(img1, kp1, img2, kp2, good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        cv2.imshow(f'Matches {i}', img_matches)

        # Step 5: Find Fundamental Matrix
        # Extract corresponding points
        pts1 = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        pts2 = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

        # Find fundamental matrix
        F, mask = cv2.findFundamentalMat(pts1, pts2, cv2.FM_RANSAC)

        # Step 6: Compute Essential Matrix
        # Camera matrices (assuming no lens distortion)
        K = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

        # # Essential matrix
        # E = K.T @ F @ K

        # # Step 7: Decompose Essential Matrix
        # # Decompose essential matrix to get relative rotation and translation
        # retval, R, t, mask = cv2.recoverPose(E, pts1, pts2, K)

        # # Now, R is the relative rotation matrix, and t is the relative translation vector. 
        # # The camera matrices for the two cameras can be constructed as follows:
        # P1 = np.hstack((np.eye(3), np.zeros((3, 1))))
        # P2 = np.hstack((R, t))

        # # Step 8: Triangulate 3D Points
        # # Triangulate points
        # points_4d = cv2.triangulatePoints(P1, P2, pts1.T, pts2.T)

        # # Convert to homogeneous coordinates
        # points_3d = cv2.convertPointsFromHomogeneous(points_4d.T)

        print(f"Fundamental Matrix {i}:\n{F}")
        # print(f"Essential Matrix:\n{E}")
        # print(f"Relative Translation:\n{t}")
        # Query detected keypoints with match indicies
        # print(f"Good Match Points {i}:\n{[(kp1[match.queryIdx].pt, kp2[match.trainIdx].pt) for match in good_matches]}")
        print(f"Good Match Points {i}: {len(good_matches)}")
        # print(f"Triangulated points:\n{points_4d}")
        # print(f"Homogeneous coordinates:\n{points_3d}")

    cv2.waitKey(0)
    cv2.destroyAllWindows()