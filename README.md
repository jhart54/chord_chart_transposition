# Welcome
Welcome! This GitHub contains instructions for the transposition and quick formatting of chord charts for many purposes. The files included here are:
- a Python script responsible for transposition, formatting ,and outputting of a PDF chord chart based on a desired key for the song and a text file input
- a sample text file input
- a pdf file with the logo of the church that sponsored this project (shoutout to the [Oaks Church](https://fonts.google.com/specimen/Inconsolata?subset=vietnamese) in Cincinnati!)
- two font files used in printing
  - the font used was Inconsolata Semi-Condensed found [here](https://fonts.google.com/specimen/Inconsolata?subset=vietnamese). Spacing may be slightly off if different fonts are used.

# Code structure
The code is split into functions responsible for reading in and processing the text file of chords and lyrics, identifying and transposing chords, and printing a formatted PDF.

# Text input file requirements:
- File must have the .txt extension
- Spaces (not tabs) must be used to separate chord names above the lyrics
- Lines with chords need to have more spaces than text characters (e.g. “G        “ as a complete line as opposed to just “G” for the line) as chords lines and lyrics lines are separated by clustering based on text to space ratio
- Any headings for different parts of the song (e.g. bridge, chorus, intro, etc.) must be typed in brackets (e.g. [Intro], [Chorus 1], etc.)
- The title of the song printed in the PDF will be the first non-empty line of the text file
- Spacing of lines in the text file does not matter
- The current key of the song is specified in the naming conventions of the file (e.g. “One of Us chords - B.txt”, where the key is B major)

# Running the code and folder structure:
Running the code is as simple as changing the current directory to a directory where several sub-folders are stored. The required naming conventions for the sub-folders are:
- txt_input_files: raw text files created with the above conventions to be processed with the code
- pdf_chord_charts: folder for complete PDF chord charts to be saved
- processing_files/fonts: folder/sub-folder to store fonts used in printing

Lastly, I want to credit Manohar Vanga with several of the musical processing functions I borrowed from the excellent tutorial found here (hyperlink). 
Feel free to reach out with any questions or improvements if you end up using any of this code!
