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
  - For training purposes, a CSV with the columns [filepath], [filesize], and [transcript] has to be created


- The transcriptions of ArchiMob audio data is stored in XML files.
- Below scripts extract the words for every seperate audio file and joins the strings to be outputted into a CSV.
- There are seperate version for CH-words and DE-words
- Next, duplicates are removed (for exact duplicates the first one is kept; for not exact duplicates (multiple voices in one audio) the duplicates are removed completly
- Zero Values are dropped
- Lastly, CSV Files are merged per language
- This is the necessary preparation as the importer of ArchiMob for the training CSV for DeepSpeech

## About this project:

<p>This importer was created as part of the Master Thesis "Automatic Speech Recognition for Swiss German using Deep Neural Networks" for the degree Master of Business Innovation at the University of St. Gallen by Tobias Rordorf. In case of questions you can contact me through <a href='https://www.linkedin.com/in/tobiasrordorf/'>LinkedIn</a>.
