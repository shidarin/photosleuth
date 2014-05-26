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

# Python 3 Compatibility
from __future__ import print_function

# Standard Imports
from selenium import webdriver
from sys import argv
import time
from Tkinter import *

if sys.version_info[0] >= 3:
    raw_input = input

# =============================================================================
# GLOBALS
# =============================================================================

REVERSE_URL = "http://images.google.com/searchbyimage?site=search&image_url="

TEST_PAGE = "http://touste.tumblr.com"

# =============================================================================
# FUNCTIONS
# =============================================================================


def _parse_images(browser):
    """Parses and returns all found images on a webpage"""

    # Scroll until all the images have been found, which is
    # useful for infinite scroll pages
    prev_elems = 0
    post_elems = browser.find_elements_by_tag_name("img")

    while len(post_elems) > prev_elems:
        prev_elems = len(post_elems)
        browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        time.sleep(0.5)
        post_elems = browser.find_elements_by_tag_name("img")

    images = [elem.getattribute('src') for elem in post_elems]
    images = list(set(images))
    images.sort()

    return images

# =============================================================================
# MAIN
# =============================================================================


def main():
    """Main script"""
    try:
        homepage = argv[1]
    except IndexError:
        raise ValueError(
            "Please pass a website when calling the script on the "
            "command line."
        )

    # We'll set the default to Firefox. Other browsers may be used but
    # additional software may have to be downloaded.
    parser = webdriver.Firefox()

    # Send parser to our homepage, wait 1 to ensure scripts finish.
    parser.get(homepage)
    time.sleep(1)

    # Get all the images on the page.
    images = _parse_images(parser)

    searcher = webdriver.Firefox()

    for img in images:
        print(
            "Now reverse searching '{img_url}'\n"
            "{index} of {length}".format(
                img_url=img,
                index=images.index(img),
                length=len(images)
            )
        )
        searcher.get(REVERSE_URL + img)
        raw_input("Results displayed. Press enter to continue")

    print("{total} images searched.".format(total=len(images)))

# =============================================================================
# RUNNER
# =============================================================================

if __name__ == '__main__':
    main()