# Swiss-German DeepSpeech Importer

This repository holds an Importer for the ArchiMob speech corpus.
The importer pre-processes the text-data so that it can be used with the open-source Speech-to-Text engine by DeepSpeech.

**Table of Contents**

- [Prerequisites](#prerequisites)
- [ArchiMob Corpus](#ArchiMob-Corpus)
- [Automatic Speech Recognition with Mozilla's DeepSpeech](#Automatic-Speech-Recognition-with-Mozilla's-DeepSpeech)
- [Walk-through ArchiMob Importer](#Walk-through-ArchiMob-Importer)
- [About this project](#About-this-project)

<h>


## Prerequisites

* [Python 3.6](https://www.python.org/)
* [Git Large File Storage](https://git-lfs.github.com/)
* [tqdm](https://pypi.org/project/tqdm/)


## ArchiMob Corpus

<p>The ArchiMob corpus holds swiss german audio data as well as swiss-german and "high-german" transcriptions. </p>
<p>The corpus is available under the <a href='https://creativecommons.org/licenses/by-nc-sa/4.0/'>Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a> and is provided by the <a href='https://www.spur.uzh.ch/en/departments/research/textgroup/ArchiMob.html'>Language and Space Lab of the University of Zurich</a>. This importer builds upon the ArchiMob corpus license and therefore is restricted to the same license.</p>

<p>The transcriptions including media-pointers (IDs to the audio file segments) are available in the XML-files <a href='https://www.spur.uzh.ch/en/departments/research/textgroup/ArchiMob.html'>here</a>. When using this importer, the XML-files do not have to be downloaded automatically</p>

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
  - Samplerate: 16kHz
  - Bit pro Sample: 16bit

<b>Walk-through</b>
- The transcriptions of ArchiMob audio data is stored in XML files.
- If the folder ./audio exists the ArchiMob audio files are pre-processed:
  - First, files are merged from subfolders into ./Pre_Processing_Files/audio_merged.
  - 1.2 Next, the .wav files are pre-processed according to above format-specifications
- The CH and DE words are extracted from the XML file and joined to strings with the media-pointer ID (which matches the audio_filename)
- Next, duplicates are removed (duplicates exist in XML files when an audio file contains two speakers) to simplify training for DeepSpeech. (A list of the removed duplicates are available in ./Pre_Processing_Files/CSV_Merged/)
- Next, Zero values are dropped (audio files with silences contain zero values in the transcriptions)
- Next, the CSV Files of the XML packages (e.g. 1300, 1295) are merged into one file per language (DE/CH). During this process, 304 files below 10'000 Bytes and above 318'400 Bytes (longer than 10 seconds) are dropped. *
- Then, a CSV that contains [wav_filename], [wav_filesize] of .wav files in ./Pre_Processing_Files/audio_processed_final/ is created
- Lastly, the merged transcripts and the CSV with filepaths and filesizes are merged
- Final output of the importer pipeline can be found in ./Final_Training_CSV_for_Deespeech/

'*' This step is necessary to ensure good audio quality. Small files contain unrecognizable audio or chopped syllables (Example: d1205_T864.wav (>10'000 Bytes) contains the sound "mhm" which is valid, d1248_T502.wav (<10'000 Bytes) however, contains the chopped sound "m" and is therefore removed). Large files are not feasible because they are too long for proper training in DeepSpeech. For traceability-purposes, have a look at the overview in folder ./Resources/Audio-Overview/DS_Data_Archimob_size_length.xlsx

<b> Please note that the full script that processes all ca. 70'000 .wav files can take a long time, because of audio pre-processing</b>

## About this project:

<p>This importer was created as part of the Master Thesis "Automatic Speech Recognition for Swiss German using Deep Neural Networks" for the degree Master of Business Innovation at the University of St. Gallen by Tobias Rordorf. In case of questions please feel free to contact me through <a href='https://www.linkedin.com/in/tobiasrordorf/'>LinkedIn</a>.
