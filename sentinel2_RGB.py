## Produce RGB true color composite map (4,3,2) from Sentinel-2 images
import matplotlib.image as mpimg
import numpy as np
from PIL import Image
import scipy.misc

Image.MAX_IMAGE_PIXELS = 1000000000

## Path for the s2 images
path = r'C:\Users\Junqian Wang\Downloads\test\s2'

print('Reading B04.jp2...')
img_red = mpimg.imread(path + '\T10SFF_20180917T185019_B04.jp2')
print('Reading B03.jp2...')
img_green = mpimg.imread(path + '\T10SFF_20180917T185019_B03.jp2')
print('Reading B02.jp2...')
img_blue = mpimg.imread(path + '\T10SFF_20180917T185019_B02.jp2')

img = np.dstack((img_red, img_green, img_blue))

scipy.misc.toimage(img, cmin=1, cmax=4095).save(path + '\T10SFF_20180917T185019_RGB.jpeg')
