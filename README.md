# Swiss-German DeepSpeech Importer

This repository holds an Importer for the ArchiMob speech corpus.
The importer pre-processes the audio- and text-data so that it can be used with the open-source Speech-to-Text engine by DeepSpeech.

**Table of Contents**

- [Prerequisites](#prerequisites)
- [ArchiMob Corpus](#ArchiMob-Corpus)
- [Automatic Speech Recognition with Mozilla's DeepSpeech](#Automatic-Speech-Recognition-with-Mozilla's-DeepSpeech)
- [Walk-through ArchiMob Importer](#Walk-through-ArchiMob-Importer)
- [Check-Characters](#Check-Characters)
- [About this project](#About-this-project)

<h>


## Prerequisites

* [Python 3.6](https://www.python.org/)
* [Git Large File Storage](https://git-lfs.github.com/)
* [tqdm](https://pypi.org/project/tqdm/)


## ArchiMob Corpus

<p>The ArchiMob corpus holds swiss german audio data as well as swiss-german and "high-german" transcriptions. </p>
<p>The corpus is available under the <a href='https://creativecommons.org/licenses/by-nc-sa/4.0/'>Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a> and is provided by the <a href='https://www.spur.uzh.ch/en/departments/research/textgroup/ArchiMob.html'>Language and Space Lab of the University of Zurich</a>. This importer builds upon the ArchiMob corpus license and therefore is restricted to the same license.</p>

<p>The transcriptions including media-pointers (IDs to the audio file segments) are available in the XML-files <a href='https://www.spur.uzh.ch/en/departments/research/textgroup/ArchiMob.html'>here</a>. When using this importer, the XML-files will be downloaded automatically.</p>

<p>At the time of the creation of this importer the Archimob corpus featured 75'344 audio files and 52 XML files. full list of Filenames in <a href='https://github.com/tobiasrordorf/swissgerman-deepspeech-importer/tree/master/Resources'>Resources</a>)</p>

<p>For access to the audio files, please follow the information on the homepage of the "Language and Space Lab"</p>


## Automatic Speech Recognition with Mozilla's DeepSpeech

<p> DeepSpeech by Mozilla is a TensorFlow implementation of <a href='https://arxiv.org/abs/1412.5567'>Baidu's DeepSpeech architecture</a></p>
<p> It is an open-source Speech-To-Text engine, and can ideally be used in combination with <a href='https://voice.mozilla.org/'>CommonVoice datasets</a>.
<p>The repository can be accessed through this link: <a href='https://github.com/mozilla/DeepSpeech'> DeepSpeech</a> </p>

## Walk-through ArchiMob Importer

<b>This section will explain what the importer does in detail in order to provide understanding of the individual steps</b>

<b>First</b>, it is crucial to understand that DeepSpeech requires the following pre-processing of data in order for the Speech-to-Text engine to be trained:
- Text-Data
  - For training purposes, a CSV with the columns [wav_filepath], [wav_filesize], and [Transcript] has to be created
- Audio
  - The audio has to be pre-processed in order to be used for training the DeepSpeech engine.
  - Audio File Format: .wav
  - Sampling rate: 16kHz
  - Audio bit depth: 16bit
  - Original ArchiMob data is formatted as follows: wav-file-format; Sampling rate: 48kHz; Audio bit depth: 16; Mono audio channel.

<b>Walk-through</b>

- Info:
  - The transcriptions of the audio files are available in Swiss German (CH) and standard German (DE), and are stored in XML files.
  - If you have acquired the audio files as mentioned above, create a folder called 'audio' and place the files in this folder. (If no 'audio'-folder exists, the script will not pre-process any audio and will not be able to match the transcripts to the available audio files)

- Steps:
1. Audio files are merged from subfolders into one folder in ./Pre_Processing_Files/audio_merged.
2. Wav-Files are pre-processed according to above format-specifications and stored in ./Pre_Processing_Files/audio_processed_final

3. The CH and DE words are extracted from the XML-files and joined to strings with the corresponding media-pointer ID (which matches the audio_filename), and stored in csv per XML-file
4. Duplicates and zero values in transcriptions  are removed. (List of removed duplicates are available in ./Pre_Processing_Files/CSV_Merged/)
5. All csv per language are merged

6. A csv that contains [wav_filename], [wav_filesize] of all wav files in ./Pre_Processing_Files/audio_processed_final/ is created.
7. The transcriptions, filenames and filesizes are merged and files below 10'000 Bytes and above 318'400 Bytes are dropped. (See comment below)
8. The merged transcripts are then cleaned of unwanted characters (e.g. semicolon, commas etc.)
9. The DE-transcriptions of files of the package 'd1163' are removed because they have not been translated

10. The final transcripts are splitted into train, test, and dev files and stored in ./Final_Training_CSV_for_Deepspeech/. (train: 75%, test: 15%, dev: 10%)



<i>Dropping due to size restrictions: This step is necessary to ensure good audio quality. Small files contain unrecognizable audio or chopped syllables (Example: d1205_T864.wav (>10'000 Bytes) contains the sound "mhm" which is valid, d1248_T502.wav (<10'000 Bytes) however, contains the chopped sound "m" and is therefore removed). Large files are not feasible because they are too long for proper training in DeepSpeech. For traceability-purposes, have a look at the overview in folder ./Resources/Audio-Overview/DS_Data_Archimob_size_length.xlsx</i>

<b> Please note that the full script that processes all wav and XML files can take up to 3.5 hours (due to extensive audio pre-processing)</b>

## Check characters

<p> In order to compile the necessary language models required by DeepSpeech, the alphabet.txt has to be configured to the Archimob-dataset</p>
<p> The script check_caracters.py (provided by DeepSpeech) generates a list of characters that appear in the csv-files. It can be instantiated like this: python3 ./Check_Characters/check_characters.py -csv './Final_Training_CSV_for_Deepspeech/ch_dev.csv' -alpha</p>


## About this project:

<p>This importer was created as part of the Master Thesis "Automatic Speech Recognition for Swiss German using Deep Neural Networks" for the degree Master of Business Innovation at the University of St. Gallen by Tobias Rordorf. In case of questions please feel free to contact me through <a href='https://www.linkedin.com/in/tobiasrordorf/'>LinkedIn</a>.
