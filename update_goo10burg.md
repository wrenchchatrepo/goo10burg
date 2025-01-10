# Update

## Instructions

- This application generates either a script (python, sql, unix shell, lookml, etc.) or a markdown file (README or technical article) subject to parameters contained in a YAML config file; if one of the parameters requires a diagram, the app uses the eraser.io API to generate the diagram.

- Every file gets a pk, unique and non-null, a string of 5 lowercase alphanumeric chars.

- All prose is written in active voice, present tense, avoid business jargon and suprfluous language; economy of words is preferred. 

- Every article is on topic that serves a purpose, built with assertions, and supported by evidence. 

- When writing a script or markdown document based on an existing file sanitize any details with obvious dummy names  and any parameter values with standard placeholder names.

- Every script generated includes comments in the file describing how the script works and the purpose it serves and 1 to 5 labels; every markdown file is assigned 1 to 5 labels.

- If scripts or markdown documents have a tagline required (a one sentence high level summary) the tagline is included as a comment at the top of the script or the document.

## Fields

These are the fields by YAML config file:
### script:
- pk
- type
- language
- new_filename
- existing_filename
- update_date
- version
- description
- author
- objective
- input
- process
- output
- number_of_diagrams
- diagram_prompt_1
- tagline_required
- old_filepath
- new_filepath
- labels
- diagram_1_pk
- zipfile
### markdown:
- pk
- type
- new_filename
- existing_filename
- update_date
- version
- description
- author
- number_assertions
- assertion_1_sentence
- assertion_2_sentence
- paragraph_per_assertions
- intro_paragraph
- concluding_paragraph
- approx_words_per_paragraphs
- total_paragraphs
- approx_total_words
- number_of_diagrams
- diagram_prompt_#
- diagram_1_pk
- tagline_required
- old_filepath
- new_filepath
- labels
- zipfile
### image:
- pk
- new_filename
- new_filepath
### package:
- pk
- package

## Reference Files
- `labels` can be found here: /Users/dionedge/dev/goo10burg/src/templates/labels.yaml
- `pk` can be found here and are marked `used` when assigned to a file: /Users/dionedge/dev/goo10burg/src/templates/pk.yaml
- A data dictionary for the fields can be found here: /Users/dionedge/dev/goo10burg/src/templates/guide.yaml

## Images
- All image files will be saved here: /Users/dionedge/dev/goo10burg/finished_files/images
- If an image file is the only digram required (number_of_diagrams=1) then the filename of the diagram is equal to new_filename but with the extion `.png` otherwise the filename of the image is new_filename_#.

## Tests

### CSVs
- Here are four csv files to convert to 9 yaml files, 2 markdown, 2 script, 4 image, 1 package, which will generate 2 md files, 2 python files, 4 image files, and 1 yaml config file:
	+ /Users/dionedge/dev/goo10burg/tests/image.csv
	+ /Users/dionedge/dev/goo10burg/tests/markdown.csv
	+ /Users/dionedge/dev/goo10burg/tests/package.csv
	+ /Users/dionedge/dev/goo10burg/tests/script.csv

## Please update /Users/dionedge/dev/goo10burg/README.md accordingly.
