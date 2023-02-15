import cv2
import pytesseract
import numpy as np
import re

# Load the image
image = cv2.imread('img1.jpg') # works for both jpg and png

def cleanText(origin_text):
    text = re.sub("[,/\^$*\"※~&』\\‘|\(\)\[\]\\`\'…》»]", '', origin_text)
    return text

# Apply OCR to extract the text from the image
text = pytesseract.image_to_string(image)
text = cleanText(text)

# Split the extracted text into sentences
sentences = text.split('\n')
while("" in sentences):
    sentences.remove("")  # empty string
print("sentences ", sentences)

# Initialize a variable to keep track of the sentence with the largest font size
largest_font_sentence = None
largest_font_size = 0

# Use pytesseract to get the bounding boxes of each character in the sentence
boxes = pytesseract.image_to_boxes(image, lang='eng')
box_arrays = []
for box in boxes.splitlines():
    box_arrays.append(box.split(' '))

# Loop through each sentence to measure its font size
for sentence in sentences:
    heights = []
    print("sentence: " , sentence)
    temp_sentence = sentence.replace(" ", "")  # remove whitespace in the middle of the sentence
    print("sentence length: " , len(temp_sentence))  # debug
    for box in box_arrays[:len(temp_sentence)]:
        print("box:", box)  # debug
        heights.append(int(box[4]) - int(box[2]))    # get the height of each character from bounding box ( y2-y1 )
    box_arrays = box_arrays[len(temp_sentence):]   # remove the boxes that have chars in this sentence 

    # Calculate the average height of the characters
    avg_height = round(np.mean(heights),2)
    print(f"the average font height is {avg_height} for sentence: '{sentence}' \n")

    # Update the sentence with the largest font size if necessary
    if avg_height > largest_font_size:
        largest_font_sentence = sentence
        largest_font_size = avg_height

# The sentence with the largest font size has been found
print(f"The sentence '{largest_font_sentence}' has the largest font size which is {largest_font_size}")


# try setting threshold of ocr confidence so the MS Teams UI OCRed results 
# won't be considered
