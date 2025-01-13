# Create an image (raw 8-bit greyscale) with a centered polygonal number
# as filled circles. The image can be opened as a .data file in GNU IMP.

import math

LAY_SPAC = 18    # spacing between layers
LAYERS   = 10
CIRC_RAD = 4     # radius of each circle
VERTICES = 8     # e.g. 8 for centered octagonal numbers
BG_COLOR = 0xff  # 0x00-0xff
FG_COLOR = 0x00  # 0x00-0xff
MARGINS  = 50    # pixels
OUT_FILE = "centered-polygonal.data"  # output file (will be overwritten!)

def get_circle_coords(edges, layer):
    # get center coordinates of each filled circle;
    # edges: e.g. 8 for centered octagonal numbers;
    # layer: which layer from inside; 0 or greater;
    # generate: (x, y) (floats with 0 at center of image)

    # vertices (on a circle)
    vertices = []
    for i in range(edges):
        angle = (i + .5) / VERTICES * math.tau
        x = math.sin(angle) * layer * LAY_SPAC
        y = math.cos(angle) * layer * LAY_SPAC
        vertices.append((x, y))
        yield (x, y)

    # add pixels in a straight line between vertices
    for i in range(edges):
        for j in range(1, layer):
            thisVert = vertices[i]
            nextVert = vertices[(i+1)%VERTICES]
            x = thisVert[0] + (nextVert[0] - thisVert[0]) * j / layer
            y = thisVert[1] + (nextVert[1] - thisVert[1]) * j / layer
            yield (x, y)

def get_pixel_coords(cx, cy):
    # cx, cy: center coordinates;
    # generate: coordinates of each pixel
    for py in range(-CIRC_RAD, CIRC_RAD + 1):
        maxAbsPx = math.floor(math.sqrt(CIRC_RAD**2 - py**2))
        yield from (
            (cx + px, cy + py) for px in range(-maxAbsPx, maxAbsPx + 1)
        )

def main():
    # image width & height
    width = round(2 * (LAYERS - 1) * LAY_SPAC + 2 * CIRC_RAD + MARGINS)
    print("Width & height:", width)

    # draw
    image = bytearray(width ** 2 * bytes((BG_COLOR,)))
    for layer in range(0, LAYERS):
        for (cx, cy) in get_circle_coords(VERTICES, layer):
            cx = round(width / 2 + cx)
            cy = round(width / 2 + cy)
            for (px, py) in get_pixel_coords(cx, cy):
                image[py*width+px] = FG_COLOR

    # save
    with open(OUT_FILE, "wb") as handle:
        handle.seek(0)
        handle.write(image)

main()
