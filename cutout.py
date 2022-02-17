import cv2
import numpy as np
from color_detector import getColorName

def find_largest_contour(image):
    """
    This function finds all the contours in an image and return the largest
    contour area.
    :param image: a binary image
    """
    image = image.astype(np.uint8)
    contours, hierarchy = cv2.findContours(
        image,
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_SIMPLE
    )
    if len(contours) == 0:
        return 0
    largest_contour = max(contours, key=cv2.contourArea)
    return largest_contour

def show(name, image):
    cv2.imshow(name, image)

def apply_new_background(mask3d, foreground, save_name):
    """
    This function applies a new background to the extracted foreground image
    if `--new-background` flag is `True` while executing the file.
    :param mask3d: mask3d mask containing the foreground binary pixels
    :param foreground: mask containg the extracted foreground image
    :param save_name: name of the input image file
    """
    # normalization of mask3d mask, keeping values between 0 and 1
    mask3d = mask3d / 255.0
    # get the scaled product by multiplying
    foreground = cv2.multiply(mask3d, foreground)
    # read the new background image
    background = cv2.imread('input/background.jpg')
    # resize it according to the foreground image
    background = cv2.resize(background, (foreground.shape[1], foreground.shape[0]))
    background = background.astype(np.float)
    # get the scaled product by multiplying
    background = cv2.multiply(1.0 - mask3d, background)
    # add the foreground and new background image
    new_image = cv2.add(foreground, background)
    show('New image', new_image.astype(np.uint8))
    cv2.imwrite(f"outputs/{save_name}_new_background.jpg", new_image)


cap = cv2.VideoCapture(0)

while True:
    success,image = cap.read()
    show('Input image', image)
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    ret, gray = cv2.threshold(gray, 200 , 255, cv2.CHAIN_APPROX_NONE)
    contour = find_largest_contour(gray)
    image_contour = np.copy(image)
    cv2.drawContours(image_contour, [contour], 0, (0, 255, 0), 2, cv2.LINE_AA, maxLevel=1)
    # show('Contour', image_contour)
    # create a black `mask` the same size as the original grayscale image 
    mask = np.zeros_like(gray)
    # fill the new mask with the shape of the largest contour
    # all the pixels inside that area will be white 
    cv2.fillPoly(mask, [contour], 255)
    # create a copy of the current mask
    res_mask = np.copy(mask)
    res_mask[mask == 0] = cv2.GC_BGD # obvious background pixels
    res_mask[mask == 255] = cv2.GC_PR_BGD # probable background pixels
    res_mask[mask == 255] = cv2.GC_FGD # obvious foreground pixels
    mask2 = np.where((res_mask == cv2.GC_FGD) | (res_mask == cv2.GC_PR_FGD),255, 0).astype('uint8')
    new_mask3d = np.repeat(mask2[:, :, np.newaxis], 3, axis=2)
    mask3d = new_mask3d
    mask3d[new_mask3d > 0] = 255.0
    mask3d[mask3d > 255] = 255.0
    # apply Gaussian blurring to smoothen out the edges a bit
    # `mask3d` is the final foreground mask (not extracted foreground image)
    mask3d = cv2.GaussianBlur(mask3d, (5, 5), 0)
    # show('Foreground mask', mask3d)
    foreground = np.copy(image).astype(float)
    foreground[mask2 == 0] = 200
    show('Foreground', foreground.astype(np.uint8))
    mean_red = np.mean(foreground[:,:,2])
    mean_green = np.mean(foreground[:,:,1])
    mean_blue = np.mean(foreground[:,:,0])
    color = getColorName(mean_red,mean_green,mean_blue)
    print(color)
    if cv2.waitKey(1) == ord('q'):
        break   