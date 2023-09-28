import os
import shutil
import re
from htmlmin import minify as html_minify
from jsmin import jsmin
from csscompressor import compress

### SETTINGS
inputFolder = "source"
outputFolder = "docs"

### Methods

def minifyHtml(inputFile, outputFile):
    with open(inputFile, "r") as infile, open(outputFile, "w") as outfile:
        htmlContent = infile.read()

        # Replace all strings with placeholders
        placeholders = []
        string_pattern = r'"(?:\\.|[^"\\])*"'
        multiline_string_pattern = r'`[^`]*`'
        htmlContent = re.sub(string_pattern, lambda x: placeholders.append(x.group()) or f"__STRING_PLACEHOLDER_{len(placeholders) - 1}__", htmlContent)
        htmlContent = re.sub(multiline_string_pattern, lambda x: placeholders.append(x.group()) or f"__MULTILINE_STRING_PLACEHOLDER_{len(placeholders) - 1}__", htmlContent)

        # Remove type="text/css" from style tag
        # TODO

        # Minify style tag
        htmlContent = minify_style_tag(htmlContent)


        # Remove HTML comments
        htmlContent = re.sub(r'<!--(.*?)-->', '', htmlContent)

        # Minify HTML content
        minifiedHtml = html_minify(htmlContent, remove_empty_space=True)

        # Minify JavaScript within <script> tags
        minifiedHtml = re.sub(r'<script[^>]*>([\s\S]*?)<\/script>', lambda x: '<script>' + jsmin(x.group(1)) + '</script>', minifiedHtml)

        # Restore the original strings
        for index, placeholder in enumerate(placeholders):
            minifiedHtml = minifiedHtml.replace(f"__STRING_PLACEHOLDER_{index}__", placeholder)
            minifiedHtml = minifiedHtml.replace(f"__MULTILINE_STRING_PLACEHOLDER_{index}__", placeholder)

        outfile.write(minifiedHtml)

def minify_style_tag(html_string):
    # Define a regular expression pattern to match <style> tags and their content
    style_tag_pattern = r'<style[^>]*>(.*?)</style>'
    
    # Function to minify the content of a <style> tag
    def minify_css(match):
        css_code = match.group(1)
        minified_css = compress(css_code)
        return f'<style>{minified_css}</style>'
    
    # Use re.sub() to find and replace <style> tags with minified content
    minified_html = re.sub(style_tag_pattern, minify_css, html_string, flags=re.DOTALL)
    
    return minified_html

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