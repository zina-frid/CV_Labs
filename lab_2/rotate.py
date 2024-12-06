from PIL import Image, ImageEnhance
import random
import os


def transform_and_save(image_path, output_dir):
    """Applies various transformations to an image and saves the results."""
    try:
        img = Image.open(image_path)
    except FileNotFoundError:
        print(f"Error: File '{image_path}' not found.")
        return
    except Exception as e:
        print(f"Error opening image: {e}")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    transformations = [
        ("rotated", lambda img, i: img.rotate(random.randint(0, 360), expand=True)),
        (
            "scaled",
            lambda img, i: img.resize((int(img.width * 0.8), int(img.height * 0.8))),
        ),
        (
            "cropped",
            lambda img, i: img.crop(
                (
                    img.width // 4,
                    img.height // 4,
                    3 * img.width // 4,
                    3 * img.height // 4,
                )
            ),
        ),
        ("bright", lambda img, i: ImageEnhance.Brightness(img).enhance(1.5)),
        ("contrast", lambda img, i: ImageEnhance.Contrast(img).enhance(1.5)),
        ("flipped_horizontal", lambda img, i: img.transpose(Image.FLIP_LEFT_RIGHT)),
        ("flipped_vertical", lambda img, i: img.transpose(Image.FLIP_TOP_BOTTOM)),
    ]

    for name, transformation in transformations:
        transformed_img = transformation(
            img.copy(), 0
        )  # Apply transformation to a copy to avoid modifying the original
        output_path = os.path.join(output_dir, f"{name}.png")
        try:
            transformed_img.save(output_path)
            print(f"Image saved as '{output_path}'")
        except Exception as e:
            print(f"Error saving image '{output_path}': {e}")


# Example usage:
image_path = "src/dog_face.jpg"  # Replace with your image path
output_directory = "transformed_images"

transform_and_save(image_path, output_directory)
