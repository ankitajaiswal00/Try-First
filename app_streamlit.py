import streamlit as st
from PIL import Image
from script import predict
import time

from evaluate import execute
from pose_parser import pose_parse

st.title("Virtual Try ON")


cloths = ['000003','000011','000013','000108','000254','000308','000627','001247','001401','000649','001500','001719','002061','002337','002385','002599','003086','005632','006158','006159' ]
c = []
for i in range(len(cloths)):
	name = str(cloths[i]) + '_1.jpg'
	c.append(Image.open('./Database/val/cloth/' + name))
#cloth1 = Image.open('./Database/val/cloth/001616_1.jpg')
#cloth2 = Image.open('./Database/val/cloth/001517_1.jpg')
#cloth3 = Image.open('./Database/val/cloth/001500_1.jpg')
#cloth4 = Image.open('./Database/val/cloth/001439_1.jpg')
#cloth5 = Image.open('./Database/val/cloth/000068_1.jpg')
#cloth6 = Image.open('./Database/val/cloth/000108_1.jpg')


slidebar = []
for i in range(len(c)):
	slidebar.append(st.sidebar.image(c[i], caption=str(cloths[i]), width=100, use_column_width=False))
#st.sidebar.image(cloth1, caption="001616", width=100, use_column_width=False)
#st.sidebar.image(cloth2, caption="001517", width=100, use_column_width=False)
#st.sidebar.image(cloth3, caption="001500", width=100, use_column_width=False)
#st.sidebar.image(cloth4, caption="000009", width=100, use_column_width=False)
#st.sidebar.image(cloth5, caption="000068", width=100, use_column_width=False)
#st.sidebar.image(cloth6, caption="000108", width=100, use_column_width=False)


uploaded_person = st.file_uploader("Upload a Photo", type="jpg")
user_input = st.text_input("Enter the User Name without space")
selected = st.selectbox('Select the Item Id:', [
                        '','000003','000011','000013','000108','000254','000308','000627','001247','001401','000649','001500','001719','002061','002337','002385','002599','003086','005632','006158','006159'], format_func=lambda x: 'Select an option' if x == '' else x)


if uploaded_person is not None and user_input is not '' and selected is not '':
    person = Image.open(uploaded_person)
    st.image(person, caption=user_input, width=100, use_column_width=False)
    st.write("Saving Image")
    bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.09)
        bar.progress(percent_complete + 1)
    person.save("./Database/val/person/"+user_input+".jpg")
    progress_bar = st.progress(0)
    st.write("Generating Mask and Pose Pairs")
    pose_parse(user_input)
    execute()
    for percent_complete in range(100):
        time.sleep(0.05)
        progress_bar.progress(percent_complete + 1)
    st.write("Please click the Click Button after Pose pairs and Masks are generated")

if st.button('Execute'):
    f = open("./Database/val_pairs.txt" , "w")    
    f.write(user_input+".jpg "+selected+"_1.jpg")
    f.close()
    predict()
    from PIL import Image
    im = Image.open("./output/second/TOM/val/" + selected + "_1.jpg")
    width, height = im.size  
  
# # Setting the points for cropped image  
    left = width / 3
    top = 2 * height / 3
    right = 2 * width / 3
    bottom = height
  
# # Cropped image of above dimension  
# # (It will not change orginal image)  
    im1 = im.crop((left, top, right, bottom)) 
    newsize = (100, 150) 
    im1 = im1.resize(newsize) 
# # Shows the image in image viewer  
    im1.save("./output/second/TOM/val/" + selected + "_1.jpg")
    execute_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.08)
        execute_bar.progress(percent_complete + 1)
    result = Image.open("./output/second/TOM/val/" + selected + "_1.jpg")
    st.image(result , caption="Result" , width=200 , use_column_width=False)

## Super Reolution


