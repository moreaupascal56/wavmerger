# WavMerger: `.wav` file merger

This is a library to concatenate (merge) `.wav` files. 
For example if you used the google text-to-speech API on several `.txt`, resulting into several `.wav` files and you want to concatenate everything into a single (big) `.wav` file

It was originally made because of a small use-case I had.

If anybody want to use it or suggest a new use case by adding features feel free to open an issue, it would be a pleasure to answer! 

## Use cases

### Merge all `.wav` files from a directory

To merge all `.wav` file from a directory, use the [concat_wav_in_dir](./wavmerger/wavmerger.py) function. 

Example from the tests: 
There is several `.wav` files in [tests/integration/data/PinkPanther30/splitted](tests/integration/data/PinkPanther30/splitted) directory. In order to merge them to a single file do:

```python
from wavmerger import concat_wav_in_dir

concat_wav_in_dir(
    dirpath = "tests/integration/data/PinkPanther30/splitted",
    write_file_name = "YOUR-OUTPUT-FILE-NAME",
    write_file_dir = "YOUR-OUTPUT-FILE-DIR",
)
```


