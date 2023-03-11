from  river import River 
from boxcounting import imageToFracDim 
import numpy as np

def main():
    imagePath = "egypt_3-0.jpg"
    fracDim = imageToFracDim(imagePath)
    print(fracDim)
    riv = River(fracDim, latLength=10)
    print(np.matrix(riv.areaMatrix))

if __name__=="__main__":
    main()