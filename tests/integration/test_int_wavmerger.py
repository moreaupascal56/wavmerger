from pathlib import Path

import pytest

from tests.helpers import WavFileEquality
from wavmerger import WavFile, merge_wav_in_dir


@pytest.fixture
def get_wav_test_data() -> tuple[Path, Path]:
    """Return the test data path. The test data is an original .wav file and the same file
    splitted in several files in the splitted/ directory.

    Returns:
        tuple[Path,Path]: (original .wav path, directory containingthe splitted .wav files)
    """
    dirpath = Path(__file__).parent.joinpath("data").joinpath("PinkPanther30")
    return (dirpath.joinpath("PinkPanther30.wav"), dirpath.joinpath("splitted"))


@pytest.mark.filterwarnings(
    "ignore"
)  # A warning is raised because of the way the test data is created, let's ignore it
def test_merge_wav_in_dir(get_wav_test_data, temp_dir):
    """Tests merge_wav_in_dir function

    Args:
        get_wav_test_data (_type_): fixture
        temp_dir (_type_): fixture
    """

    write_file_name = "output_test_merge_wav_in_dir.wav"
    original_data_path, splitted_data_path = get_wav_test_data

    merge_wav_in_dir(
        dirpath=splitted_data_path,
        write_file_name=write_file_name,
        write_file_dir=temp_dir,
    )

    created_wav = Path(temp_dir).joinpath(write_file_name)

    WavFileEquality(
        WavFile(filepath=created_wav),
        WavFile(filepath=original_data_path),
    )
    assert created_wav.is_file()
