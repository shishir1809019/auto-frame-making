import json
from PIL import Image, ImageDraw, ImageFilter,ImageFont
import requests


  
# Opening JSON file
f = open('./frameJSON.json',encoding="utf8")
  
# returns JSON object as  a dictionary

data = json.load(f)
  
# Iterating through the json list

for i in data:
    print(i['Name'])
    print(i['Student ID'])

    #get the photo
    id = i['Upload Your decent Photo'].split("=")[1]
    print("Id:", id)
    url = "https://drive.google.com/uc?export=view&id={0}".format(id)
    print(url)

    response = requests.get(url, stream=True)
    #resize the photo and set it in the tamplate
    img = Image.open(response.raw)

    newsize = (610, 610)
    img = img.resize(newsize)

    mask_im = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask_im)
    draw.ellipse((0, 0, 590, 590), fill=255)

    mask_im = mask_im.filter(ImageFilter.GaussianBlur(6))


    tamplate = Image.open("./template.png")
    tamplate.paste(img, (200, 150), mask_im)

    #draw name and id in the tamplate and align center(horizontal)
    W1, H1 = (600, 200)
    W2, H2 = (800, 200)

    name = "{0}".format(i['Name'])
    studentID ="{0}".format(i['Student ID'])

    image = tamplate
    font = ImageFont.truetype("arial.ttf",60, encoding="unic")
    draw = ImageDraw.Draw(image)
    w1,h1 = draw.textsize(name)
    w2,h2 = draw.textsize(studentID)
    
    draw.text(((W1-w1)/2,800), name , fill=(255, 69, 0), font=font)
    draw.text(((W2-w2)/2, 850), studentID , fill=(255, 69, 0), font=font)
    # image = image.convert('RGB')

    #save or show the final image
    image.save("{0}.png".format(i['Name']), format="png")
    # image.show()
  
# Closing file
f.close()