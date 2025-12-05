import numpy as np
import matplotlib.pyplot as plt
from skimage import io, color, feature
from skimage.metrics import structural_similarity as ssim

plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['image.cmap'] = 'gray'

