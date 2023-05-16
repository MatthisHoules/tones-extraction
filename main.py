# External Imports
import pandas as pd
import numpy as np
import librosa
import os
import multiprocessing
from dotenv import dotenv_values
import sys
import subprocess

# Internal Imports
from src.pitchtier.PitchTierWriter import df_to_pitchtier
from src.audio.utils import get_wave_duration
from src.utils import is_file_csv

ipu_window_margin_s : float = .1 # 100ms
f0_window_size_s = 0.01 # 10ms
 

def process_chunk(chunk : pd.DataFrame) -> pd.DataFrame :
    """process_chunk

        ### params : 
            chunk : pd.DataFrame - IPUs dataframe to iter
        ### return :
            pd.DataFrame that contains f0_estimation each f0_window_size_s ms
    """

    list_r : list = []
    l_index : list = []
    for index, row in chunk.iterrows() :
        l_index.append(index)
        print("Computing IPU : ", index+1)
        
        if row.transcript is None or row.transcript in ["@", '#', "NaN"] :
            continue

        # Window Margin computation
        start_s : float = round(row.start_s - ipu_window_margin_s, 2) if round(row.start_s - ipu_window_margin_s, 2) > 0 else row.start_s
        end_s  : float = round(row.end_s + ipu_window_margin_s, 2) if round(row.end_s + ipu_window_margin_s, 2) < wav_duration else wav_duration
        duration_s : float = end_s - start_s

        waveform, sr = librosa.load(
            wav_path, 
            offset=start_s, 
            duration=duration_s
        )

        time_to_frame = int(f0_window_size_s * sr)

        f0, _, _ = librosa.pyin(
            waveform,
            fmin=librosa.note_to_hz('C1'),
            fmax=librosa.note_to_hz('C7'),
            sr=sr,
            frame_length=time_to_frame,
            hop_length=time_to_frame
        )

        if len(f0) == 0 :
            continue
        
        time_l = librosa.times_like(f0, hop_length=time_to_frame, sr=sr) 
        times = time_l + start_s # Add IPU start offset

        list_r += list(zip(times, f0))

    df_result = pd.DataFrame(list_r, columns=["time", "f0_estimation"], dtype=np.float64).sort_values("time")
    return df_result
# def process_chunk(chunk : pd.DataFrame) -> pd.DataFrame



def chunk_initializer(*args) :
    """chunk_initializer

        ### params :
            args : 
                [0] : wav path
                [1] : wav duration in seconds
        This function initializes global parameters for chunk pool execution (in __main__)
    """
    
    global wav_path, wav_duration

    wav_path = args[0]
    wav_duration = args[1]
#  def chunk_initializer(*args)



if __name__ == "__main__" :

    assert len(sys.argv) == 2

    inputs_folder_path : str = sys.argv[1]
    assert os.path.isdir(inputs_folder_path)

    inputs_files = os.listdir(inputs_folder_path)
    for file in inputs_files :
        file_path = os.path.join(inputs_folder_path, file)

        print("Processing file ", file_path)

        if not is_file_csv(file_path) :
            print("Not a csv file, continue")
            continue
        
        df_ipus = pd.read_csv(file_path, header=None).rename({
            0 : "IPUs",
            1 : "start_s",
            2 : "end_s",
            3 : "transcript"
        }, axis = 1).dropna().reset_index()

    
        csv_path = file_path
        wav_path = os.path.splitext(csv_path)[0]+".wav"
        wav_duration = get_wave_duration(wav_path)

        num_processes = multiprocessing.cpu_count()

        chunk_size = int(df_ipus.shape[0]/num_processes)
        chunks = [df_ipus.iloc[df_ipus.index[i:i + chunk_size]] for i in range(0, df_ipus.shape[0], chunk_size)]

        pool = multiprocessing.Pool(processes=num_processes, initializer=chunk_initializer, initargs=(wav_path, wav_duration))

        result = pool.map(process_chunk, chunks)

        result = pd.concat(result, axis=0, ignore_index=True)
        result = result.dropna()
        result["time"] = result["time"].round(2)
        df = result.drop_duplicates(subset=["time"])

        common_outpath : str = os.path.splitext(csv_path)[0]
        pitchtier_outpath : str = common_outpath + ".PitchTier"

        df_to_pitchtier(
            df,
            "time",
            "f0_estimation",
            pitchtier_outpath,
            get_wave_duration(wav_path)
        )

        # SPPAS Momel & intsint
        config : dict = dotenv_values(".env")
        python_cmd : str = config.get("PYTHON_CMD")
        sppas_path : str = config.get("SPPAS_PATH")
            
        # Momel
        subprocess.run(
            f"{python_cmd} \"{sppas_path}\\sppas\\bin\\momel.py\" -i \"{pitchtier_outpath}\" -o \"{common_outpath}_momel\""
        )
        # Intsint
        subprocess.run(
            f"{python_cmd} \"{sppas_path}\\sppas\\bin\\intsint.py\" -i \"{pitchtier_outpath}\" -o \"{common_outpath}_intsint\""
        )

