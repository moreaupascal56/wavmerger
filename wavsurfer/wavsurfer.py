import numpy as np
from scipy.io import wavfile


class WavFile:
    def __init__(self, rate: int = None, data: np.array = None, filepath: str = None):
        """A class to manipulate .wav files.
        You should init with either filepath to a .wav file or the couple (rate,data).

        Args:
            rate (int, optional): .wav file rate. Defaults to None.
            data (np.array, optional): .wav data as a numpyp.array. Defaults to None.
            filepath (str, optional): filepath to a .wav file. Defaults to None.

        Raises:
            ValueError: raised if filepath, rate and data are None
        """
        if filepath is not None:
            self.rate, self.data = wavfile.read(filepath)

        elif rate is not None and data is not None:
            self.rate = rate
            self.data = data
        else:
            raise ValueError(
                "Either filepath or (rate,data) input is mandatory to init a WavFile"
            )

        self.duration = len(self.data) / self.rate

    def to_dict(self) -> dict:
        """Get WavFile data as dict

        Returns:
            dict: dict of the WavFile data.
        """
        return {"rate": self.rate, "data": self.data, "duration": self.duration}

    def write(self, filepath: str):
        """Write the WaveFile to a file.

        Args:
            filepath (str): filepath where to create the .wav file
        """
        wavfile.write(filename=filepath, rate=self.rate, data=self.data)


def concat_wav(wav1: WavFile, wav2: WavFile) -> WavFile:
    """Concatenate 2 .wav files.
    example:
        WavFile1 is a .wav file of someone saying "hello"
        WavFile2 is a .wav file of someone saying "world"
        The output will be the concatenation of both so "Hello world"

    Args:
        wav1 (WavFile): WavFile
        
        wav2 (WavFile): WavFile

    Raises:
        ValueError: Rates are not compatible

    Returns:
        WavFile: The desired Wavfile. The content of the WavFile2 added to WavFile1
    """
    from itertools import chain

    if wav1.rate != wav2.rate:
        raise ValueError("Rates are not compatible")

    else:
        return WavFile(rate=wav1.rate, data=np.array(list(chain(wav1.data, wav2.data))))


def concat_wav_list(wavlist: list[WavFile]) -> WavFile:
    """Concatenate WavFile from a list into a new WavFile, it keeps the list order.


    Args:
        wavlist (list[WavFile]): List of WavFiles to concatenate

    Returns:
        WavFile: The desired Wavfile. The concatenation of all the WavFiles in the list.
    """
    wav = wavlist[0]
    for wavfile in wavlist[1:]:
        wav = concat_wav(wav, wavfile)
    return wav
