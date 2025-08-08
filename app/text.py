"""
Functions to embed text into an image
"""
import numpy as np
import matplotlib.pyplot as plt
from text_utils import text_to_binary, append_bit, bin_to_int, binary_to_char_ascii
from typing import Union

def encode_message(img_path: Union[str, np.ndarray], text:str):
    """
    Hide a string using ASCII inside the LSB of an image
    """
    if isinstance(img_path, str):
        img_array: np.ndarray = plt.imread(img_path)
    elif isinstance(img_path, np.ndarray):
        img_array = img_path
    else:
        raise ValueError("Incorrect image file given here! Unable to encode message data")
    
    if img_array.dtype != np.uint8:
        img_array = (img_array * 255).astype(np.uint8)
    
    message = np.asarray(text_to_binary(text), dtype=object).flatten()

    img_array_rounded = img_array - img_array%2  
    flat_img = img_array_rounded.flatten()
    
    if len(message) > img_array_rounded.size:
        raise ValueError("Message is too long to encode in the image.")
    
    for i in range(len(message)):
        flat_img[i] = flat_img[i] + int(message[i])

    return flat_img.reshape(img_array.shape)


def decode_message(img_arr):
    bit_arr = np.array([2**(7-i) for i in range(8)]) #length of each bit
    decoded_img_arr = img_arr.flatten() #flatten the image
    num_chars: int = 0 #int value
    bit_char_value = []
    still_reading = True
    result = ""

    for i in range(8):
        bit_char_value.append(append_bit(decoded_img_arr[i]))
    num_chars = bin_to_int(bit_char_value)

    for i in range(num_chars + 1):
        curr = []
        for j in range(8):
            curr.append(append_bit(decoded_img_arr[i*8 + j]))
        result += binary_to_char_ascii(curr)
    
    return result
