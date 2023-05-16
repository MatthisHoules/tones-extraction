import os
import filetype
import wave


def is_file_wav(path : str) -> bool :
    """
        ## is_file_wav

        ### params :
            path : path to check of the file is a wav file or not
        ### return :
            True if the file is a .wav file, False instead
    """

    if not os.path.exists(path) or not os.path.isfile(path) :
        return False
        
    kind = filetype.guess(path)
    return kind is not None and kind.extension == "wav"
# def is_file_wav(path : str) -> bool 


def get_wave_duration(wav_path : str) -> float :
    """get_wave_duration

        ### params :
            wav_path : wav file path
        ### return : 
            wav duration in seconds
    """

    assert is_file_wav(wav_path) is True

    w = wave.open(wav_path,'r')

    frames = w.getnframes()
    sr = w.getframerate()
    
    duration = frames / float(sr)
    return duration
# def get_wave_duration(wav_path : str) -> float