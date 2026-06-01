#!/usr/bin/env python3
"""
Generate a random one-time-pad PNG image using OpenCV.
"""

import cv2
import numpy as np


# Generate RGB pad (1024x576)
img = np.random.randint(0, 256, (576, 1024, 3), dtype=np.uint8)

# Save output
cv2.imwrite('pad.png', img)
print('Generated RGB pad: pad.png (1024x576)')
print('Done!')
