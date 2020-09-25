from PIL import Image, ImageDraw
import colorsys


def comparePixels(pix1, pix2):
    return pix1[0][0] > pix2[0][0]


# end def comparePixels(pix1,pix2):


def storePixels(im):
    width = int(im.size[0])
    height = int(im.size[1])

    # store ppixels inout double tuple format.
    pixel_array = []
    yiq_pixels = []

    for i in range(width):  # for loop for x position
        for j in range(height):  # for loop for y position
            # get r and g and b values of pixel at position
            r, g, b = im.getpixel((i, j))
            #yiq conversion is expecting float between 0-1
            yiq = colorsys.rgb_to_yiq(r/255,g/255,b/255)
            yiq_pixels.append([yiq, (i,j)])
            pixel_array.append([(r, g, b), (i, j)])
        # end for j
    # end for i
    return (pixel_array, yiq_pixels) #return both lists in a tuple
# end def storePixels(im):

def pixelsToImage(im, pixels):
    outimg = Image.new("RGB", im.size)

    #list element 0, tuple value 0, inner tuple value 0
    if type(pixels[0][0][0]) == float:  #dealing with YIQ
        print("yiq")
        yiq_out = []
        for p in pixels:
            r,g,b = colorsys.yiq_to_rgb(p[0][0], p[0][1], p[0][2])
            #rgb comes out of conversion as 0-1 float
            r,g,b = int(r*255), int(g*255), int(b*255)
            yiq_out.append((r,g,b))
        outimg.putdata(yiq_out)
        #end for p in pixels:
    else:   #dealing with RGB
        outimg.putdata([p[0] for p in pixels])
    #outimg.show()
    return outimg
# end def pixelsToImage(im, pixels):

def pixelsToPoints(im, pixels):
    #default background color is black
    for p in pixels:
        if type(p[0][0]) == float:  #YIQ value
            im.putpixel(p[1],
                        tuple([int(v*255) for v in colorsys.yiq_to_rgb(p[0][0], p[0][1], p[0][2])]))
        else:
            im.putpixel(p[1], p[0])
    #im.show()
# enddef pixelsToPoints(im, pixels):

def grayScale(im, pixels):
    draw = ImageDraw.Draw(im)
    for px in pixels:
        gray_av = int((px[0][0] + px[0][1] + px[0][2])/3)
        draw.point(px[1], (gray_av, gray_av, gray_av))
#end of def grayScale(im, pixels):
