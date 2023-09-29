# FileMelt
An everything minifier for websites.

Write clean code while minimizing bandwidth costs.

Roadmap:
- [x] Basic HTML minification.
- [x] Remove html comments.
- [x] Minify style tag.
    - [x] Remove type="text/css".
    - [x] Remove spaces and newlines.
- [ ] Minify hexcodes in style attributes.
- [x] Setting for removing console.log statements
- [ ] Basic svg minification.
    - [x] Remove comments.
    - [ ] Classes only used once are changed to style="".
- [ ] Remove unecessary script tags.
    - [x] Remove empty scripts.
    - [ ] Merge scripts when possible.
- [x] Option to print individual file stats.
- [ ] Replace dependencies with built-in functions.
    - [ ] htmlmin
    - [ ] jsmin
    - [ ] csscompressor