"""
Simple demo of the imshow function.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.cbook as cbook

image_file = cbook.get_sample_data('ada.png')
image = plt.imread(image_file)
patch = patches.Circle((260, 400), radius=50)

im = plt.imshow(image)
# im.set_clip_path(patch)
plt.show()