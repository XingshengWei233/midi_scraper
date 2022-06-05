import numpy as np
import argparse
import os
from piano_transcription_inference import PianoTranscription, sample_rate, load_audio
from pathlib import Path
from mido import MidiFile
from utils.midi2array import Midi2Array

"""
input by args: 
    a file containing a list of spotify playlist or artist links
    or a folder containing midi files

    --gui shows when processing with matplotlib

output:
    save converted midi files to a directory

to do:
    
furure:
    use youtubeDL directly to download from more platforms
"""

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_source', type=str, default=None) 
    #'midi_dir', 'playlist_links' or 'artist_links', None for doing all
    parser.add_argument('--list_file', type=str, default=None) 
    parser.add_argument('--gui', type=bool, default=False) 
    #plot array during converting
    return parser.parse_args()

def audio2midi(audio_file):
    print(audio_file)
    (audio, _) = load_audio(audio_file, sr=sample_rate, mono=True)
    transcriptor = PianoTranscription(device='cuda')    # 'cuda' | 'cpu'
    
    # Transcribe and write out to MIDI file
    transcribed_dict = transcriptor.transcribe(audio, os.path.join('../midi_data',Path(audio_file).stem+'.mid'))

def download_playlist_to_midi(url): #download spotify playlist or artist to temp dir as mp3
    os.system('mkdir temp')
    os.chdir('temp/')
    os.system(f"spotdl {url}")
    thisdir = os.getcwd()
    # r=root, d=directories, f = files
    for r, d, f in os.walk(thisdir):
        for file in f:
            if file.endswith(".mp3"):
                audio2midi(file)
    os.chdir('../')
    os.system('rm -r temp')
    
def download_list_file(list_file):
    file = open(list_file, 'r')
    urls = file.readlines()
    file.close
    for i, url in enumerate(urls):
        print(f'processing line: {i}')
        download_playlist_to_midi(url)

def replace_symbol(midi_data_dir):
    for filename in os.listdir(midi_data_dir):
        new_filename = filename.replace(' ', '_')
        new_filename = new_filename.replace('_-_', '-')
        new_filename = new_filename.replace("'", '+')
        os.rename(os.path.join(midi_data_dir,filename),os.path.join(midi_data_dir, new_filename))

def main(args):
    pass

if __name__ == '__main__':
    args = get_args()
    list_file = 'playlist_links.txt'
    midi_data_dir = 'midi_data'
    download_list_file(list_file)
    replace_symbol(midi_data_dir)

    