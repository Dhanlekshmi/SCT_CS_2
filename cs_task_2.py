from PIL import Image
import numpy as np
import random

# Encryption key
ENCRYPTION_KEY = 50
SWAP_SEED = 12345  # Seed for reproducible swapping

def load_image(image_path):
    return Image.open(image_path)

def save_image(image_array, save_path):
    image = Image.fromarray(image_array.astype(np.uint8))
    image.save(save_path)

def encrypt_pixels_math(image_array, key):
    # Add key to each pixel value and apply modulo to stay in 0-255 range
    return (image_array + key) % 256

def decrypt_pixels_math(image_array, key):
    return (image_array - key) % 256

def swap_pixels(image_array):
    flat = image_array.reshape(-1, image_array.shape[-1])
    indices = list(range(len(flat)))
    random.seed(SWAP_SEED)
    random.shuffle(indices)
    return flat[indices].reshape(image_array.shape), indices

def unswap_pixels(image_array, indices):
    flat = image_array.reshape(-1, image_array.shape[-1])
    unswapped = np.zeros_like(flat)
    for i, idx in enumerate(indices):
        unswapped[idx] = flat[i]
    return unswapped.reshape(image_array.shape)

def encrypt_image(image_path, output_path):
    image = load_image(image_path).convert("RGB")
    array = np.array(image)

    # Apply pixel value modification
    encrypted_array = encrypt_pixels_math(array, ENCRYPTION_KEY)

    # Swap pixels
    swapped_array, swap_indices = swap_pixels(encrypted_array)

    save_image(swapped_array, output_path)
    print("Image encrypted and saved to", output_path)
    return swap_indices

def decrypt_image(encrypted_path, output_path, swap_indices):
    encrypted_image = load_image(encrypted_path).convert("RGB")
    array = np.array(encrypted_image)

    # Unswap pixels
    unswapped_array = unswap_pixels(array, swap_indices)

    # Undo pixel value modification
    decrypted_array = decrypt_pixels_math(unswapped_array, ENCRYPTION_KEY)

    save_image(decrypted_array, output_path)
    print("Image decrypted and saved to", output_path)

# Example usage:
# Make sure to change the file paths accordingly
if __name__ == "__main__":
    input_path = "input.jpg"
    encrypted_path = "encrypted.png"
    decrypted_path = "decrypted.png"

    swap_indices = encrypt_image(input_path, encrypted_path)
    decrypt_image(encrypted_path, decrypted_path, swap_indices)
