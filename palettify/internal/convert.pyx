cdef float color_distance(tuple col1, tuple col2):
    return abs(col1[0] - col2[0]) + abs(col1[1] - col2[1]) + abs(col1[2] - col2[2])

cdef void _apply_palette(pixels, list palette, unsigned int min_x, unsigned int max_x, unsigned int height):
    cdef dict cached_colors = {}
    cdef unsigned int x, y
    cdef tuple pixel_color, color 
    cdef list distances
    for x in range(min_x, max_x):
        for y in range(height):
            try:
                pixel_color = pixels[x, y]
            except IndexError:
                break

            if pixel_color in cached_colors:
                pixels[x, y] = cached_colors[pixel_color]
                continue

            distances = []
            for color in palette:
                distances.append(color_distance(color, pixel_color))

            color = palette[distances.index(min(distances))]
            cached_colors[pixel_color] = color

            pixels[x, y] = color

def apply_palette(pixels, palette, min_x, max_x, height):
    _apply_palette(pixels, palette, min_x, max_x, height)