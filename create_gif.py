'''
VRPTW cs633 project
author: Bhavdeep Khileri(bk2281), Jay Nair(an1147), Sanish Suwal (ss4657)
'''
import os
import re
import imageio

def natural_sort_key(s):
    """
    Key function for natural sorting.
    """
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]


def create_gif(directory_name, gif_filename):
    # Get all PNG files in the directory
    png_files = [f for f in os.listdir(directory_name) if f.endswith('.png')]
    
    # Sort the PNG files by name
    png_files.sort(key=natural_sort_key)

    images = []
    for png_file in png_files:
        # print(png_file)
        file_path = os.path.join(directory_name, png_file)
        print(file_path)
        images.append(imageio.imread(file_path))
    # Save the GIF
    imageio.mimsave(gif_filename, images, fps=10)  # Duration is in seconds, here set to 1 second per frame

# Example usage
if __name__ == "__main__":
    directory_name = "assets/c201"  # Change to the directory containing your PNG images
    gif_filename = "output.gif"
    
    create_gif(directory_name, gif_filename)
