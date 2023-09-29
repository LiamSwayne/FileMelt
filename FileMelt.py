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

# Process script tags
def processScriptTags(match):
    script_content = match.group(1)
    if re.search(r'type\s*=\s*["\']?module["\']?', match.group(0), re.IGNORECASE):
        # If the <script> tag has type="module", keep it
        return "<script type=\"module\">" + jsmin(script_content) + "</script>"
    else:
        # If the <script> tag doesn't have type="module", remove the type attribute
        return '<script>' + jsmin(script_content) + '</script>'

# Delete console log statements
def removeConsoleLogStatements(html_string):
    # Regular expression pattern to match script tags
    script_pattern = r'<script\b([^>]*)>([\s\S]*?)<\/script>'
    
    def repl(match):
        # Extract attributes and script content
        attributes = match.group(1)
        script_content = match.group(2)
        
        # Remove console.log statements from script content
        script_content = re.sub(r'console\.log\s*\([^)]*\);?', '', script_content)
        
        # Reconstruct the script tag with attributes (if any)
        if attributes:
            if "type=module" in attributes:
                attributes.replace("type=module","type=\"module\"")
            attributes = attributes.lstrip()
            return f'<script {attributes}>{script_content}</script>'
        else:
            return f'<script>{script_content}</script>'
    
    # Use re.sub to replace and modify script tags
    return re.sub(script_pattern, repl, html_string)

# Minify html files
def minifyHtml(inputFile, outputFile):
    with open(inputFile, "r") as inFile, open(outputFile, "w") as outFile:
        htmlContent = inFile.read()

        # Substitute type="module" with placeholders
        type_module_pattern = re.compile(r'type\s*=\s*(?:"module"|\'module\')')
        type_module_placeholders = []
        htmlContent, _ = re.subn(type_module_pattern, lambda x: type_module_placeholders.append(x.group()) or r'__FILEMELT_TYPE_MODULE_PLACEHOLDER__', htmlContent)

        # Replace all strings with placeholders
        placeholders = []
        stringPattern = r'"(?:\\.|[^"\\])*"'
        multilineStringPattern = r'`[^`]*`'
        htmlContent = re.sub(stringPattern, lambda x: placeholders.append(x.group()) or f"__FILEMELT_STRING_PLACEHOLDER_{len(placeholders) - 1}__", htmlContent)
        htmlContent = re.sub(multilineStringPattern, lambda x: placeholders.append(x.group()) or f"__FILEMELT_MULTILINE_STRING_PLACEHOLDER_{len(placeholders) - 1}__", htmlContent)

        # Resubstitute type="module"
        htmlContent = re.sub(r'__FILEMELT_TYPE_MODULE_PLACEHOLDER__', lambda x: type_module_placeholders.pop(0), htmlContent)

        # Process scripts
        htmlContent = re.sub(r'<script[^>]*>([\s\S]*?)<\/script>', processScriptTags, htmlContent)

        # Minify style tag
        htmlContent = minifyStyleTag(htmlContent)

        # Remove HTML comments
        if removeHtmlComments:
            htmlContent = re.sub(r'<!--(.*?)-->', '', htmlContent)

        # Minify HTML content (changes type="module" to type=module)
        htmlContent = minify(htmlContent, remove_empty_space=True)

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