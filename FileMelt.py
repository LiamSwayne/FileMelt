import os
import shutil

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
    while i < len(html):
        if html[i:i+4] == "<!--":
            insideComment = True
            i += 4
        elif html[i:i+3] == "-->":
            insideComment = False
            i += 3
        elif not insideComment:
            result += html[i]
            i += 1
        else:
            i += 1
    return result

totalInputBytes, totalOutputBytes = minifyHtml(inputFolder, outputFolder)
print("Total bytes in input folder: " + str(totalInputBytes) + " bytes")
print("Total bytes in output folder: " + str(totalOutputBytes) + " bytes")
percentDecrease = 1 - (totalOutputBytes / float(totalInputBytes))
print("Percent decrease: " + str(round(percentDecrease*100, 4)) + "%")
