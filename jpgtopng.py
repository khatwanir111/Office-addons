from PIL import Image

# To convert the Image From JPG to PNG
def jpg_to_png(IMG_PATH):
  img = Image.open(IMG_PATH).convert('RGB')
  img.save("Image_1.png", "PNG")
 
# To convert the Image From PNG to JPG
def png_to_img(PNG_PATH):
  img = Image.open(PNG_PATH).convert('RGB')
  img.save("Image_1.jpg", "JPEG")

png_to_img("file.png")
jpg_to_png("Image.jpg")
