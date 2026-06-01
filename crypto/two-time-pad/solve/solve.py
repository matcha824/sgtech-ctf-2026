import cv2

# Load the two encrypted images
img1 = cv2.imread('picture_1.png')
img2 = cv2.imread('picture_2.png')

# XOR the images
result = cv2.bitwise_xor(img1, img2)

# Save the solution
cv2.imwrite('solution.png', result)
print('Solution saved to solution.png')
