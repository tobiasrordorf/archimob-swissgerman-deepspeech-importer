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



## About this project: 

<p>This importer was created as part of the Master Thesis "Automatic Speech Recognition for Swiss German using Deep Neural Networks" for the degree Master of Business Innovation at the University of St. Gallen by Tobias Rordorf. In case of questions you can contact me through <a href='https://www.linkedin.com/in/tobiasrordorf/'>LinkedIn</a>.
