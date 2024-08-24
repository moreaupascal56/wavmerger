from numpy.testing import assert_array_equal

from wavmerger import WavFile


def WavFileEquality(wav: WavFile, expected: WavFile | dict):
    """ "An equality test for WavFiles

    Args:
        wav (WavFile): WavFile to test
        expected (WavFile | dict): expected values as a dict or WavFile
    """
    d = wav.to_dict()

    if not isinstance(expected, dict):
        expected = expected.to_dict()

    assert d["rate"] == expected["rate"]
    assert d["duration"] == expected["duration"]
    assert_array_equal(d["data"], expected["data"])
    assert d.keys() == expected.keys()
