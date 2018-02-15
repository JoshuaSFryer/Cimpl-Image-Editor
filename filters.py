"""
Image manipulation library by Joshua Fryer, with help from material by
Prof. Donald L. Bailey, particularly the CIMPL library, which acts as an
interface with the PIL/Pillow image manipulation library.
"""
from Cimpl import *
import Cimpl
#from PIL import ImageTk
#import os
#import sys

# Filters
def red_channel(image):
	for pixel in image:
		x, y, (r, g, b) = pixel

		g = 0
		b = 0

		col = create_color(r, g, b)
		set_color(image, x, y, col)

def green_channel(image):
	for pixel in image:
		x, y, (r, g, b) = pixel

		r = 0
		b = 0

		col = create_color(r, g, b)
		set_color(image, x, y, col)

def blue_channel_(image):
	for pixel in image:
		x, y, (r, g, b) = pixel

		r = 0
		g = 0

		col = create_color(r, g, b)
		set_color(image, x, y, col)

def get_channel(image, chan):
	"""
	Strip away all but the specified colour channel of an image
	chan = r, g, or b, corresponding to the red/green/blue channel,
	respectively
	"""
	if chan == 'r':
		red_channel(image)

	elif chan == 'g':
		green_channel(image)

	elif chan == 'b':
		blue_channel(image)

def modify_brightness(image, scale):
	"""
	Adjust the brightness of an image by (scale)%
	"""
	scale = scale/100

	for pixel in image:
		x, y, (r, g, b) = pixel

		r = r * scale
		g = g * scale
		b = b * scale

		col = create_color(r, g, b)
		set_color(image, x, y, col)

	show(image)

def swap_red_blue(image):
	"""
	Swap the values of the red and blue channels of each pixel in an image
	"""
	for pixel in image:
		x, y, (r, g, b) = pixel
		oldr = r
		oldb = b
		r = oldb
		b = oldr

		col = create_color(r, g, b)
		set_color(image, x, y, col)

	show(image)

def encode_image(image):

	"""
	Encode the RGB values of each pixel in an image into arrays of ASCII
	characters and make the image black. 
	To restore the image, run the decode_image method.
	NOTE: Large images will result in long processing times and significant
	memory usage (>100-200 MB for a 1920*1080 image)
	"""
	image.encoded_channels = []
	for i in range(3):
		image.encoded_channels.append([])
	for pixel in image:
		x, y, (r, g, b) = pixel
		image.encoded_channels[0].append(chr(r))
		image.encoded_channels[1].append(chr(g))
		image.encoded_channels[2].append(chr(b))
		r = 0
		g = 0
		b = 0
		col = create_color(r, g, b)
		set_color(image, x, y, col)      

def decode_image(image):
	"""
	Converts the ASCII in the encoded arrays back to ints, and restores the
	original image using these ints as RGB channel data
	"""
	image.color_vals = []
	for i in range(3):
		image.color_vals.append([])
	index = 0
	for i in image.encoded_channels[0]:
		image.color_vals[0].append(ord(i))
	for i in image.encoded_channels[1]:
		image.color_vals[1].append(ord(i))
	for i in image.encoded_channels[2]:
		image.color_vals[2].append(ord(i))

	for pixel in image:
		x, y, (r, g, b) = pixel

		r = image.color_vals[0][index]
		g = image.color_vals[1][index]
		b = image.color_vals[2][index]

		col = create_color(r, g, b)
		set_color(image, x, y, col)
		index += 1
	# Clear the obscenely large arrays to free up memory once the GC
	# does its rounds
	# TODO: Find a better algorithm :P
	image.color_vals = None
	image.encoded_channels = None

def greyscale(image):
	"""
	Turns all colour in an image into shades of grey
	"""
	for pixel in image:
		x, y, (r, g, b) = pixel
		brightness = get_brightness(r, g, b)

		col = create_color(brightness, brightness, brightness)
		set_color(image, x, y, col)   

def negative(image):
	"""
	Converts an image to its negative
	"""
	for pixel in image:
		x, y, (r, g, b) = pixel

		r = abs(r - 255)
		g = abs(g - 255)
		b = abs(b - 255)

		col = create_color(r, g, b)
		set_color(image, x, y, col)

def extreme_contrast(image):
	"""
	Greatly increases the contrast of an image, increasing a channel's value
	where its value is >= 128, and decreasing it if it is lower
	"""
	for pixel in image:
		x, y, (r, g, b) = pixel
		channel = [r, g, b]

		for i in range (0, 2):
			if channel[i] >= 128:
				channel[i] = 200
			else:
				channel[i] = 55
		col = create_color(channel[0], channel[1], channel[2])
		set_color(image, x, y, col)

def sepia(image):

	"""
	Converts an image to grayscale and then yellows it by selectively muting
	its blue channel and boosting its red channel
	"""
	greyscale(image)

	for pixel in image:
		x, y, (r, g, b) = pixel

		if b < 63:
			b = b * 0.8
			r = r * 1.20
			# g = g * 1.07
		elif b >= 63 and b <= 191:
			b = b * 0.75
			r = r * 1.25
			# g = g * 1.1
		else:
			b = b * 0.83
			r = r * 1.18
			# g = g * 1.06

		col = create_color(r, g, b)
		set_color(image, x, y, col)

def blur(image):
	""" (Cimpl.Image) -> Cimpl.Image

	Return a new image that is a blurred copy of image.

	original = load_image(choose_file())
	blurred = blur(original)
	show(original)
	show(blurred)    
	"""

	# We modify a copy of the original image, because we don't want blurred
	# pixels to affect the blurring of subsequent pixels.

	target = copy(image)
	"""
	# Recall that the x coordinates of an image's pixels range from 0 to
	# get_width() - 1, inclusive, and the y coordinates range from 0 to
	# get_height() - 1.
	#
	# To blur the pixel at location (x, y), we use that pixel's RGB components,
	# as well as the components from the four neighbouring pixels located at
	# coordinates (x - 1, y), (x + 1, y), (x, y - 1) and (x, y + 1).
	#
	# As such, we can't use this loop to generate the x and y coordinates:
	#
	# for y in range(0, get_height(image)):
	#     for x in range(0, get_width(image)):
	#
	# With this loop, when x or y is 0, subtracting 1 from x or y yields -1, 
	# which is not a valid coordinate. Similarly, when x equals get_width() - 1 
	# or y equals get_height() - 1, adding 1 to x or y yields a coordinate that
	# is too large.
	#
	# We have to adjust the arguments passed to range to ensure that (x, y)
	# is never the location of pixel on the top, bottom, left or right edges
	# of the image, because those pixels don't have four neighbours.
	"""
	for y in range(1, get_height(image) - 1):
		for x in range(1, get_width(image) - 1):
			
			r = 0
			g = 0
			b = 0
			pixel_x = x

			for i in range (-1, 2):
				for j in range (-1, 2):
					col = get_color(image, x+i, y+j)
					r = r + col[0]
					g = g + col[1]
					b = b + col[2]

			new_color = create_color(r / 9, g / 9, b / 9)
			#new_color = create_color(new_red, new_green, new_blue)

			# Modify the pixel @ (x, y) in the copy of the image
			set_color(target, x, y, new_color)
	#global curr_image
	#currImage = target
	show(target)

def detect_edges(image, threshold):
	""" (Cimpl.Image, float) -> None
	 Modify image using edge detection.
	 An edge is detected when a pixel's brightness differs
	 from that of its neighbour by an amount that is greater
	 then the specified threshold.
	 >>> image = load_image(choose_file())
	 >>> detect_edges(image, 10.0)
	 >>> show(image)
	 """
	target = copy(image)
	black = create_color(0,0,0)
	white = create_color(255,255,255)

	for y in range(1, get_height(image) - 1):
		for x in range (1, get_width(image) - 1):
			center_red, center_green, center_blue = get_color(image, x, y)
			below_red, below_green, below_blue = get_color(image, x, y+1)
			right_red, right_green, right_blue = get_color(image, x+1, y)


			center_brightness = get_brightness(center_red, center_green,
			                                   center_blue)
			below_brightness = get_brightness(below_red, below_green,
			                                  below_blue)
			right_brightness = get_brightness(right_red, right_green,
			                                  right_blue)

			if abs(center_brightness-below_brightness) > threshold or abs(
			    center_brightness - right_brightness) > threshold:
				set_color(target, x, y, black)
			else:
				set_color(target, x, y, white)
	show(target)

def flip_vertical(image):
	"""
	Image --> None
	Inverts an image along the vertical/y-axis
	"""
	target = copy(image)
	for y in range(0, get_height(image)):
		for x in range(0, get_width(image)):
			col1 = get_color(image, x, y)
			col2 = get_color(image, (get_width(image) - x - 1), y)
			set_color(target, x, y, col2)
			set_color(target, (get_width(image) - x - 1), y, col1)
	show(target)
	
def flip_horizontal(image):
	"""
	Image --> None
	Inverts an image along the horizontal/x-axis
	"""
	target = copy(image)
	for y in range(0, get_height(image)):
		for x in range(0, get_width(image)):
			col1 = get_color(image, x, y)
			col2 = get_color(image, x, (get_height(image) - y - 1))
			set_color(target, x, y, col2)
			set_color(target, x, (get_height(image) - y - 1), col1)
	show(target)

def get_brightness(r, g, b):
	"""
	3-element tuple --> float
	Uses a weighting formula to get a value representing the brightness of
	a colour, defined by an RGB tuple
	"""
	# weighted formula to account for percieved brightness
	return abs(0.2126 * r + 0.7152 * g + 0.0722 *b)
