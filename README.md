# `FileMelt 📁🔥`
**An everything minifier for websites implemented in Python.**

| Pros | Cons |
| ------------- | ------------- |
| Write clean code without paying for extra bandwidth | Output folder increases git repo size quickly (but can be added to .gitignore) |
| Minifies HTML, CSS, JS, SVG | JS minifier is imperfect (but can be disabled) |
| Decreases load speeds | |

## How it works
The only file you need is [FileMelt.py](https://github.com/LiamSwayne/FileMelt/blob/main/FileMelt.py). Add it to your repository, and assign the input and output directories at the top of the file (and optionally modify the settings also in the file). Each time you run `FileMelt.py`, it will generate a minfied output directory of all files in the input directory, including files that FileMelt cannot minify (yet). Work in your input directory and host in your output directory to minimize bandwidth costs with zero impact on development.

## Contributing
This repo is active! All PRs will be reviewed ASAP. All the code is in `FileMelt.py` (this project is 100% Python). The `source` and `docs` folders are full of input/output test cases. Implement a roadmap feature, minify a new file type, or make any general improvement.

## Roadmap:
- [x] Basic HTML minification.
- [x] CSS minification.
- [x] Remove html comments.
- [x] Minify style tag.
    - [x] Remove type="text/css".
    - [x] Remove spaces and newlines.
- [ ] Minify hexcodes in style attributes.
- [x] Setting for removing console.log statements
- [ ] Basic svg minification.
    - [x] Remove comments.
    - [x] Simplify style tags.
    - [ ] Classes only used once are substituted for style attribute.
- [ ] Minify svgs in html files.
- [x] Remove empty scripts.
- [ ] Merge scripts when possible.
- [x] Minify JavaScript files.
- [x] Option to delete files in output with matching input.
- [x] Preserve module attribute in script tags.
- [x] Option to print individual file stats.
- [ ] Avoid deleting copyright or license comments.
- [ ] Replace dependencies with built-in functions.
    - [ ] htmlmin
    - [ ] jsmin
    - [ ] csscompressor
