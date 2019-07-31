# Swiss-German DeepSpeech Importer

This repository holds an Importer for the ArchiMob speech corpus.
The importer pre-processes the text-data so that it can used with the open-source Speech-to-Text engine by DeepSpeech.

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
<p>The corpus is available under the <a href='https://creativecommons.org/licenses/by-nc-sa/4.0/'>Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a> and is provided by the <a href='https://www.spur.uzh.ch/en/departments/research/textgroup/ArchiMob.html'>Language and Space Lab of the University of Zurich</a>.</p>

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
1. If the folder ./audio exists the ArchiMob audio files are pre-processed:
  1.1 First, files are merged from subfolders into ./Pre_Processing_Files/audio_merged.
  1.2 Next, the .wav files are pre-processed according to above format-specifications
2.  The CH and DE words are extracted from the XML file and joined to strings with the media-pointer ID (which matches the audio_filename)
3. Next, duplicates are removed (duplicates exist in XML files when an audio file contains two speakers) to simplify training for DeepSpeech. (A list of the removed duplicates are available in ./Pre_Processing_Files/CSV_Merged/)
4. Next, Zero values are dropped (audio files with silences contain zero values in the transcriptions)
5. Next, the CSV Files of the XML packages (e.g. 1300, 1295) are merged into one file per language (DE/CH)
5. Then, a CSV that contains [wav_filepath], [wav_filesize] of .wav files in ./Pre_Processing_Files/audio_processed_final/ is created
6. Lastly, the merged transcripts and the CSV with filepaths and filesizes are merged
7. Final output of the importer pipeline can be found in ./Final_Training_CSV_for_Deespeech/


## About this project:

<p>This importer was created as part of the Master Thesis "Automatic Speech Recognition for Swiss German using Deep Neural Networks" for the degree Master of Business Innovation at the University of St. Gallen by Tobias Rordorf. In case of questions you can contact me through <a href='https://www.linkedin.com/in/tobiasrordorf/'>LinkedIn</a>.
