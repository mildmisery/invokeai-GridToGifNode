import os
import re

from PIL import Image

from invokeai.app.invocations.primitives import (ImageCollectionOutput,
                                                 ImageField)
from invokeai.app.models.image import ImageCategory, ResourceOrigin

from .baseinvocation import (BaseInvocation, InputField, InvocationContext,
                             UIType, invocation)


@invocation(
    'tileToImageCollection', 
    title="Tile to Image Collection", 
    version="1.0.0"
    )
class TileToImageCollectionInvocation(BaseInvocation):
    '''Crops an image by tile dimension and converts them to a gif'''
    
    #Inputs
    image: ImageField = InputField(description="The input tiled image")
    dimX: int = InputField(default=2, ge=2, le=256, description="X dimension of tile (how many horizontal tiles)")
    dimY: int = InputField(default=2, ge=2, le=256, description="Y dimension of tile (how many vertical tiles)")
    
    def invoke(self, context: InvocationContext) -> ImageCollectionOutput:
        # Load the image using InvokeAI's predefined Image Service. Returns the PIL image.
        tiledImage = context.services.images.get_pil_image(self.image.image_name)
        
        imageTiles = imageUtils.tileToArray(
            tiledImage, 
            self.dimX, 
            self.dimY,
        )
        
        # Save the image using InvokeAI's predefined Image Service. Returns the prepared PIL image.
        imageCollection = []
        for i in range(len(imageTiles)):
            image_dto = context.services.images.create(
                image=imageTiles[i],
                image_origin=ResourceOrigin.INTERNAL,
                image_category=ImageCategory.OTHER,
                node_id=self.id,
                session_id=context.graph_execution_state_id,
                is_intermediate=self.is_intermediate,
                workflow=self.workflow,
            )
            imageCollection.append( ImageField(image_name=image_dto.image_name))

        # Returning the Image
        return ImageCollectionOutput( collection=imageCollection )
        
        
@invocation(
    'ImageCollectionToGif', 
    title="Image Collection to Gif", 
    version="1.0.0"
    )
class ImageCollectionToGif(BaseInvocation):
    '''Takes a collection of images and converts them to a gif to save in a given directory'''
    
    #Inputs
    collection: list[ImageField] = InputField(
        default_factory=list,
        description="The image frames Collection",
        ui_type=UIType.ImageCollection,
    )
    gif_out_path: str = InputField(default='', description="Absolute path and filename of output gif")
    fps: int = InputField(default=4, ge=4, le=60, description="Number of frames per second to play the gif back at (4-60)")
    loop_gif: bool = InputField(default=True, description="Should the gif loop")
    open_gif: bool = InputField(default=False, description="Open the Gif in your system's default image viewer")
    
    def invoke(self, context: InvocationContext) -> ImageCollectionOutput:
        imageFieldArray = self.collection
        saveDir = os.path.dirname(self.gif_out_path)
        filename = os.path.basename(self.gif_out_path)

        defaultName = r"TileToGif.gif"
        fileExtension = r".gif"

        if not len(re.findall(r'\S+\.' + re.escape(fileExtension), filename, re.IGNORECASE)) > 0:
            if len(filename) > 0:
                filename += fileExtension
            else: 
                filename = defaultName

        try:
            if not os.path.exists(saveDir):
                os.makedirs(saveDir)
        except FileNotFoundError as e:
            print(f"Error creating save directory for your gif: {e}")
            print(f"Saving to a default location: {os.path.expanduser('~')}")
            saveDir = os.path.expanduser("~")

        gifSavePath = os.path.join(saveDir, filename)

        imageArray = []
        for image in imageFieldArray:
            imageArray.append(context.services.images.get_pil_image(image.image_name))
                
        newGif = imageUtils.createGif(
            imageArray, 
            self.fps, 
            not self.loop_gif,
            gifSavePath
        )

        if self.open_gif:
            newGif = Image.open(saveDir + filename)
            print("Open?")
            newGif.show()
        
        return ImageCollectionOutput(collection=self.collection)
        
        
class imageUtils(object):
    def tileToArray(tiledImage, dimX, dimY):
        w, h = tiledImage.size

        spacY = h / dimY
        spacX = w / dimX

        imageTiles = []

        #forward move
        for j in range(dimY):
            for i in range(dimX):
                xrange1 = int(i*spacX)
                xrange2 = int((i+1)*(spacX))
                yrange1 = int(j*spacY)
                yrange2 = int((j+1)*(spacY))
                crop_img = tiledImage.crop((xrange1,yrange1,xrange2,yrange2))
                #if saveIndividuals:
                #    curImageName = str(j) + 'x' + str(i) + '.png'
                #    crop_img.save(os.path.join(saveDir, curImageName), 'png')
                imageTiles.append(crop_img)
        return imageTiles
        
    def createGif(imageTiles, framerate, loopIterations, savePath):
        durationInMs = int(1000 * 1/framerate);
        imageTiles[0].save(fp=savePath, format='GIF', append_images=imageTiles[1:], save_all=True, duration=durationInMs, loop=loopIterations)