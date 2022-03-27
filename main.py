from PIL import Image 
import random
import json

# Each image is made up a series of traits
# The weightings for each trait drive the rarity and add up to 100%

background = ["Space, By Tonya","Spanish Fields","Sunrise on the Road","Overseeing the Islands","You're in the 'Gaming World'","The one with the Fantom logo","Lost in the Blue","The Flare","Grass Clippings","The Depth","The Crayons have melted","Sun over the Grass"]
background_weights = [7,7,7,7,7,7,7,7,7,7,13,10]

body = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15"] 
body_weights = [10,10,10,10,7,7,6,5,5,5,5,5,5,3,2]

eyes = ["1", "2", "3", "4", "5","6"] 
eyes_weights = [40,20,15,10,10,5]

mouth = ["1", "2", "3", "4", "5","6","7","8","9"] 
mouth_weights = [30,15,15,10,15,5,5,5,1]

extra = ["1","none","3","4","5","6","7"]
extra_weights = [30,30,0,15,3,2,15]


# Dictionary variable for each trait. 
# Eech trait corresponds to its file name
background_files = {
    "Space, By Tonya": "bg1",
    "Spanish Fields": "bg2",
    "Sunrise on the Road": "bg3",
    "Overseeing the Islands": "bg4",
    "You're in the 'Gaming World'": "bg5",
    "The one with the Fantom logo": "bg6",
    "Lost in the Blue": "bg7",
    "The Flare": "bg8",
    "Grass Clippings": "bg9",
    "The Depth": "bg10",
    "The Crayons have melted": "bg11",
    "Sun over the Grass": "bg12"
}

body_files = {
    "1": "body1",
    "2": "body2",
    "3": "body3",
    "4": "body4",
    "5": "body5",
    "6": "body6",
    "7": "body7",
    "8": "body8",
    "9": "body9",
    "10": "body10",
    "11": "body11",
    "12": "body12",
    "13": "body13",
    "14": "body14",
    "15": "body15",
}

eyes_files = {
    "1": "eyes1",
    "2": "eyes2",
    "3": "eyes3",
    "4": "eyes4",
    "5": "eyes5",
    "6": "eyes6"
}

mouth_files = {
    "1": "mouth1",
    "2": "mouth2",
    "3": "mouth3",
    "4": "mouth4",
    "5": "mouth5",
    "6": "mouth6",
    "7": "mouth7",
    "8": "mouth8",
    "9": "mouth9"
}

extra_files = {
    "1": "extra1",
    "none": "extra2",
    "3": "extra3",
    "4": "extra4",
    "5": "extra5",
    "6": "extra6",
    "7": "extra7"
}
## Generate Traits

TOTAL_IMAGES = 3333 # Number of random unique images we want to generate

all_images = [] 

# A recursive function to generate unique image combinations
def create_new_image():
    
    new_image = {} #

    # For each trait category, select a random trait based on the weightings 
    new_image["Background"] = random.choices(background, background_weights)[0]
    new_image["Body"] = random.choices(body, body_weights)[0]
    new_image["Eyes"] = random.choices(eyes, eyes_weights)[0]
    new_image["Mouth"] = random.choices(mouth, mouth_weights)[0]
    new_image["Extra"] = random.choices(extra, extra_weights)[0]

    if False:
        return create_new_image()
    else:
        return new_image
    
    
# Generate the unique combinations based on trait weightings
for i in range(TOTAL_IMAGES): 
    
    new_trait_image = create_new_image()
    
    all_images.append(new_trait_image)

    # Returns true if all images are unique
def all_images_unique(all_images):
    seen = list()
    return not any(i in seen or seen.append(i) for i in all_images)

print("Are all images unique?", all_images_unique(all_images))

# Add token Id to each image
i = 0
for item in all_images:
    item["tokenId"] = i
    i = i + 1

print(all_images)

# Get Trait Counts

background_count = {}
for item in background:
    background_count[item] = 0
    
body_count = {}
for item in body:
    body_count[item] = 0
    
eyes_count = {}
for item in eyes:
    eyes_count[item] = 0

mouth_count = {}
for item in mouth:
    mouth_count[item] = 0

extra_count = {}
for item in extra:
    extra_count[item] = 0

for image in all_images:
    background_count[image["Background"]] += 1
    body_count[image["Body"]] += 1
    eyes_count[image["Eyes"]] += 1
    mouth_count[image["Mouth"]] += 1
    extra_count[image["Extra"]] += 1

    
#print(body_count)
#print(eyes_count)
#print(mouth_count)

#### Generate Metadata for all Traits 
METADATA_FILE_NAME = './metadata/all-traits.json'; 
with open(METADATA_FILE_NAME, 'w') as outfile:
    json.dump(all_images, outfile, indent=4)

#### Generate Images    
for item in all_images:

    im0 = Image.open(f'./trait-layers/backgrounds/{background_files[item["Background"]]}.png').convert('RGBA')
    im1 = Image.open(f'./trait-layers/body/{body_files[item["Body"]]}.png').convert('RGBA')
    im2 = Image.open(f'./trait-layers/eyes/{eyes_files[item["Eyes"]]}.png').convert('RGBA')
    im3 = Image.open(f'./trait-layers/mouth/{mouth_files[item["Mouth"]]}.png').convert('RGBA')
    im4 = Image.open(f'./trait-layers/extras/{extra_files[item["Extra"]]}.png').convert('RGBA')

    #Create each composite
    com0 = Image.alpha_composite(im0, im1)
    com1 = Image.alpha_composite(com0, im3)
    com2 = Image.alpha_composite(com1, im4)
    com3 = Image.alpha_composite(com2, im2)

    #Convert to RGB
    rgb_im = com3.convert('RGB')
    file_name = str(item["tokenId"]) + ".png"
    rgb_im.save("./images/" + file_name)
    print("#" + str(item["tokenId"]) + " done!")
#### Generate Metadata for each Image    

f = open('./metadata/all-traits.json',) 
data = json.load(f)


IMAGES_BASE_URI = "https://github.com/Pokesi/Ultimates/blob/main/images/"
PROJECT_NAME = "Ultimate Fantoms #"

def getAttribute(key, value):
    return {
        "trait_type": key,
        "value": value 
    }
for i in data:
    token_id = i['tokenId']
    token = {
        "image": IMAGES_BASE_URI + str(token_id) + '.png',
        "id": token_id,
        "name": PROJECT_NAME + '' + str(token_id),
        "attributes": []
    }
    token["attributes"].append(getAttribute("body", i["Body"]))
    token["attributes"].append(getAttribute("eyes", i["Eyes"]))
    token["attributes"].append(getAttribute("mouth", i["Mouth"]))
    token["attributes"].append(getAttribute("extra", i["Extra"]))
    token["attributes"].append(getAttribute("background", i["Background"]))

    with open('./metadata/' + str(token_id), 'w') as outfile:
        json.dump(token, outfile, indent=4)
f.close()