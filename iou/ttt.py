import cv2

x1, y1 = 105,132
winW1 , winH1 = 250, 60

x2, y2 = 104,128
winW2 , winH2 = 250, 60

newx = x2 + winW2
newy = y2 + winH2

image_path = '/home/alpha/Pictures/iou/example_03.jpg'
image = cv2.imread(image_path) 
cv2.rectangle(image, (x1, y1), (x1+winW1, y1+winH1), (0, 255, 0), 2)
cv2.rectangle(image, (x2, y2), (x2+winW2, y2+winH2), (0, 0, 255), 2)

cv2.imshow('image', image)
cv2.waitKey(0)
# cv2.rectangle(clone, (x, y), (x+winW+20, y+winH+20), (0, 255, 0), 2)

boxA = [x1, y1, x1+winW1, y1+winH1]
boxB = [x2, y2, x2 + winW2, y2 + winH2]

print(boxA)
print(boxB)
print(newx, newy)
	
def bb_intersection_over_union(boxA, boxB):
	# determine the (x, y)-coordinates of the intersection rectangle
	xA = max(boxA[0], boxB[0])
	yA = max(boxA[1], boxB[1])
	xB = min(boxA[2], boxB[2])
	yB = min(boxA[3], boxB[3])
 
	# compute the area of intersection rectangle
	interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
 
	# compute the area of both the prediction and ground-truth
	# rectangles
	boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
	boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
 
	# compute the intersection over union by taking the intersection
	# area and dividing it by the sum of prediction + ground-truth
	# areas - the interesection area
	iou = interArea / float(boxAArea + boxBArea - interArea)
 
	# return the intersection over union value
	return iou

iou = bb_intersection_over_union(boxA, boxB)
print(iou)