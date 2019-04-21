import cv2


class ClickAndDrop:
frame_size = (1280, 720)
window_name = "Crop the recording (top-left click -> bottom-right drop) - 'C' to crop - 'R' to restart"

def __init__(self, thumbnail):
    """
    Loads the image to crop and controls the callback loop. Calculates the reference points once a valid cropped area has been chosen and the user has clicked "c".
    """
    self.thumbnail = thumbnail
    self.reference_points = list()
    self.cropping = False
    
    # load the image, clone it, and setup the mouse callback function
    self.image = cv2.resize(self.thumbnail, self.frame_size, interpolation=cv2.INTER_AREA)
    clone = self.image.copy()
    cv2.namedWindow(self.window_name)
    cv2.setMouseCallback(self.window_name, self.click_and_crop)

    # keep looping until the 'q' key is pressed
    while True:
        # display the image and wait for a keypress
        cv2.imshow(self.window_name, self.image)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("r"):  # reset the cropping region
            self.image = clone.copy()
        elif key == ord("c"):  # break from the loop
            break

    # if there are 2 reference points, then crop the region of interest from the image
    if len(self.reference_points) == 2:
        self.roi = clone[self.reference_points[0][1]:self.reference_points[1][1],
                         self.reference_points[0][0]:self.reference_points[1][0]]

    # close all open windows
    cv2.destroyAllWindows()

def click_and_crop(self, event, x, y, flags, param):
    """
    Callback function allowing a user to manually crop an image.
    NOTE: must crop from top-left corner to bottom-right corner
    """
    # if the left mouse button was clicked, record the starting (x, y) coordinates and indicate that cropping is being performed
    if event == cv2.EVENT_LBUTTONDOWN:
        self.reference_points = [(x, y)]
        self.cropping = True

    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that the cropping operation is finished
        self.reference_points.append((x, y))
        self.cropping = False

        # draw a rectangle around the region of interest
        cv2.rectangle(self.image, self.reference_points[0], self.reference_points[1], (0, 255, 0), 2)
        cv2.imshow(self.window_name, self.image)

def get_roi(self):
    return self.roi

def get_reference_points(self):
    return self.reference_points