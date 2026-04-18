import numpy as np

width = 50
height = 50

sugar_map = np.zeros((height, width))

for y in range(height):
    for x in range(width):
        # sugar increases along the y-direction
        gradient = y / (height - 1)

        # add some random noise
        noise = np.random.normal(0, 0.1)

        value = gradient + noise

        # limit range
        value = max(0, min(1, value))

        # map to 1–4
        sugar_map[y, x] = int(1 + 3 * value)

np.savetxt("sugar-map-coastal.txt", sugar_map, fmt="%d")