# import cv2
# import numpy as np
# #from  matplotlib import pyplot as plt
# #img = cv2.imread(r'C:\Users\MrSmile\Desktop\New folder\priroda.jpg',flags = cv2.IMREAD_COLOR)
# #cv2.namedWindow('priroda',cv2.WINDOW_AUTOSIZE)
# #cv2.imshow('priroda',img)
# #cv2.imwrite('priroda2.jpg',img)
# #k = cv2.waitKey(0)
# #plt.imshow(img, cmap ='hot', interpolation = 'bicubic')
# #plt.imshow(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
# #plt.xticks([]), plt.yticks([])
# #plt.axis('off')
# #plt.show()
#
#
# cap = cv2.VideoCapture ('trace-traffic.avi')
#
# while(cap.isOpened()):
#     ret, frame = cap.read()
#
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#
#     cv2.imshow('frame',gray)
#     cv2.waitKey(50)
#     if cv2.waitKey(1) & 0xFF == ord('p'):
#         #break
#       	input()
#
# cap.release()
# cv2.destroyAllWindows()
import numpy as np
import cv2

cap = cv2.VideoCapture ('trace-traffic3.mp4')

# params for ShiTomasi corner detection
feature_params = dict( maxCorners = 100,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )

# Parameters for lucas kanade optical flow
lk_params = dict( winSize  = (15,15),
                    maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Create some random colors
color = np.random.randint(0,255,(1000,3))

# Take first frame and find corners in it
ret, old_frame = cap.read()
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)

# Create a mask image for drawing purposes
mask = np.zeros_like(old_frame)

while(cap.isOpened()):
    ret,frame = cap.read()
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # calculate optical flow
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

    # Select good points
    good_new = p1[st==1]
    good_old = p0[st==1]

    # draw the tracks
    for i,(new,old) in enumerate(zip(good_new,good_old)):
        a,b = new.ravel()
        c,d = old.ravel()
        # mask = cv2.line(mask, (a,b),(c,d), color[i].tolist(), 2)
        frame = cv2.circle(frame,(a,b),5,color[i].tolist(),-1)
    img = cv2.add(frame,mask)

    cv2.imshow('frame',img)
    k = cv2.waitKey(25) & 0xff
    if k == 27:
        break


    # Now update the previous frame and previous points
    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1,1,2)

cv2.destroyAllWindows()
cap.release()
