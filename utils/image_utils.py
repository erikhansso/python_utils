import os
import re
import uuid

from PIL import Image
import numpy as np
import cv2

# Crop region is a 4-tuple of left, top, right, bottom


def center_crop(img_filepath, new_width, new_height):

    im = Image.open(img_filepath)
    width, height = im.size

    if width <= new_width:
        left = 0
        right = width
    else:
        left = (width - new_width) / 2
        right = (width + new_width) / 2
    if height <= new_width:
        top = 0
        bottom = height
    else:
        top = (height - new_height) / 2
        bottom = (height + new_height) / 2

    crop_rectangle = (left, top, right, bottom)

    return im.crop(crop_rectangle)


def deans_center_crop(img, new_width=None, new_height=None):

    width = img.shape[1]
    height = img.shape[0]

    if new_width is None:
        new_width = min(width, height)

    if new_height is None:
        new_height = min(width, height)

    left = int(np.ceil((width - new_width) / 2))
    right = width - int(np.floor((width - new_width) / 2))

    top = int(np.ceil((height - new_height) / 2))
    bottom = height - int(np.floor((height - new_height) / 2))

    if len(img.shape) == 2:
        center_cropped_img = img[top:bottom, left:right]
    else:
        center_cropped_img = img[top:bottom, left:right, ...]

    return center_cropped_img


def current_img_dimension(img_filepath):
    img = Image.open(img_filepath)
    width, height = img.size
    return width, height


def resize_image(image_fp, width, height):
    image = Image.open(image_fp)
    return image.resize((width, height), Image.ANTIALIAS)


def process_images_in_dir(dir_path, save_dirpath, output_width, output_height, rescaling_threshold):

    for root, dirnames, filenames in os.walk(dir_path):
        for filename in filenames:
            if re.search("\.(jpg|jpeg|png|bmp)$", filename):
                input_img_filepath = os.path.join(root, filename)
                save_filepath = save_dirpath
                save_filepath += str(uuid.uuid4()) + ".png"
                width, height = current_img_dimension(input_img_filepath)

                if width <= output_width or height <= output_height:
                    print("Image too small to be cropped, upsizing it proportionally first")
                    img_resized = scale_img_up_proportionally(input_img_filepath, output_height, output_width)
                    img_resized.save(save_filepath)
                    input_img_filepath = save_filepath
                    width, height = current_img_dimension(input_img_filepath)

                if width > (output_width * rescaling_threshold) or height > (output_height * rescaling_threshold):
                    img_resized = scale_img_down_proportionally(input_img_filepath, output_height, output_width)
                    if img_resized is not None:
                        img_resized.save(save_filepath)
                        input_img_filepath = save_filepath
                result = center_crop(input_img_filepath, output_width, output_height)
                # If there is more than 3 channels, force rgb
                if img_is_rgba(result):
                    result = wipe_rgba(result)
                width, height = result.size
                if width != output_width or height != output_height:
                    print("Skipping file that had incorrect width or height, filename: ", filename)
                    continue
                result.save(save_filepath)


def scale_img_up_proportionally(img_filepath, output_height, output_width):

    width, height = current_img_dimension(img_filepath)
    original_ratio = height / width
    width_diff = output_width - width
    height_diff = output_height - height
    if height_diff > 0:
        new_height = int(height + height_diff)
        new_width = int((original_ratio / new_height) ** (-1))
    elif width_diff > 0:
        new_width = int(width + width_diff)
        new_height = int(new_width * original_ratio)
    return resize_image(img_filepath, new_width, new_height)


def scale_img_down_proportionally(img_filepath, output_height, output_width):

    width, height = current_img_dimension(img_filepath)
    original_ratio = height / width
    width_diff = output_width - width
    height_diff = output_height - height
    if height < width:
        new_height = int(height + height_diff)
        new_width = int((original_ratio / new_height) ** (-1))
    else:
        new_width = int(width + width_diff)
        new_height = int(new_width * original_ratio)
    return resize_image(img_filepath, new_width, new_height)


def img_is_rgba(img):
    return len(img.split()) > 3


def wipe_rgba(img):
    wiped_img = Image.new("RGB", img.size, (255, 255, 255))
    wiped_img.paste(img, mask=img.split()[3])
    return wiped_img


save_filepath = "D:\\PyProjects18\\image_generation\\datasets\\out\\"
input_dir_filepath = "D:\\PyProjects18\\image_generation\\datasets\\in\\"
new_output_width = 512
new_output_height = 512
rescaling_threshold = 1.1

process_images_in_dir(input_dir_filepath, save_filepath, new_output_width, new_output_height, rescaling_threshold)

print("Done.")
