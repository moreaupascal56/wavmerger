import numpy as np
import pytest
from numpy.testing import assert_array_equal

from wavmerger import WavFile, concat_wav, concat_wav_list


@pytest.fixture
def temp_dir(tmp_path) -> str:
    """Creates a temporary directory for tests

    Args:
        tmp_path (_type_): tmp_path fixture

    Returns:
        str: tmp_path
    """
    return tmp_path


@pytest.fixture
def get_rate_data() -> dict:
    """Get example rate and data

    Returns:
        dict: dict of rate and data
    """
    samplerate = 44100
    fs = 100
    t = np.linspace(0.0, 1.0, samplerate)
    amplitude = np.iinfo(np.int16).max
    data = amplitude * np.sin(2.0 * np.pi * fs * t)
    return {"rate": samplerate, "data": data}


@pytest.fixture
def create_wav_file(temp_dir, get_rate_data) -> str:
    """Creates a .wav file

    Args:
        temp_dir (_type_): fixture
        get_rate_data (_type_): fixture to get example rate and data

    Returns:
        str: the .wav file path
    """

    from scipy.io.wavfile import write

    write(temp_dir / f"example.wav", get_rate_data["rate"], get_rate_data["data"])

    return temp_dir / f"example.wav"


class TestWavFile:
    """Tests the WavFile class"""

    def WavFileEquality(wav: WavFile, expected: dict):
        """An equality test for WavFiles

        Args:
            wav (WavFile): WavFile to test
            expected (dict): expected values as a dict
        """
        d = wav.to_dict()
        assert d["rate"] == expected["rate"]
        assert d["duration"] == expected["duration"]
        assert_array_equal(d["data"], expected["data"])
        assert d.keys() == expected.keys()

    def test_init_from_rate_data(self, get_rate_data):
        """Tests WavFile initialization with rate and data

        Args:
            get_rate_data (_type_): fixture
        """

        wav = WavFile(rate=get_rate_data["rate"], data=get_rate_data["data"])
        assert wav.rate == get_rate_data["rate"]
        assert_array_equal(wav.data, get_rate_data["data"])

    def test_init_from_filepath(self, create_wav_file, get_rate_data):
        """Tests WavFile initialization with filepath

        Args:
            create_wav_file (_type_): fixture
            get_rate_data (_type_): fixture
        """
        wav = WavFile(filepath=create_wav_file)
        assert wav.rate == get_rate_data["rate"]
        assert_array_equal(wav.data, get_rate_data["data"])

    def test_init_fail_from_none(self):
        """Tests WavFile error if filepath, rate and data are None"""
        with pytest.raises(ValueError):
            wav = WavFile()

    def test_to_dict(self):
        """Tests the WavFile.to_dict method."""
        d = WavFile(rate=21, data=np.array([1, 2, 3])).to_dict()
        expected = {"rate": 21, "data": np.array([1, 2, 3]), "duration": 3 / 21}

        assert d["rate"] == expected["rate"]
        assert d["duration"] == expected["duration"]
        assert_array_equal(d["data"], expected["data"])
        assert d.keys() == expected.keys()


class TestWavOperations:
    """Tests the operation functions on WavFile"""

    @pytest.mark.parametrize(
        "wav1,wav2,expected",
        [
            (
                WavFile(rate=24000, data=np.array([1, 2, 3])),
                WavFile(rate=24000, data=np.array([4, 5, 6])),
                {"rate": 24000, "data": [1, 2, 3, 4, 5, 6], "duration": 6 / 24000},
            ),
            (
                WavFile(rate=18000, data=np.array([1, 2, 3])),
                WavFile(rate=24000, data=np.array([4, 5, 6])),
                None,
            ),
        ],
    )
    def test_concat_wav(self, wav1, wav2, expected):
        """Tests concat_wav function

        Args:
            wav1 (_type_): WavFile
            wav2 (_type_): WavFile
            expected (_type_): expected WavFile dict
        """
        if not expected:
            with pytest.raises(ValueError):
                concat_wav(wav1, wav2)
        else:
            TestWavFile.WavFileEquality(concat_wav(wav1, wav2), expected)

    @pytest.mark.parametrize(
        "wavlist,expected",
        [
            (
                [
                    WavFile(rate=24000, data=np.array([1, 2, 3])),
                    WavFile(rate=24000, data=np.array([4, 5, 6])),
                ],
                {"rate": 24000, "data": [1, 2, 3, 4, 5, 6], "duration": 6 / 24000},
            ),
            (
                [
                    WavFile(rate=24000, data=np.array([0])),
                    WavFile(rate=24000, data=np.array([1, 2, 3])),
                    WavFile(rate=24000, data=np.array([4, 5, 6])),
                ],
                {"rate": 24000, "data": [0, 1, 2, 3, 4, 5, 6], "duration": 7 / 24000},
            ),
            (
                [
                    WavFile(rate=18000, data=np.array([1, 2, 3])),
                    WavFile(rate=24000, data=np.array([4, 5, 6])),
                ],
                None,
            ),
        ],
    )
    def test_concat_wav_list(self, wavlist, expected):
        """Tests concat_wav function

        Args:
            wavlist (_type_): list of WavFiles
            expected (_type_): expected WavFile dict
        """
        if not expected:
            with pytest.raises(ValueError):
                concat_wav_list(wavlist)
        else:
            TestWavFile.WavFileEquality(concat_wav_list(wavlist), expected)
