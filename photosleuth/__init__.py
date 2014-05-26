#!/usr/bin/env python
"""

PhotoSleuth
===========

Uses Google with Selenium controlled browsers to perform reverse image search
and allow users to page through results.

## License

Original is by /u/touste
http://www.reddit.com/r/ScriptSwap/comments/26bdm8/python_reversesearch_each_image_of_a_website/
http://www.reddit.com/r/photography/comments/26j0oe/for_the_programming_photographers_python_script/

The MIT License (MIT)

Copyright (c) 2014 /u/touste & Sean Wallitsch

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

# =============================================================================
# IMPORTS
# =============================================================================

import time
from selenium import webdriver
from Tkinter import *

#Webpage to parse
page="http://touste.tumblr.com"

#First browser to open and parse webpage
browser = webdriver.Chrome()#may be changed to use Firefox
browser.get(page)
time.sleep(1)


#Scroll until all the images have been found (useful for infinte scroll pages)
prev_numb = 0
post_elems = browser.find_elements_by_tag_name("img")

while len(post_elems)>prev_numb:
    prev_numb=len(post_elems)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.5)
    post_elems = browser.find_elements_by_tag_name("img")

#Second browser to reverse search the images
browser2 = webdriver.Chrome()#may be changed to use Firefox

#Window that captures keypress and display image counter
root = Tk()
prompt = StringVar()
prompt.set("Press Enter to go to next image (image 0 of " + str(len(post_elems)+1) + ")")
label1 = Label(root, textvariable=prompt, width=50,bg="yellow")

#Reverse search each image and update the window
k=0
def gotonext(event):
    global k
    global post_elems
    prompt.set("Press Enter to go to next image (image " + str(k+1) +" of " + str(len(post_elems)+1) + ")")
    root.update_idletasks()
    if k<len(post_elems):
        post = post_elems[k]
        k=k+1
        url = "http://images.google.com/searchbyimage?site=search&image_url=" + post.get_attribute("src")
        browser2.get(url)

#Execute previous function each time Enter is pressed
label1.bind('<Return>', gotonext)
label1.focus_set()
label1.pack()
root.mainloop()