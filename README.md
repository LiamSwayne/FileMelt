# FileMelt
An everything minifier for websites.

Write clean code while minimizing bandwidth costs.

| Pros | Cons |
| ------------- | ------------- |
| Saves significant bandwidth | Increases git repo size quickly |
| Makes your site load faster | JS minifier is imperfect (but can be disabled) |

Roadmap:
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
- [ ] 
- [ ] Replace dependencies with built-in functions.
    - [ ] htmlmin
    - [ ] jsmin
    - [ ] csscompressor
