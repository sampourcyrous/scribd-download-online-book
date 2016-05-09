# Script that Downloads Books Online

Scribd is a digital documents library that gives people an abundant resource of books. Unfortunately it is a subscription based website that requires users to pay in order to access their services. I wanted a personal copy of a book that Scribd offered without paying a subscription, so I wrote a script in Python to download the online book.

Scribd does offer various books online for free, however there are limitations to viewing them. The main limitation for a user is they are not allowed to download a local copy of the online textbook. The goal was to tackle that issue with this script. The script only works if each page of the online book is an image.

# How the script works
First the user must save the source code of the webpage that hosts thier desired book. (e.g. https://www.scribd.com/doc/103237194/Mandelbrot-Benoit-La-geometria-fractal-de-la-naturaleza)

The user would then run the script which does the following:
  - The script searches through the source code using regular expressions to extract the source of where the page (image) is loaded from
  - The pages (images) are then downloaded and stored in a local folder
  - A seperate script can then combine the downloaded images to form a pdf

This script works with Python 2.7

Scribd might have updated their source code since the script was first created

Last time script was tested: May 2016
