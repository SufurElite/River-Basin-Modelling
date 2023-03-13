from  river import River 
from boxcounting import imageToFracDim 
import numpy as np

def main():
    imagePath = "satellite-images/egypt_3-0.jpg"
    fracDim = imageToFracDim(imagePath)
    print(fracDim)
    riv = River(fracDim, latLength=10)
    riv.pprint()
    riv.plotGraph(save=True)

if __name__=="__main__":
    main()