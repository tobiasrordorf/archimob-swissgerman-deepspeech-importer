#!/usr/bin/env python
# coding: utf-8

## Extract words from XML into CSV for transcript matching, in preparation for DeepSpeech training CSV
##
print('The ArchiMob importer in preparation for DeepSpeech training has started')

#Imports
import xml.etree.ElementTree as ET
import pandas as pd
from glob import glob
from pathlib import Path
import numpy as np
import os
from tqdm.auto import tqdm            # conda install tqdm / pip install tqdm
from joblib import Parallel, delayed  # conda install joblib
from zipfile import ZipFile
import requests
from io import BytesIO
from urllib.request import urlopen
import shutil

#Import Audio pre-processing function
from change_sample_rate import pre_process_audio



#Download XML Zip File of ArchiMob Corpus
url = 'https://www.spur.uzh.ch/dam/jcr:9e63ee4b-42eb-4204-a869-53aa2042d57c/ArchiMob_Release1_160812.zip'
file_name = 'ArchiMob_Release1_160812.zip'


def download_and_extract_zip(url):
    with urlopen(url) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall('./Pre_Processing_Files')

download_and_extract_zip(url)

#Creating the necessary directories
path_PP = './Pre_Processing_Files'

if not os.path.exists(path_PP):
    try:
        os.mkdir(path_PP)
    except OSError:
        print('Creation of directory %s failed' %path_PP)
    else:
        print('Successfully created the directory %s' %path_PP)

path_DS = './Final_Training_CSV_for_Deespeech'

if not os.path.exists(path_DS):
    try:
        os.mkdir(path_DS)
    except OSError:
        print('Creation of directory %s failed' %path_DS)
    else:
        print('Successfully created the directory %s' %path_DS)

path_Extracts_CH = './Pre_Processing_Files/ArchiMob_Release1_160812/XML_Transcripts_CH'

if not os.path.exists(path_Extracts_CH):
    try:
        os.mkdir(path_Extracts_CH)
    except OSError:
        print('Creation of directory %s failed' %path_Extracts_CH)
    else:
        print('Successfully created the directory %s' %path_Extracts_CH)

path_Extracts_DE = './Pre_Processing_Files/ArchiMob_Release1_160812/XML_Transcripts_DE'
if not os.path.exists(path_Extracts_DE):
    try:
        os.mkdir(path_Extracts_DE)
    except OSError:
        print('Creation of directory %s failed' %path_Extracts_DE)
    else:
        print('Successfully created the directory %s' %path_Extracts_DE)

path_CSV_merged = './Pre_Processing_Files/CSV_Merged'
if not os.path.exists(path_CSV_merged):
    try:
        os.mkdir(path_CSV_merged)
    except OSError:
        print('Creation of directory %s failed' %path_CSV_merged)
    else:
        print('Successfully created the directory %s' %path_CSV_merged)

path_DS_audio = './Pre_Processing_Files/DS_audio'
if not os.path.exists(path_DS_audio):
    try:
        os.mkdir(path_DS_audio)
    except OSError:
        print('Creation of directory %s failed' %path_DS_audio)
    else:
        print('Successfully created the directory %s' %path_DS_audio)

#Audio pre-processing

def merge_audiofiles_from_folders ():
    path_audio = './Pre_Processing_Files/audio_merged'
    if not os.path.exists(path_audio):
        try:
            os.mkdir(path_audio)
        except OSError:
            print('Creation of directory %s failed' %path_audio)
        else:
            print('Successfully created the directory %s' %path_audio)

    src = r'./audio'
    dest = r'./Pre_Processing_Files/audio_merged'

    for path, subdirs, files in os.walk(src):
        for name in files:
            filename = os.path.join(path, name)
            shutil.copy2(filename, dest)
    print('Audio-Files-Merge complete, dir "audio_merged" created ')



if os.path.isdir('./audio') is True:
    merge_audiofiles_from_folders()
    pre_process_audio()
else:
    print('No directory "audio" detected and therefore no audio-pre-processing initiated')
    print('See Readme.md for more information on ArchiMob audio files')
    next

#Extracting DE and CH Texts from XML Files and saving the outputs per file in a csv

def extract(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    de_data = pd.DataFrame(columns=['Filename', 'transcript'])
    ch_data = pd.DataFrame(columns=de_data.columns)

    #loop through u-tags which each stand for 1 audio file (e.g. d1007_T1.wav)
    for text in tqdm(root.iter('{http://www.tei-c.org/ns/1.0}u'), desc=f'Extracting transcriptions: {xml_file.name}'):
        media = text.attrib['start']
        filename = media.split('#')[1]

        #w-tags contain the individual words of the audio files
        word = text.findall('{http://www.tei-c.org/ns/1.0}w')

        #loop through all w-tags in the u-tags
        de_transcript = []
        ch_transcript = []
        for token in word:
            de_transcript.append(token.attrib['normalised'])
            ch_transcript.append(token.text)

        try:
            de_data = de_data.append({'Filename': filename, 'transcript': " ".join(de_transcript)}, ignore_index=True)
            ch_data = ch_data.append({'Filename': filename, 'transcript': " ".join(ch_transcript)}, ignore_index=True)
        except:
            next

    de_data.to_csv(Path('./Pre_Processing_Files/ArchiMob_Release1_160812/XML_Transcripts_DE', f'{xml_file.stem}_transcript_DE.csv'), header=True, index=False, encoding='utf-8-sig')
    ch_data.to_csv(Path('./Pre_Processing_Files/ArchiMob_Release1_160812/XML_Transcripts_CH', f'{xml_file.stem}_transcript_CH.csv'), header=True, index=False, encoding='utf-8-sig')

#Remove duplicates and drop zero values

def remove_duplicates_CH ():
    save_duplicates_CH = pd.DataFrame()
    for csvfile in glob('./Pre_Processing_Files/ArchiMob_Release1_160812/XML_Transcripts_CH/*.csv'):
        #read csv files of XML Extracts and sort by filename
        df_duplicates_CH = pd.read_csv(csvfile)
        df_duplicates_CH.sort_values("Filename", inplace=True)
        #save duplicates to dataframe to later save to csv-file
        write_duplicates_CH = df_duplicates_CH[df_duplicates_CH.duplicated(['Filename'], keep=False)]

        #remove zero values
        df_duplicates_CH['transcript'] = df_duplicates_CH['transcript'].replace('', np.nan)
        df_duplicates_CH = df_duplicates_CH.dropna(axis=0, subset = ['transcript'])

        #remove one of the exact duplicates but keep the other one
        df_duplicates_CH.drop_duplicates(keep='first', inplace=True)

        #clear csvfiles of XML Extracts of duplicates
        df_removed_CH = df_duplicates_CH.drop_duplicates(['Filename'], inplace=True, keep=False)
        df_duplicates_CH.to_csv(csvfile, header=True, index=False, encoding='utf-8-sig')

        save_duplicates_CH = save_duplicates_CH.append(write_duplicates_CH)
    save_duplicates_CH.to_csv('./Pre_Processing_Files/CSV_Merged/ArchiMob_Transcript_list_of_double IDs_CH.csv', header=True, index=False, encoding='utf-8-sig')
    print('Duplicates and zero values removed for CH-Files')

def remove_duplicates_DE ():
    save_duplicates_DE = pd.DataFrame()
    for csvfile in glob('./Pre_Processing_Files/ArchiMob_Release1_160812/XML_Transcripts_DE/*.csv'):
        #read csv files of XML Extracts and sort by filename
        df_duplicates_DE = pd.read_csv(csvfile)
        df_duplicates_DE.sort_values("Filename", inplace=True)
        #save duplicates to dataframe to later save to csv-file
        write_duplicates_DE = df_duplicates_DE[df_duplicates_DE.duplicated(['Filename'], keep=False)]

        #remove zero values
        df_duplicates_DE['transcript'] = df_duplicates_DE['transcript'].replace('', np.nan)
        df_duplicates_DE = df_duplicates_DE.dropna(axis=0, subset = ['transcript'])

        #remove one of the exact duplicates but keep the other one
        df_duplicates_DE.drop_duplicates(keep='first', inplace=True)

        #clear csvfiles of XML Extracts of duplicates
        df_removed_DE = df_duplicates_DE.drop_duplicates(['Filename'], inplace=True, keep=False)
        df_duplicates_DE.to_csv(csvfile, header=True, index=False, encoding='utf-8-sig')

        save_duplicates_DE = save_duplicates_DE.append(write_duplicates_DE)
    save_duplicates_DE.to_csv('./Pre_Processing_Files/CSV_Merged/ArchiMob_Transcript_list_of_double IDs_DE.csv', header=True, index=False, encoding='utf-8-sig')
    print('Duplicates and zero values removed for DE-Files')

#Merge CSV File per XML package to one file per language
#This step is in preparation for the creation of the CSV File for the DeepSpeech Training

def merge_ch ():
    df_combined_CH = pd.DataFrame()

    for entry in glob ('./Pre_Processing_Files/ArchiMob_Release1_160812/XML_Transcripts_CH/*.csv'):
        df = pd.read_csv(entry)
        df_combined_CH = df_combined_CH.append(df)

    df_combined_CH.to_csv('./Pre_Processing_Files/CSV_Merged/ArchiMob_Transcript_Merged_CH.csv', header=True, index=False, encoding='utf-8-sig')
    print('All CH files merged')

def merge_de ():
    df_combined_DE = pd.DataFrame()

    for entry in glob ('./Pre_Processing_Files/ArchiMob_Release1_160812/XML_Transcripts_DE/*.csv'):
        df = pd.read_csv(entry)
        df_combined_DE = df_combined_DE.append(df)

    df_combined_DE.to_csv('./Pre_Processing_Files/CSV_Merged/ArchiMob_Transcript_Merged_DE.csv', header=True, index=False, encoding='utf-8-sig')
    print('All DE files merged')

def create_DS_csv ():
    print('Extracting Filepath and -size for ArchiMob Audio')
    #this function holds the code to extract the filepath and filesize of all audio in the respective directory
    data = pd.DataFrame(columns=['wav_filename', 'wav_filesize'])
    df = pd.DataFrame(columns=['wav_filename', 'wav_filesize'])

    for entry in glob('./Pre_Processing_Files/audio_processed_final/*.wav'):
        filepath = os.path.abspath(entry)
        filesize = os.path.getsize(entry)
        df['wav_filename'] = [filepath]
        df['wav_filesize'] = [filesize]
        data = data.append(df)
    data.to_csv('./Pre_Processing_Files/DS_audio/DS_Data_Archimob_Filepath_Filesize.csv', header=True, index=False, encoding='utf-8-sig')


def merge_AM_transcripts (language):
    df_ds_csv = pd.read_csv('./Pre_Processing_Files/DS_audio/DS_Data_Archimob_Filepath_Filesize.csv')
    df_ds_csv['Filename'] = df_ds_csv['wav_filename']

    #Extract ID from filepath for merging
    def extract_ID (x):
        y = x.split('l/')[1]
        z = y[:-4]
        return z

    df_ds_csv_2 = df_ds_csv['Filename'].apply(extract_ID)
    df_ds_csv['Filename'] = df_ds_csv_2
    df_ds_csv.to_csv('./Pre_Processing_Files/DS_audio/DS_Data_Archimob_Prep.csv', header=True, index=False, encoding='utf-8-sig')

    #replace deviating characters from Transcript file,
    df_archi_trans = pd.DataFrame()
    df_archi_trans = pd.read_csv('./Pre_Processing_Files/CSV_Merged/ArchiMob_Transcript_Merged_' + language +'.csv')
    df_archi_trans['Filename'] = df_archi_trans['Filename'].str.replace('-', '_')

    #Merge on the column Filename
    add_transcripts = pd.DataFrame()
    add_transcripts = pd.merge(df_ds_csv, df_archi_trans, on='Filename')

    #Only save lines with filesize over 10'000 bytes and smaller than 318'400 (below 10 seconds)
    add_transcripts = add_transcripts.drop(columns=['Filename'])

    add_transcripts[add_transcripts['wav_filesize'] > 10000].to_csv('./Final_Training_CSV_for_Deespeech/DS_Archimob_Merged_'+language+'.csv', header=True, index=False, encoding='utf-8-sig')
    resize = pd.read_csv('./Final_Training_CSV_for_Deespeech/DS_Archimob_Merged_' + language +'.csv')
    resize[resize['wav_filesize']< 318400].to_csv('./Final_Training_CSV_for_Deespeech/DS_Archimob_Merged_'+language+'.csv', header=True, index=False, encoding='utf-8-sig')
    print('Merged Transcripts and Filenames and resized sample')

#Call the functions

#Extract CH and DE from XMLs
path_to_XML = './Pre_Processing_Files/ArchiMob_Release1_160812/XML/Content'
_ = Parallel(n_jobs=4)(delayed(extract)(xml_file) for xml_file in tqdm(list(Path(path_to_XML).glob("*.xml")), desc="XML Conversion"))

#Remove duplicates in CH and DE data
remove_duplicates_CH()
remove_duplicates_DE()

#merge seperate csv files from XML packages to one merged csv file
merge_ch()
merge_de()

#This function creates a CSV file with the columns Filepath and Filesize for DS-Training
if os.path.isdir('./Pre_Processing_Files/audio_processed_final') is True:
    create_DS_csv()
else:
    print('WARNING: No folder "audio_processed_final" with ArchiMob audio files detected, therefore no Transcript-Merge with Filepath&Filesize')
    print('See Readme.md for information on ArchiMob audio files')
    next

#Merge the transcripts from the XML files with the DeepSpeech CSV
#The DS-CSV offers filepaths and filesize of all audio files in the directory

if os.path.isdir('./Pre_Processing_Files/audio_processed_final') is True:
    merge_AM_transcripts('CH')
    merge_AM_transcripts('DE')
else:
    next

print('*** Finished ***')
print('The preprocessing of Transcripts and Audio (if available) from ArchiMob is complete')
print('The final CSV files for DeeSpeech training are stored in the folder: "Final_Training_CSV_for_Deespeech"')
