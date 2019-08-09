import base64
import struct
from PIL import Image
import sys
import re


def read_blocks(stream, block_size = 10000000):
    '''
    Finds blocks delimited by <<< >>>
    '''
    regex = r'\s*<<<(.*?)>>>\s*(.*)'
    buffer = ''
    count = 0
    end_reached = False

    while not end_reached:
        data = stream.read(block_size)

        if not data:
            print("Unexpected EOF")
            sys.exit(-1)

        buffer += data

        match = re.match(regex, buffer, re.MULTILINE | re.DOTALL)

        while match:
            block = match.group(1)
            buffer = match.group(2)

            # Decode base64
            decoded = base64.b64decode(block)

            if len(decoded) == 4:
                end_reached = True
            else:
                yield decoded

            match = re.match(regex, buffer, re.MULTILINE | re.DOTALL)


def block_to_image(block):
    '''
    Takes a block of data, base64-decodes it and turns it into an image.
    '''
    # Read two little endian 32 bit integers
    width, height = struct.unpack('<2I', block[:8])

    # Read groups of 3 unsigned chars
    pixels = list(struct.iter_unpack("3B", block[8:]))

    # Create image
    image = Image.new('RGB', (width, height))

    # Get pixel buffer
    image_buffer = image.load()

    # Write pixels to buffer
    for y in range(height):
        for x in range(width):
            i = y * width + x
            image_buffer[x, y] = pixels[i]

    # Return image
    return image


def read_frames(stream):
    return ( block_to_image(block) for block in read_blocks(stream) )
