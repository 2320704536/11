
import numpy as np
from PIL import Image

def apply_cinematic_pipeline(img, contrast=0.2):
    arr=np.asarray(img)/255
    arr=(arr-0.5)*(1+contrast)+0.5
    arr=np.clip(arr,0,1)
    return Image.fromarray((arr*255).astype(np.uint8))
