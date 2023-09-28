import os
import shutil
import re

# SETTINGS
inputFolder = "source"
outputFolder = "docs"

def minifyHtml(inputPath, outputPath):
    # Create the output directory if it doesn't exist
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)

    totalInputBytes = 0
    totalOutputBytes = 0

    for root, _, files in os.walk(inputPath):
        for filename in files:
            inputFile = os.path.join(root, filename)
            outputFile = os.path.join(outputPath, filename)

            if filename.endswith(".html"):
                with open(inputFile, "r") as infile, open(outputFile, "w") as outfile:
                    htmlContent = infile.read()
                    cleanedHtml = removeHtmlComments(htmlContent)
                    outfile.write(cleanedHtml)
            else:
                # Copy non-HTML files to the output folder
                shutil.copy(inputFile, outputFile)

            # Calculate total bytes
            totalInputBytes += os.path.getsize(inputFile)
            totalOutputBytes += os.path.getsize(outputFile)

    return totalInputBytes, totalOutputBytes

def removeHtmlComments(html):
    result = ""
    insideComment = False
    i = 0

    # Replace all strings with placeholders
    placeholders = []
    string_pattern = r'"(?:\\.|[^"\\])*"'
    multiline_string_pattern = r'`[^`]*`'
    html = re.sub(string_pattern, lambda x: placeholders.append(x.group()) or f"__STRING_PLACEHOLDER_{len(placeholders) - 1}__", html)
    html = re.sub(multiline_string_pattern, lambda x: placeholders.append(x.group()) or f"__MULTILINE_STRING_PLACEHOLDER_{len(placeholders) - 1}__", html)

    while i < len(html):
        if html[i:i+4] == "<!--":
            insideComment = True
            i += 4
            while i < len(html) and html[i:i+3] != "-->":
                i += 1
            if i < len(html):
                i += 3
        else:
            result += html[i]
            i += 1

    # Restore the original strings
    for index, placeholder in enumerate(placeholders):
        result = result.replace(f"__STRING_PLACEHOLDER_{index}__", placeholder)
        result = result.replace(f"__MULTILINE_STRING_PLACEHOLDER_{index}__", placeholder)

    return result

totalInputBytes, totalOutputBytes = minifyHtml(inputFolder, outputFolder)
print("Total bytes in input folder: " + str(totalInputBytes) + " bytes")
print("Total bytes in output folder: " + str(totalOutputBytes) + " bytes")
percentDecrease = 1 - (totalOutputBytes / float(totalInputBytes))
print("Percent decrease: " + str(round(percentDecrease*100, 4)) + "%")
