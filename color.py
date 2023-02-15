from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

# Load the image
image = Image.open('img3.jpg')

# Get the image size
width, height = image.size

# Get a pixel map of the image
pixel_map = image.load()

# Define a function to get the color of a pixel
def get_pixel_color(x, y):
    # Check if the pixel is within the image bounds
    if x < 0 or x >= width or y < 0 or y >= height:
        return None
    # Get the RGB color of the pixel
    color = pixel_map[x, y]
    return color

# Define a function to get the average color of the pixels surrounding a point
def get_text_color(x, y, radius):
    # Get the color of each pixel within the given radius of the point
    colors = []
    for i in range(x-radius, x+radius+1):
        for j in range(y-radius, y+radius+1):
            color = get_pixel_color(i, j)
            if color is not None:
                colors.append(color)
    # Calculate the average color of the surrounding pixels
    if colors:
        avg_color = tuple(int(sum(color[channel] for color in colors) / len(colors)) for channel in range(3))
        return avg_color
    else:
        return None


def display_color(r, g, b):
    # Create a 1x1 figure
    fig, ax = plt.subplots(1, 1, figsize=(1, 1))

    # Create a 1x1 grid of pixels with the given color
    pixels = [[[r/255, g/255, b/255]]]
    ax.imshow(pixels)

    # Turn off the axis ticks and labels
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('off')

    # Display the color
    plt.show()

print("get colors")
# Example usage: Get the color of the pixel at (100, 100) and the average color of the pixels within a radius of 5 pixels
pixel_color = get_pixel_color(100, 100)
colors = np.array(pixel_color)
print("colors: ", colors)
display_color(colors[0], colors[1], colors[2])


# print("# Example usage")
# text_color = get_text_color(100, 100, 5)
# print(text_color)
# display_color(255, 0, 0)  # Red
# display_color(0, 255, 0)  # Green
# display_color(0, 0, 255)  # Blue