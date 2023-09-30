# invokeai-Tile to Gif Node
Custom Node for InvokaAI to take a tiled image and convert it into an image collection, or take an image collection and convert it into an animated gif

Simply download the `tileToGif.py` node file and add it to the `invokeai/app/invocations` folder in your Invoke AI install location. If you used the automated installation, this can be found inside the `.venv/Lib/site-packages/invokeai/app/invocations` folder. 

The file contains two nodes:
# Tile to Image collection
Takes an image and splits it into equal sized smaller images based on provided dimesnions of how many images to cut it into
ie, an image with four quadrants can be split into four images be providing 2x2 as the dimensions

# Image Collection to Gif
Takes an image collection and uses PIL to combine the given images, in the order it received them, into an animated gif with options for framerate and looping. Invokeai doesn't support animted gifs in the webui, so there is a field for a save directory. Provide an absolute path along with a name for the file, and the gif will be saved to that location when invocation is complete. If no directory is given, it is saved to the user's home directory as specified by the python function `os.path.expanduser("~")`. If no filename can be parsed from the string, the gif will be named `TileToGif.gif`. Python will attempt to make the specified directory if one is specified, and this saved file will overwrite another file in the same location (So, if invocation is run twice without changing the path, the gif made in the previous invocation will be overwritten)
