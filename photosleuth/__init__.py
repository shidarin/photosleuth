import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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