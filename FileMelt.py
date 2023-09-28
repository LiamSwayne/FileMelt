import os
import shutil
import re
from htmlmin import minify
from jsmin import jsmin
from csscompressor import compress

# SETTINGS
inputFolder = "source"
outputFolder = "docs"
removeHtmlComments = True  # Remove HTML comments
removeConsoleLog = True  # Remove console log statements.

# Methods

def minifyHtml(inputFile, outputFile):
    with open(inputFile, "r") as inFile, open(outputFile, "w") as outFile:
        htmlContent = inFile.read()

        # Replace all strings with placeholders
        placeholders = []
        stringPattern = r'"(?:\\.|[^"\\])*"'
        multilineStringPattern = r'`[^`]*`'
        htmlContent = re.sub(stringPattern, lambda x: placeholders.append(x.group()) or f"__FILEMELT_STRING_PLACEHOLDER_{len(placeholders) - 1}__", htmlContent)
        htmlContent = re.sub(multilineStringPattern, lambda x: placeholders.append(x.group()) or f"__FILEMELT_MULTILINE_STRING_PLACEHOLDER_{len(placeholders) - 1}__", htmlContent)

        # Minify style tag
        htmlContent = minifyStyleTag(htmlContent)

        # Remove HTML comments
        if removeHtmlComments:
            htmlContent = re.sub(r'<!--(.*?)-->', '', htmlContent)

        # Minify HTML content
        minifiedHtml = minify(htmlContent, remove_empty_space=True)

        # Minify JavaScript within <script> tags
        minifiedHtml = re.sub(r'<script[^>]*>([\s\S]*?)<\/script>', lambda x: '<script>' + jsmin(x.group(1)) + '</script>', minifiedHtml)

        # Restore the original strings
        for index, placeholder in enumerate(placeholders):
            minifiedHtml = minifiedHtml.replace(f"__FILEMELT_STRING_PLACEHOLDER_{index}__", placeholder)
            minifiedHtml = minifiedHtml.replace(f"__FILEMELT_MULTILINE_STRING_PLACEHOLDER_{index}__", placeholder)

        outFile.write(minifiedHtml)

def minifyStyleTag(htmlString):
    # Define a regular expression pattern to match <style> tags and their content
    styleTagPattern = r'<style[^>]*>(.*?)</style>'

    # Function to minify the content of a <style> tag
    def minifyCss(match):
        cssCode = match.group(1)
        minifiedCss = compress(cssCode)
        return f'<style>{minifiedCss}</style>'

    # Use re.sub() to find and replace <style> tags with minified content
    minifiedHtml = re.sub(styleTagPattern, minifyCss, htmlString, flags=re.DOTALL)

    return minifiedHtml

# Main program

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
print("Size decrease: " + str(round(percentDecrease * 100, 4)) + "%")