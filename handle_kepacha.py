import os
from google.cloud import vision

from PIL import Image

def solve_kepacha():

    os.environ['GOOGLE_APPLICATION_CREDENTIALS']="./amiable-nova-356209-0557b45327a5.json"
    img=Image.open("kepacha.png")
    client = vision.ImageAnnotatorClient()
    image = vision.AnnotateImageRequest()
    
        
    cropped_img=img.crop((0,270//3,300,(270*2)//3))
    cropped_img.save("cut.png")

    with open("cut.png" , 'rb' ) as kp:
        binary_content = kp.read()
  
    response = client.text_detection({
    'content': binary_content})
    
    del img
    answer = (response.text_annotations[0].description).replace(" ","").replace("\n","").lower()
    
    ### we can verify here if answer is not 4 char long or is empty than  we can raise an error
    return answer

def solve_small_kepacha():
    
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']="./amiable-nova-356209-0557b45327a5.json"
    img=Image.open("kepacha.png")
    client = vision.ImageAnnotatorClient()
    image = vision.AnnotateImageRequest()
    


    with open("kepacha.png" , 'rb' ) as kp:
        binary_content = kp.read()
    
    response = client.text_detection({
    'content': binary_content})
    

    del img
    answer = (response.text_annotations[0].description).replace(" ","").replace("\n","")
    return answer
    