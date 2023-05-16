# External Imports
import pandas as pd

def df_to_pitchtier(df : pd.DataFrame, x_column_name : str, y_column_name : str, out_path : str, wav_duration_s : float) -> None :  
    """df_to_pitchtier
    """
    
    # header
    header = [
        'File type = "ooTextFile"',
        'Object class = "PitchTier"',
        "\n",
        f"xmin = 0",
        f"xmax = {wav_duration_s}",
        f"points: size = {len(df)}"
    ]

    body : list = list()
    for index, row in df.iterrows() :
        body.extend([
            f"points [{index+1}]:",
            f"\tnumber = {round(row[x_column_name], 3)}",
            f"\tvalue = {row[y_column_name]}"
        ])

    header = "\n".join(header)
    body = "\n".join(body)

    with open(out_path, mode='w', encoding='utf-8', newline='\n') as f:
        f.write(header)
        f.write(body)

# def df_to_pitchtier(df : pd.DataFrame, x_column_name : str, y_column_name : str, out_path : str, wav_duration_s : float) -> None

