from PIL import Image, ImageEnhance
import numpy as np
from sklearn.cluster import KMeans

# Caractères ASCII du plus foncé au plus clair
ASCII_CHARS = "@%#*+=-."

def resize_image(image, new_width=100):
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)  # Ajustement vertical
    return image.resize((new_width, new_height))

def grayify(image):
    return image.convert("L")

def colorify(image):
    return image.convert("RGB")

def enhance_saturation(image, factor=1.8):
    enhancer = ImageEnhance.Color(image)
    return enhancer.enhance(factor)

def adjust_brightness(image, factor=0.8):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

def enhance_sharpness(image, factor=2.0):
    enhancer = ImageEnhance.Sharpness(image)
    return enhancer.enhance(factor)

def pixels_to_ascii(gray_image):
    pixels = gray_image.getdata()
    scale = 256 // len(ASCII_CHARS)
    ascii_str = "".join(ASCII_CHARS[min(pixel // scale, len(ASCII_CHARS) - 1)] for pixel in pixels)
    return ascii_str

def dominant_colors(image, n_colors=4):
    img = np.array(image)
    img = img.reshape((-1, 3))
    kmeans = KMeans(n_clusters=n_colors)
    kmeans.fit(img)
    return [tuple(map(int, c)) for c in kmeans.cluster_centers_]

def assign_color_labels(image, color_list):
    img = np.array(image)
    h, w, _ = img.shape
    flat_img = img.reshape((-1, 3))
    labels = []
    for pixel in flat_img:
        distances = [np.linalg.norm(np.array(pixel) - np.array(c)) for c in color_list]
        labels.append(np.argmin(distances))
    return np.array(labels).reshape((h, w))

def build_color_ascii_layers(ascii_str, color_labels, ascii_width, ascii_height, n_colors):
    layers = []
    ascii_matrix = np.array(list(ascii_str)).reshape((ascii_height, ascii_width))
    colors_comparison = {}
    for color_idx in range(n_colors):
        layer = []
        acc_dominant = 0
        for y in range(ascii_height):
            linestr = ""
            for x in range(ascii_width):
                if color_labels[y, x] == color_idx:
                    linestr += ascii_matrix[y, x]
                    acc_dominant += 1
                else:
                    linestr += "1"
            linestr += "\n"
            layer.append(linestr)
        layers.append(layer)
        colors_comparison[str(color_idx)] = acc_dominant
    color_max = int(max(colors_comparison, key=colors_comparison.get))
    return layers, color_max

def image_to_ascii_by_color(image_path, output_path="ascii_art_by_color.txt", width=100, n_colors=4, export_mode=0):
    image = Image.open(image_path)
    image = enhance_saturation(image, factor=1.7)     # Augmentation de saturation
    image = adjust_brightness(image, factor=0.9)      # Réduction de luminosité
    image = enhance_sharpness(image, factor=2.0)      # Augmentation de netteté
    resized = resize_image(image, width)
    gray = grayify(resized)
    color = colorify(resized)

    ascii_str = pixels_to_ascii(gray)
    colors = dominant_colors(color, n_colors)
    labels = assign_color_labels(color, colors)

    ascii_width, ascii_height = resized.size
    layers, color_skip = build_color_ascii_layers(ascii_str, labels, ascii_width, ascii_height, n_colors)

    if export_mode == 0:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"__VISUAL{export_mode}__\n")
            f.write(f"__NBCOLORS__{n_colors - 1}\n")
            for idx, layer in enumerate(layers):
                if idx != color_skip:
                    r, g, b = colors[idx]
                    f.write(f"__COLORR__{r}\n")
                    f.write(f"__COLORG__{g}\n")
                    f.write(f"__COLORB__{b}\n")
                    for line in layer :
                        f.write(line)
                    f.write("__ENDVISUAL__\n")
    else:
        try:
            with open(output_path, 'r', encoding='utf-8') as file_txt:
                content = [line for line in file_txt]
        except FileNotFoundError:
            content = []

        # Suppression de l'ancien bloc correspondant à ce mode
        start_idx = None
        end_idx = None
        counter_colors = 0
        for i, line in enumerate(content):
            if line == f"__VISUAL{export_mode}__\n":
                start_idx = i
                nb_colors = int(content[i+1].split("__NBCOLORS__")[1].strip())
            elif start_idx is not None and line == "__ENDVISUAL__\n":
                if counter_colors == nb_colors-1 :
                    end_idx = i
                    print(end_idx)
                    break
                else :
                    counter_colors += 1

        if start_idx is not None and end_idx is not None:
            del content[start_idx:end_idx + 1]

        # Insertion du nouveau bloc
        new_block = [f"__VISUAL{export_mode}__\n",
                     f"__NBCOLORS__{n_colors - 1}\n"]
        for idx, layer in enumerate(layers):
            if idx != color_skip:
                r, g, b = colors[idx]
                new_block.append(f"__COLORR__{r}\n")
                new_block.append(f"__COLORG__{g}\n")
                new_block.append(f"__COLORB__{b}\n")
                for line in layer :
                    new_block.append(line)
                new_block.append("__ENDVISUAL__\n")

        # Insertion à la fin du fichier ou juste après la suppression
        if start_idx is not None and end_idx is not None:
            index = start_idx
            for line in new_block :
                content.insert(index, line)
                index += 1
        else:
            content.extend(new_block)

        with open(output_path, "w", encoding="utf-8") as f:
            for line in content:
                f.write(line)