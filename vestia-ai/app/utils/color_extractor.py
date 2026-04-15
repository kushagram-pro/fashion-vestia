from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
from webcolors import rgb_to_hex

def extract_colors(image_path, k=3):
    """
    Extract dominant colors from an image using KMeans
    """
    try:
        image = Image.open(image_path)
        image = image.resize((150, 150))  # Resize for faster processing

        img_array = np.array(image)
        img_array = img_array.reshape(-1, 3)  # Reshape to (num_pixels, 3)

        kmeans = KMeans(n_clusters=k, n_init=10)
        kmeans.fit(img_array)

        colors = kmeans.cluster_centers_

        hex_colors = [rgb_to_hex(color) for color in colors]

        return hex_colors
    except Exception as e:
        return {"error": str(e)}
    
def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(
        int(rgb[0]), int(rgb[1]), int(rgb[2])
    )