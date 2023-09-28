import os
import shutil
import re
from htmlmin import minify as html_minify
from jsmin import jsmin

### SETTINGS
inputFolder = "source"
outputFolder = "docs"

### Methods

def minifyHtml(inputFile, outputFile):
    with open(inputFile, "r") as infile, open(outputFile, "w") as outfile:
        htmlContent = infile.read()

        # Remove HTML comments
        htmlContent = re.sub(r'<!--(.*?)-->', '', htmlContent)

        # Minify HTML content
        minifiedHtml = html_minify(htmlContent, remove_empty_space=True)

        # Minify JavaScript within <script> tags
        minifiedHtml = re.sub(r'<script[^>]*>([\s\S]*?)<\/script>', lambda x: '<script>' + jsmin(x.group(1)) + '</script>', minifiedHtml)

        outfile.write(minifiedHtml)

### Main program

# Create the output directory if it doesn't exist
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)

totalInputBytes = 0
totalOutputBytes = 0

for root, _, files in os.walk(inputFolder):
    for filename in files:
        inputFile = os.path.join(root, filename)
        outputFile = os.path.join(outputFolder, filename)

        if filename.endswith(".html"):
            minifyHtml(inputFile, outputFile)
        else:
            # Copy non-HTML files to the output folder
            shutil.copy(inputFile, outputFile)

        # Calculate total bytes
        totalInputBytes += os.path.getsize(inputFile)
        totalOutputBytes += os.path.getsize(outputFile)

print("Total bytes in input folder: " + str(totalInputBytes) + " bytes")
print("Total bytes in output folder: " + str(totalOutputBytes) + " bytes")
percentDecrease = 1 - (totalOutputBytes / float(totalInputBytes))
print("Percent decrease: " + str(round(percentDecrease * 100, 4)) + "%")