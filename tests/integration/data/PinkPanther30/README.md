This data have been created using Audacity markers and export multiple files option. 
This results in the warning below when executing tests:

```

tests/integration/test_int_wavmerger.py::test_merge_wav_in_dir
  /home/pascal/Documents/github/wavsurfer/wavmerger/wavmerger.py:21: WavFileWarning: Chunk (non-data) not understood, skipping it.
    self.rate, self.data = wavfile.read(filepath)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html

```

Please ignore it.