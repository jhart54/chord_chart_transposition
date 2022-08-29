# Background
Welcome! This GitHub contains instructions for the transposition and quick formatting of chord charts for many purposes. The goal of this project was to design a system that could output chord charts in a concise, clean PDF format as well as automatically transpose chord charts into different keys based on user input. The final product was a Python script that takes a named .txt file with chords and lyrics in a song, as well as the desired key for the song, and outputs the formatted song to a PDF in the desired key.

# Files included
- python scripts: 
    - create_one_song: script for transposing, formatting, and outputting a PDF chord chart based on a desired key for one song and a text file input
    - build_chord_chart_function: script that just contains the function that builds the chord chart for a song based on an import path and a desired key
    - create_all_songs: script that runs through each text input file and uses the build chord chart function to create chord charts for each song in all possible keys
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

Lastly, I want to credit Manohar Vanga with several of the musical processing functions I borrowed from the excellent tutorial found [here](https://www.mvanga.com/blog/basic-music-theory-in-200-lines-of-python). 
Feel free to reach out with any questions or improvements if you end up using any of this code!
