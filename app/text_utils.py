def int_to_binary(num):
    """
    Convert integer values to binary representation
    """
    x = [int(x) for x in bin(num)[2:]]
    x = [0]*(8-len(x)) + x
    return x

def binary_to_char_ascii(binary_list):
    """
    Converts binary to its character representation
    """
    ascii_value = bin_to_int(binary_list)
    return chr(ascii_value)

def bin_to_int(binary_list):
    """
    Convert list to integer representation
    """
    binary_string = ''.join(str(bit) for bit in binary_list)
    return int(binary_string, 2)

def char_to_binary(c):
    """
    Convert a character into its ascii value
    """
    x = [int(x) for x in bin(ord(c))[2:]]
    x = [0]*(8-len(x)) + x
    return x

def text_to_binary(text: str):
    # text_list = text.split(" ")
    # encode length of each word to the start
    num_iterations = int_to_binary(len(text))
    response = [num_iterations]
    for char in text + '\0':
        response.append(char_to_binary(char))
    return response

#Specific to this implementation
def append_bit(num):
    if(num%2==0):
        return 0
    else:
        return 1
