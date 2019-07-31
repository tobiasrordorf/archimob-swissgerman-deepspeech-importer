import librosa
import soundfile
import os
import time
import sys
import shutil

def pre_process_audio():
    path_audio_processed_f = './audio_processed_final'
    if not os.path.exists(path_audio_processed_f):
        try:
            os.mkdir(path_audio_processed_f)
        except OSError:
            print('Creation of directory %s failed' %path_audio_processed_f)
        else:
            print('Successfully created the directory %s' %path_audio_processed_f)

    try:
        start = time.time()
        n = 0
        audio_path = "./audio_merged/"
        for file in os.listdir(audio_path):
            if(file.endswith('.wav')):
                nameSolo_1 = file.rsplit('.', 1)[0]
                y, s = librosa.load(audio_path + file, sr=16000) # Downsample 44.1kHz to 8kHz
                librosa.output.write_wav('./audio_processed_final/' + nameSolo_1 + '.wav', y, s)
                n = n+1
                print('File ', n , ' completed:', nameSolo_1)

        print('Downsampling complete')
        print('----------------------------------------------------------')

        directory = "./audio_processed_final/"

        s = 0
        for file in os.listdir(directory):
            if(file.endswith('.wav')):
                nameSolo_2 = file.rsplit('.', 1)[0]
                data, samplerate = soundfile.read(directory + file)
                soundfile.write('./audio_processed_final/' + nameSolo_2 + '.wav', data, samplerate, subtype='PCM_16')
                #print("converting " + file + " to 16 - bit")
                s = s + 1
                print('File ' , s , ' completed')

        print('Bit pro sample changed')

        shutil.rmtree('./audio', ignore_errors=True)
        shutil.rmtree('./audio_merged', ignore_errors=True)
        end = time.time()

        print('The script took ', end-start, ' seconds to run')
    except EOFError as error:
        next


#Source:
#https://stackoverflow.com/questions/30619740/python-downsampling-wav-audio-file
#https://stackoverflow.com/questions/44812553/how-to-convert-a-24-bit-wav-file-to-16-or-32-bit-files-in-python3
