import os
import shutil

# Define input and output folders
input_folder = "source"
output_folder = "docs"

def minify_html(input_path, output_path):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    total_input_bytes = 0
    total_output_bytes = 0

    for root, _, files in os.walk(input_path):
        for filename in files:
            input_file = os.path.join(root, filename)
            output_file = os.path.join(output_path, filename)

            if filename.endswith(".html"):
                with open(input_file, "r") as infile, open(output_file, "w") as outfile:
                    html_content = infile.read()
                    cleaned_html = remove_html_comments(html_content)
                    outfile.write(cleaned_html)
            else:
                # Copy non-HTML files to the output folder
                shutil.copy(input_file, output_file)

            # Calculate total bytes
            total_input_bytes += os.path.getsize(input_file)
            total_output_bytes += os.path.getsize(output_file)

    return total_input_bytes, total_output_bytes

def remove_html_comments(html):
    result = ""
    inside_comment = False
    i = 0
    while i < len(html):
        if html[i:i+4] == "<!--":
            inside_comment = True
            i += 4
        elif html[i:i+3] == "-->":
            inside_comment = False
            i += 3
        elif not inside_comment:
            result += html[i]
            i += 1
        else:
            i += 1
    return result

total_input_bytes, total_output_bytes = minify_html(input_folder, output_folder)
print("Total bytes in input folder: " + str(total_input_bytes) + " bytes")
print("Total bytes in output folder: " + str(total_output_bytes) + " bytes")
percent_decrease = 1 - (total_output_bytes / float(total_input_bytes))
print("Percent decrease: " + str(round(percent_decrease*100,4)) + "%")