# Transforming Key Signatures

# This file inputs and processes a text file with lyrics and chords
# in correct positions and outputs a formatted PDF of the song in
# the desired key.

# Inputs: song.txt, current_key, desired_key




# Importing Libraries
import re
import os
import pandas as pd
import numpy as np
import PyPDF2
from sklearn.cluster import KMeans
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# changing current directory
master_path = '/Users/Jonathan/Desktop/oaks_music'
os.chdir(master_path)



################################################################################

# Importing previous work with copyright - for music scales processing

# MIT License
#
# Copyright (c) 2021 Manohar Vanga
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


# The musical alphabet consists of seven letter from A through G
alphabet = ['C', 'D', 'E', 'F', 'G', 'A', 'B']

# The twelve notes in Western music, along with their enharmonic equivalents
notes = [
    ['B#',  'C',  'Dbb'],
    ['B##', 'C#', 'Db'],
    ['C##', 'D',  'Ebb'],
    ['D#',  'Eb', 'Fbb'],
    ['D##', 'E',  'Fb'],
    ['E#',  'F',  'Gbb'],
    ['E##', 'F#', 'Gb'],
    ['F##', 'G',  'Abb'],
    ['G#',  'Ab'],
    ['G##', 'A',  'Bbb'],
    ['A#',  'Bb', 'Cbb'],
    ['A##', 'B',  'Cb'],
]


def find_note_index(scale, search_note):
    ''' Given a scale, find the index of a particular note '''
    for i, note in enumerate(scale):
        # Deal with situations where we have a list of enharmonic
        # equivalents, as well as just a single note as and str.
        if type(note) == list:
            if search_note in note:
                return i
        elif type(note) == str:
            if search_note == note:
                return i


def rotate(scale, n):
    ''' Left-rotate a scale by n positions. '''
    return scale[n:] + scale[:n]


def chromatic(key):
    ''' Generate a chromatic scale in a given key. '''
    # Figure out how much to rotate the notes list by and return
    # the rotated version.
    num_rotations = find_note_index(notes, key)
    return rotate(notes, num_rotations)


# Interval names that specify the distance between two notes
intervals = [
    ['P1', 'd2'],  # Perfect unison   Diminished second
    ['m2', 'A1'],  # Minor second     Augmented unison
    ['M2', 'd3'],  # Major second     Diminished third
    ['m3', 'A2'],  # Minor third      Augmented second
    ['M3', 'd4'],  # Major third      Diminished fourth
    ['P4', 'A3'],  # Perfect fourth   Augmented third
    ['d5', 'A4'],  # Diminished fifth Augmented fourth
    ['P5', 'd6'],  # Perfect fifth    Diminished sixth
    ['m6', 'A5'],  # Minor sixth      Augmented fifth
    ['M6', 'd7'],  # Major sixth      Diminished seventh
    ['m7', 'A6'],  # Minor seventh    Augmented sixth
    ['M7', 'd8'],  # Major seventh    Diminished octave
    ['P8', 'A7'],  # Perfect octave   Augmented seventh
]

# Interval names based off the notes of the major scale
intervals_major = [
    [ '1', 'bb2'],
    ['b2',  '#1'],
    [ '2', 'bb3',   '9'],
    ['b3',  '#2'],
    [ '3',  'b4'],
    [ '4',  '#3',  '11'],
    ['b5',  '#4', '#11'],
    [ '5', 'bb6'],
    ['b6',  '#5'],
    [ '6', 'bb7',  '13'],
    ['b7',  '#6'],
    [ '7',  'b8'],
    [ '8',  '#7'],
]


def find_note_by_root(notes, root):
    '''
    Given a list of notes, find it's alphabet. Useful for figuring out which
    enharmonic equivalent we must use in a particular scale.
    '''
    for note in notes:
        if note[0] == root:
            return note

def make_intervals_major(root):
    labeled = {}
    c = chromatic(root)
    start_index = find_note_index(alphabet, root[0])
    for i, interval in enumerate(intervals_major):
        for interval_name in interval:
            interval_index = int(re.sub('[b#]', '', interval_name)) - 1
            note = c[i % len(c)]
            note_root = alphabet[(start_index + interval_index) % len(alphabet)]
            if note_root is not None:
                labeled[interval_name] = find_note_by_root(note, note_root)
    return labeled


def make_formula(formula, labeled):
    '''
    Given a comma-separated interval formula, and a set of labeled
    notes in a key, return the notes of the formula.
    '''
    return [labeled[x] for x in formula.split(',')]



formulas = {
    # Scale formulas
    'scales': {
        # Basic chromatic scale
        'chromatic':          '1,b2,2,b3,3,4,b5,5,b6,6,b7,7',
        # Major scale, its modes, and minor scale
        'major':              '1,2,3,4,5,6,7',
        'minor':              '1,2,b3,4,5,b6,b7',
        # Melodic minor and its modes
        'melodic_minor':      '1,2,b3,4,5,6,7',
        # Harmonic minor and its modes
        'harmonic_minor':     '1,2,b3,4,5,b6,7',
        # Blues scales
        'major_blues':        '1,2,b3,3,5,6',
        'minor_blues':        '1,b3,4,b5,5,b7',
        # Penatatonic scales
        'pentatonic_major':   '1,2,3,5,6',
        'pentatonic_minor':   '1,b3,4,5,b7',
        'pentatonic_blues':   '1,b3,4,b5,5,b7',
    },
    'chords': {
        # Major
        'major':              '1,3,5',
        'major_6':            '1,3,5,6',
        'major_6_9':          '1,3,5,6,9',
        'major_7':            '1,3,5,7',
        'major_9':            '1,3,5,7,9',
        'major_13':           '1,3,5,7,9,11,13',
        'major_7_#11':        '1,3,5,7,#11',
        # Minor
        'minor':              '1,b3,5',
        'minor_6':            '1,b3,5,6',
        'minor_6_9':          '1,b3,5,6,9',
        'minor_7':            '1,b3,5,b7',
        'minor_9':            '1,b3,5,b7,9',
        'minor_11':           '1,b3,5,b7,9,11',
        'minor_7_b5':         '1,b3,b5,b7',
        # Dominant
        'dominant_7':         '1,3,5,b7',
        'dominant_9':         '1,3,5,b7,9',
        'dominant_11':        '1,3,5,b7,9,11',
        'dominant_13':        '1,3,5,b7,9,11,13',
        'dominant_7_#11':     '1,3,5,b7,#11',
        # Diminished
        'diminished':         '1,b3,b5',
        'diminished_7':       '1,b3,b5,bb7',
        'diminished_7_half':  '1,b3,b5,b7',
        # Augmented
        'augmented':          '1,3,#5',
        # Suspended
        'sus2':               '1,2,5',
        'sus4':               '1,4,5',
        '7sus2':              '1,2,5,b7',
        '7sus4':              '1,4,5,b7',
    },
}

# define sharp and flat variables
flat = '\u266d'
sharp = '\u266f'



def format_scales(scale, separator=' '):
    '''
    Pretty-print the notes of a scale. Replaces b and # characters
    for unicode flat and sharp symbols.
    '''
    return separator.join(['{:<3s}'.format(x) for x in scale]) \
                    .replace('b', flat) \
                    .replace('#', sharp)

##############################################################################


# define a function to read in a song with a given key and parse it out
# into chords/lyrics/headers/title
def read_song(song_title, desired_key):

    # load text file with lyrics and chords
    with open(song_title, encoding='utf-8') as f:
        song = f.readlines()
        f.close()

    # isolate classes in the song

    # create a dataframe to store info about each song
    song_df = pd.DataFrame([line.strip('\n') for line in song if any(line.strip('\n').strip())], columns = ['text'])

    # add line number
    song_df['line_num'] = range(1, len(song_df) + 1)

    # add a space to each line of text for chord integrity in transpositions
    song_df['text'] = song_df['text'] + ' '

    # add characteristic of song
    song_df['class'] = np.where(song_df.index==0, 'title',
                               np.where(song_df['text'].str.contains('\['), 'heading', 'other'))

    # add number of characters that aren't spacing and number of spaces in text
    song_df['nchar'] = [len(re.sub(r"\s+", "", string)) for string in song_df['text']]
    song_df['nspace'] = song_df['text'].str.count(" ")

    # get df to cluster the chords/text into two different groups
    chords_lyrics = song_df[song_df['class']=='other'].reset_index(drop=True)

    # build clusters of lyrics and chords (this worked perfectly the first time so we'll trust it)
    clustering_kmeans = KMeans(n_clusters=2, precompute_distances="auto", n_jobs=-1)
    chords_lyrics['cluster'] = clustering_kmeans.fit_predict(chords_lyrics[['nchar', 'nspace']])

    # join back the cluster information to the original song_df
    song_df1 = pd.merge(song_df, chords_lyrics[['line_num', 'cluster']], how='left', on='line_num')

    # reclassify the "other" values into chords and lyrics based on average text to space ratio
    # average nchar/nspace should always be greater for lyrics than for chords

    # calculate cluster means
    mean_cluster0 = ((chords_lyrics['nchar']/chords_lyrics['nspace'])[chords_lyrics['cluster']==0]).mean()
    mean_cluster1 = ((chords_lyrics['nchar']/chords_lyrics['nspace'])[chords_lyrics['cluster']==1]).mean()

    if mean_cluster0 > mean_cluster1:
        song_df1.loc[song_df1['cluster']==0, 'class'] = 'lyrics'
        song_df1.loc[song_df1['cluster']==1, 'class'] = 'chords'
    else:
        song_df1.loc[song_df1['cluster']==1, 'class'] = 'lyrics'
        song_df1.loc[song_df1['cluster']==0, 'class'] = 'chords'

    # now for the fun part - we need to be able to isolate the chords and change all chord names to a new key
    # split chords on m/maj7/7 for different chords, spaces between chords, and '/' for chords with a different base
    #chord_list = song_df1[song_df1['class']=='chords']['text'].str.strip().str.split(' |/|m|maj7|7')
    #chords_in_song = list({chord for chord_sublist in chord_list for chord in chord_sublist if chord != ''})

    # get the current key of the song
    current_key = current_key = song_title.split(" ")[len(song_title.split(" ")) - 1].split(".")[0]


    # get list of chords that are in the specified major keys
    #dump(make_formula(formulas['scales']['major'], make_intervals_major(current_key))).strip()
    chords_in_current_key = make_formula(formulas['scales']['major'], make_intervals_major(current_key))
    chords_in_desired_key = make_formula(formulas['scales']['major'], make_intervals_major(desired_key))

    # create a dictionary that has keys of current key notes and values of current key roman numerals
    current_key_note_to_roman = {}
    for i, j in enumerate(chords_in_current_key):
        current_key_note_to_roman[j] = i+1

    # create a dictionary that has keys of roman numerals for the desired key and values of chord names in desired key
    desired_key_roman_to_note = {}
    for i, j in enumerate(chords_in_desired_key):
        desired_key_roman_to_note[i+1] = j

    # use those dictionaries to go from current chords -> current roman -> desired roman -> desired chords

    # transform chords in current key to get chords in desired key
    transformed_chords = [desired_key_roman_to_note[current_key_note_to_roman[chord]] for chord in chords_in_current_key]

    # create a dictionary to use those chords in a desired key paired with the current key for replacing
    transformed_chords_dict = {}
    for i in range(len(chords_in_current_key)):
        transformed_chords_dict[chords_in_current_key[i]] = transformed_chords[i]

    # add to the transformed chords dictionary to include m/maj7/7 chords as well
    #m_chords = {a + 'm' : b + 'm' for a,b in transformed_chords_dict.items()}
    #maj7_chords = {a + 'maj7' : b + 'maj7' for a,b in transformed_chords_dict.items()}
    #seven_chords = {a + '7' : b + '7' for a,b in transformed_chords_dict.items()}

    # combine chords dictionaries
    # combine chords dictionaries
    #chords_dict = {**transformed_chords_dict, **m_chords, **maj7_chords, **seven_chords}
    chords_dict = transformed_chords_dict
    #chords_dict = {a.replace('b', flat).replace('#', sharp) : b.replace('b', flat).replace('#', sharp) for a, b in transformed_chords_dict.items()}


    # define a function to replace chords
    def replace_chords(string, chords_dict):

        # format all sharps and flats in the string
        #string = string.replace('b', flat).replace('#', sharp)

        # create a blank string that will be the final string that is created by the function
        final_string = ''

        # create spaces variables to keep track of spaces to add or remove
        spaces_to_remove = 0
        spaces_to_add = 0
        space_found = False

        # go through each line of the string and identify chords (start with A-G)

        i = 0
        while (i < len(string)): # or (string[i:len(string)] == " " * (len(string) - i)):

            # all chords start with the letters A-G, so identify the starts of chords this way
            if string[i] in {'A', 'B', 'C', 'D', 'E', 'F', 'G'}:

                # see if the full chord is a sharp or a flat
                if i == len(string) - 1: # if it's the end of the string, the current string[i] is the chord
                    chord = string[i]
                elif string[i + 1] == ' ': # if the next character is a space, the current string[i] is the chord
                    chord = string[i]
                elif string[i + 1] in {'#', 'b'}: # use in {sharp, flat} if code is updated to include real symbols
                    chord = string[i:i+2]
                else:
                    chord = string[i]

                chord_replacement = chords_dict[chord]

                # if chord and replacement aren't the same length, record # of spaces to adjust
                if len(chord) < len(chord_replacement):
                    spaces_to_remove += 1
                elif len(chord) > len(chord_replacement):
                    spaces_to_add += 1

                # now we want to replace the chord in the final string
                final_string += chord_replacement

                # add on the length of the chord to move the counter forward
                i += len(chord)

                # keep everything that comes after the chord as well
                # if it's not a chord, it might be part of a chord that we just want to keep (e.g. '/', 'm', 'maj7', etc.)
                # anything that's not a space we'll just keep the way it is

            elif string[i] != ' ':
                final_string += string[i]
                i += 1

            else: # (if string[i] == ' ')

                # if there is a space to add, then add it as soon as you reach another space
                if (spaces_to_add > 0) or (spaces_to_remove > 0):

                    if spaces_to_add > 0:
                        final_string += ' ' * (spaces_to_add + 1)
                        spaces_to_add = 0
                        i += 1
                    if spaces_to_remove > 0:
                        # if there is a space to take away, if the next n characters are spaces, take them away
                        # where n is the number of spaces to remove
                        if string[i:i + spaces_to_remove + 1] == " " * (spaces_to_remove + 1):
                            final_string += string[i + spaces_to_remove : i + spaces_to_remove + 1]
                            spaces_to_remove = 0
                            i += spaces_to_remove + 2

                        else: # if you can't remove the space, then just move on
                            final_string += string[i]
                            i += 1
                # if there are no spaces to add or remove, just move the space to final string
                else:
                    final_string += string[i]
                    i += 1
            #print(final_string + ":")

        return(final_string)

    # now we do the actual string replacing within the text based on the chords_dict

    # subset to just the chords in the song and replace those
    chords = song_df1[['line_num', 'class', 'text']][song_df1['class']=='chords'].reset_index(drop=True)
    chords['new_chords'] = chords['text'].apply(replace_chords, args = [chords_dict])


    # join back to the original song_df1 on line number
    song_df2 = song_df1.merge(chords[['line_num', 'new_chords']], how='left', on='line_num')

    # create combined text column with old lyrics and new chords
    song_df2['text2'] = np.where(song_df2['class'] == 'chords', song_df2['new_chords'], song_df2['text'])

    # create a column to store the key of the song
    song_df2['key'] = desired_key


    return(song_df2)








#####################################################################################

# define function to print "paragraphs"/sections of a song onto the PDF

def print_paragraphs(song):

    """
    This function takes a text dataframe and outputs a list of lists containing indices of each line in each paragraph.

    """

    # define starter variables
    current_paragraph_list = []
    paragraphs_list = []
    first_heading = False # only start printing to the paragraph list once we've found the first heading in the song

    i = 0
    while i < len(song):

        # create a new list of indices every time you get to a new heading (after the first heading in the song)
        if song.loc[i, 'class'] == 'heading':

            # if we have a previously completed paragraph
            if len(current_paragraph_list) != 0:
                paragraphs_list.append(current_paragraph_list)

            # append location of text to current paragraph list
            current_paragraph_list = [i]
            first_heading = True

        elif first_heading == True:
            current_paragraph_list.append(i)

        # go to next line
        i+=1

    # append the final paragraph list to the overall list
    paragraphs_list.append(current_paragraph_list)


    return(paragraphs_list)


###############################################################################

# get user inputs for the song, current_key, and desired_key in order to output a pdf

# change working directory
os.chdir(master_path + '/txt_input_files')

song_import_path = input('Enter path to current song.txt file (from ../txt_input_files/ wd):  ')
#current_key = input('Enter the current key for the song:  ')
desired_key = input('Enter the desired key for the song:  ')

# call the function to process those inputs
song = read_song(song_title = song_import_path, desired_key = desired_key)

# split the song up into paragraphs
paragraphs = print_paragraphs(song)




# print the PDF



# get title of pdf and download location - text + key
song_name = song.loc[0, 'text2'].strip()
song_key = song.loc[0, 'key']

# create a folder for the song to store it in different keys it it doesn't already exist
folder = master_path + '/pdf_chord_charts/' + song_name
if not os.path.exists(folder):
    os.makedirs(folder)

# get path to the song itself
song_path = folder + '/' + song_name + ' chords - ' + song_key + '_temp.pdf'

# create the pdf object
canvas = Canvas(song_path, pagesize = LETTER, bottomup=False)

# register and set the font we want to use - get both the regular and bold fonts
pdfmetrics.registerFont(TTFont('Inconsolata',
                               master_path + '/processing_files/fonts/Inconsolata_SemiCondensed-Regular.ttf'))
pdfmetrics.registerFont(TTFont('InconsolataBold',
                               master_path + '/processing_files/fonts/Inconsolata_SemiCondensed-Bold.ttf'))
canvas.setFont('Inconsolata', 10)

# set page margins
center = 8.5*72/2
center_left_margin = center - 10
center_right_margin = center + 10
left_margin = 0.5*72
right_margin = (8.5-0.5)*72
top_margin = 0.5*72
bottom_margin = (11-0.5)*72
width = 8.5*72
height = 11*72


# determine the font size for each line (default 10 unless the line will be too long)
default_font_size = 10
song['line_font_size'] = np.where((song['nspace'] + song['nchar']) * default_font_size * 0.45 <= (center_left_margin - left_margin - 2*8),
                                  default_font_size,
                                  (center_left_margin - left_margin - 2*8) / (0.45 * (song['nspace'] + song['nchar'])))

# if a lyrics line is shortened, have to also shorten the chords line above it
for i in range(len(song)):
    if (song.loc[i, 'line_font_size'] < default_font_size) & (song.loc[i, 'class'] == 'lyrics'):
        song.loc[i-1, 'line_font_size'] = song.loc[i, 'line_font_size']



# print the title on the left side
canvas.setFont('InconsolataBold', 25)
canvas.setStrokeColorRGB(0,0,0)
canvas.setFillColorRGB(0,0,0)
canvas.drawString(x = left_margin, y = top_margin + 10, text = song.loc[0, 'text2'])

# print the key of the song on the right side
canvas.setFont('InconsolataBold', 15)
canvas.setStrokeColorRGB(0,0,0)
canvas.setFillColorRGB(0,0,0)
# get key string
key = 'Key: ' + song.loc[0, 'key']
canvas.drawString(x = right_margin - canvas.stringWidth(key, "InconsolataBold", 15),
                  y = top_margin + 10, text = 'Key: ' + song.loc[0, 'key'])


# this is for printing the title centered if we want
# # get title width to determine positioning
# title_width = canvas.stringWidth(song.loc[0, 'text2'] , "InconsolataBold", 25)
# # set font
# canvas.setFont('InconsolataBold', 25)
# canvas.setStrokeColorRGB(0,0,0)
# canvas.setFillColorRGB(0,0,0)
# canvas.drawString(x = center - 0.5*title_width, y = top_margin, text = song.loc[0, 'text2'])




# get current position as well as the current column to start printing rectangles
current_x = left_margin
current_y = top_margin + 25
column = 1


# print sections of song
for i in range(len(paragraphs)):

    # for each paragraph, determine what shading the rectangle should have (grey for chorus, white everything else)
    if ('chorus' in song.loc[paragraphs[i][0], 'text2'].lower()) & ('pre' not in song.loc[paragraphs[i][0], 'text2'].lower()):

        #set fill and outline for rectangle
        canvas.setStrokeColorRGB(0,0,0)
        canvas.setFillColorRGB(211/256, 211/256, 211/256)

    else:
        #set fill and outline for rectangle
        canvas.setStrokeColorRGB(0,0,0)
        canvas.setFillColorRGB(1,1,1)


    # here's where we'll start the logic to iterate building rectangles of paragraphs


    # set width and height
    rect_width = center_left_margin - left_margin
    rect_height = 5 + len(paragraphs[i])*10 + len(paragraphs[i])*1 + 5


    # check to make sure there's going to be enough space on the page to print the rectangle
    # if so, print that baby as is; if not, move the current x and y position to top left of 2nd column
    if rect_height > height - (current_y):
        current_x = center_right_margin
        current_y = top_margin + 25
        column = 2



    # draw the rectangle
    canvas.roundRect(current_x, current_y, rect_width, rect_height,
                     radius = 10, stroke=1, fill=1) # stroke = border, fill = fill

    # update text position to create left and top margins within rectangle
    # 10pt vertical for text to start at top right of font (since position measured from bottom) + 5pt for the top margin
    current_x += 8
    current_y += 15

    # print the paragraph
    for i in paragraphs[i]:

        # see if it's a heading or lyrics and set font accordingly
        if song.loc[i, 'class'] == 'lyrics':
            canvas.setFont('Inconsolata', song.loc[i, 'line_font_size'])
            canvas.setStrokeColorRGB(0,0,0)
            canvas.setFillColorRGB(0,0,0)
        elif (song.loc[i, 'class'] == 'heading') | (song.loc[i, 'class'] == 'chords'):
            canvas.setFont('InconsolataBold', song.loc[i, 'line_font_size'])
            canvas.setStrokeColorRGB(0,0,0)
            canvas.setFillColorRGB(0,0,0)

        # draw text string
        canvas.drawString(x = current_x, y = current_y, text = song.loc[i, 'text2'])
        current_y += 10 # update y position to account for printing a line

        # change font to add space in between lines
        canvas.setFont('Inconsolata', 3)
        canvas.drawString(x = current_x, y = current_y, text = '\n')
        current_y += 1



    # reset current_x for making the next rectangle outline
    if column == 1:
        current_x = left_margin
    elif column == 2:
        current_x = center_right_margin



# save the pdf object
canvas.save()


#####################

# now we add the oaks logo in the bottom left

# to add an image to a pdf, we have to use a separate pdf library
# have to read in the pdf we just created, write an image on it, and then save it back out to the same path

input_file = song_path
output_file = folder + '/' + song_name + ' chords - ' + song_key + '.pdf'
watermark_file = master_path + "/processing_files/oaks_logo.pdf"

with open(input_file, "rb") as filehandle_input:
    # read content of the original file
    pdf = PyPDF2.PdfFileReader(filehandle_input)

    with open(watermark_file, "rb") as filehandle_watermark:
        # read content of the watermark
        watermark = PyPDF2.PdfFileReader(filehandle_watermark)

        # get first page of the original PDF
        first_page = pdf.getPage(0)

        # get first page of the watermark PDF
        first_page_watermark = watermark.getPage(0)

        # merge the two pages
        first_page.mergePage(first_page_watermark)

        # create a pdf writer object for the output file
        pdf_writer = PyPDF2.PdfFileWriter()

        # add page
        pdf_writer.addPage(first_page)

        with open(output_file, "wb") as filehandle_output:
            # write the watermarked file to the new file
            pdf_writer.write(filehandle_output)


# remove the intermediate version without the watermark
os.remove(song_path)


# print success message
print("Success")
