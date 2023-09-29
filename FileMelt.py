# Imports
import os
import shutil
import re
from htmlmin import minify
from jsmin import jsmin
from csscompressor import compress

### SETTINGS
inputFolder = "source"
outputFolder = "docs"
deleteFilesMissingInput = True  # Delete files in output folder without corresponding input files
printFileStatistics = True      # Print the size decrease of each individual file.
removeHtmlComments = True       # Remove HTML comments
removeSvgComments = True        # Remove svg comments
minifyJsFiles = True            # Minify JS files (imperfect in some cases)
removeConsoleLog = True         # Remove JavaScript console log statements.

### Methods

# Helper function to minify the content of a <style> tag
def minifyCss(match):
    cssCode = match.group(1)
    minifiedCss = compress(cssCode)
    return f'<style>{minifiedCss}</style>'

# Shrink the style tag
def minifyStyleTag(htmlString):
    # Define a regular expression pattern to match <style> tags and their content
    styleTagPattern = r'<style[^>]*>(.*?)</style>'

    # Use re.sub() to find and replace <style> tags with minified content
    return re.sub(styleTagPattern, minifyCss, htmlString, flags=re.DOTALL)

# Delete console log statements
def removeConsoleLogStatements(html_string):
    # Regular expression pattern to match console.log statements
    pattern = r'<script\b[^>]*>([\s\S]*?)<\/script>'
    
    def repl(match):
        # Replace console.log statements with an empty string
        script_content = match.group(1)
        script_content = re.sub(r'console\.log\s*\([^)]*\);?', '', script_content)
        return f'<script>{script_content}</script>'
    
    # Use re.sub to replace console.log statements    
    return re.sub(pattern, repl, html_string)

# Minify html files
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
        htmlContent = minify(htmlContent, remove_empty_space=True)

        # Minify JavaScript within <script> tags
        if minifyJsFiles:
            htmlContent = re.sub(r'<script[^>]*>([\s\S]*?)<\/script>', lambda x: '<script>' + jsmin(x.group(1)) + '</script>', htmlContent)

        # Delete JavaScript console log statements
        htmlContent = removeConsoleLogStatements(htmlContent)

        # Remove empty scripts
        htmlContent = re.sub(r'<script[^>]*>\s*</script>', '', htmlContent)

        # Restore the original strings
        for index, placeholder in enumerate(placeholders):
            htmlContent = htmlContent.replace(f"__FILEMELT_STRING_PLACEHOLDER_{index}__", placeholder)
            htmlContent = htmlContent.replace(f"__FILEMELT_MULTILINE_STRING_PLACEHOLDER_{index}__", placeholder)

        outFile.write(htmlContent)

# Minify svg files
def minifySvg(inputFile, outputFile):
    with open(inputFile, "r") as inFile, open(outputFile, "w") as outFile:
        svgContent = inFile.read()

        # Replace all strings with placeholders
        placeholders = []
        stringPattern = r'"(?:\\.|[^"\\])*"'
        multilineStringPattern = r'`[^`]*`'
        svgContent = re.sub(stringPattern, lambda x: placeholders.append(x.group()) or f"__FILEMELT_STRING_PLACEHOLDER_{len(placeholders) - 1}__", svgContent)
        svgContent = re.sub(multilineStringPattern, lambda x: placeholders.append(x.group()) or f"__FILEMELT_MULTILINE_STRING_PLACEHOLDER_{len(placeholders) - 1}__", svgContent)

        # Remove svg comments
        if removeSvgComments:
            svgContent = re.sub(r'<!--(.*?)-->', '', svgContent)

        # Restore the original strings
        for index, placeholder in enumerate(placeholders):
            svgContent = svgContent.replace(f"__FILEMELT_STRING_PLACEHOLDER_{index}__", placeholder)
            svgContent = svgContent.replace(f"__FILEMELT_MULTILINE_STRING_PLACEHOLDER_{index}__", placeholder)

        outFile.write(svgContent)

# Minify js files
def minifyJs(inputFile, outputFile):
    with open(inputFile, "r") as inFile, open(outputFile, "w") as outFile:
        jsContent = inFile.read()

        # Replace all strings with placeholders
        placeholders = []
        stringPattern = r'"(?:\\.|[^"\\])*"'
        multilineStringPattern = r'`[^`]*`'
        jsContent = re.sub(stringPattern, lambda x: placeholders.append(x.group()) or f"__FILEMELT_STRING_PLACEHOLDER_{len(placeholders) - 1}__", jsContent)
        jsContent = re.sub(multilineStringPattern, lambda x: placeholders.append(x.group()) or f"__FILEMELT_MULTILINE_STRING_PLACEHOLDER_{len(placeholders) - 1}__", jsContent)

        # Remove html format comments in JavaScript
        jsContent = re.sub(r'<!--(.*?)-->', '', jsContent)

        # Minify JavaScript
        jsContent = jsmin(jsContent)

        # Restore the original strings
        for index, placeholder in enumerate(placeholders):
            jsContent = jsContent.replace(f"__FILEMELT_STRING_PLACEHOLDER_{index}__", placeholder)
            jsContent = jsContent.replace(f"__FILEMELT_MULTILINE_STRING_PLACEHOLDER_{index}__", placeholder)

        outFile.write(jsContent)

# Print statistics of given file
def getFileStats(inputFilename, inputSize, outputSize):
    print(inputFilename)
    print(str(inputSize) + " --> "+ str(outputSize) + " bytes")
    percentDecrease = 1 - (outputSize / float(inputSize))
    print("Size decrease: " + str(round(percentDecrease * 100, 4)) + "%\n")

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
        elif filename.endswith(".svg"):
            minifySvg(inputFile, outputFile)
        elif filename.endswith(".js") and minifyJsFiles:
            minifyJs(inputFile, outputFile)
        else:
            # Copy non-HTML files to the output folder
            shutil.copy(inputFile, outputFile)
            fileSize = os.path.getsize(inputFile)
            totalInputBytes += fileSize
            totalOutputBytes += fileSize
            if printFileStatistics:
                getFileStats(filename, fileSize, fileSize)
            continue

        # Calculate total bytes
        inputSize = os.path.getsize(inputFile)
        outputSize = os.path.getsize(outputFile)
        totalInputBytes += inputSize
        totalOutputBytes += outputSize
        if printFileStatistics:
            getFileStats(filename, inputSize, outputSize)

print("Total bytes in input folder: " + str(totalInputBytes) + " bytes")
print("Total bytes in output folder: " + str(totalOutputBytes) + " bytes")
percentDecrease = 1 - (totalOutputBytes / float(totalInputBytes))
print("Total size decrease: " + str(round(percentDecrease * 100, 4)) + "%")