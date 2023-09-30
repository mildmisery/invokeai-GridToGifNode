# invokeai-Tile to Gif Node
Custom Node for InvokaAI to take a tiled image and convert it into an image collection, or take an image collection and convert it into an animated gif

Simply download the .py node file and add it to the `invokeai/app/invocations` folder in your Invoke AI install location. If you used the automated installation, this can be found inside the `.venv\Lib\site-packages\invokeai\app\invocations` folder. 

The file contains two nodes:
# Tile to Image collection
Takes an image and splits it into equal sized smaller images based on provided dimesnions of how many images to cut it into
ie, an image with four quadrants can be split into four images be providing 2x2 as the dimensions

# Image Collection to Gif
Takes an image collection and uses PIL to combine the given images, in the order it received them, into an animated gif with options for framerate and looping
