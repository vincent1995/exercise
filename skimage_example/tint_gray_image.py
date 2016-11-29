import matplotlib.pyplot as plt
from skimage import data
from skimage import color
from skimage import img_as_float
from skimage import io

image = io.imread("coldplay.jpg")
print(image.shape)
print(image)

red_multiplier = [1, 0, 0]
yellow_multiplier = [1, 1, 1]
print(yellow_multiplier*image)
fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(8, 4), sharex=True, sharey=True)
ax1.imshow()
ax2.imshow(yellow_multiplier * image)
ax1.set_adjustable('box-forced')
ax2.set_adjustable('box-forced')
plt.show()
