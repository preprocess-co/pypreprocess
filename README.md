[![Preprocess](https://playground.preprocess.co/try/logo_1.png)](https://preprocess.co)
# Preprocess SDK ![V1.2.0](https://img.shields.io/badge/Version-1.2.0-333.svg?labelColor=eee) ![MIT License](https://img.shields.io/badge/License-MIT-333.svg?labelColor=eee)

[Preprocess](https://preprocess.co) is an API service that splits any kind of document into optimal chunks of text for use in language model tasks.
Given documents in input `Preprocess` splits them into chunks of text that respect the layout and semantics of the original document.
We split the content by taking into account sections, paragraphs, lists, images, data tables, text tables, and slides, and following the content semantics for long texts.
We support 
- PDFs
- Microsoft Office documents (Word, PowerPoint, Excel) 
- OpenOffice documents (ods, odt, odp)
- HTML content (web pages, articles, emails)
- Plain text

## Installation
Install the Python `Preprocess` library if it is not already present:
```bash
pip install pypreprocess
```
Alternatively, if you want to add it as a depencancy with poetry: 
```bash
poetry add pypreprocess
poetry install
```


## Initialise a connection
First, you should have an api key to use it, otherwise you'll not be allowed to connect/interact with preprocess system
To get an api key, feel free to send a request to [Support](mailto:support@preprocess.co) asking for an api key.

There is a 3 ways to insitlaise the SDK

1- Passing a `filepath`
_here you are passing the file path that you want the system to chunk it_
```python
from pypreprocess import Preprocess
preprocess = Preprocess(api_key=YOUR_API_KEY, filepath="path/for/file")
```
2- Passing `process_id`
_here you already did a chunk before and already have the `process_id`, so you can pass it and the result will be loaded from this process_
```python
from pypreprocess import Preprocess
preprocess = Preprocess(api_key=YOUR_API_KEY, process_id="id_of_the_process")
```

3- Passing `ProcessResponse` Object
_here you already got a response from chunk, you can pass it totally to the SDK and the object will be inistialised with this process_id inside the response object_
```python
import json
from pypreprocess import Preprocess, ProcessResponse
response = ProcessResponse(**json.loads("The json result from calling chunk before."))
preprocess = Preprocess(api_key=YOUR_API_KEY, process=ProcessResponse)
```

## Chunk
Here you have to pass the filepath then call chunk method for chunking and it'll return to you a `ProcessResponse` object containing all info you'll need.

```python
response = preprocess.chunk()
```

## Getting the results
You can directly call one of those methods that'll be listed to get the result after getting a success chunk call, or whenever you want call them after initialise the Preprocess object with either `process_id` or `process` which is a PreprocessResponse object, and the result will be always a PreprocessResponse containing the chunks inside data parameter.

- If you want to wait until it finish use `wait()` method
    ```python
    result = preprocess.wait()
    print(result.data['chunks'])
    ```
- If you don't want to wait consider calling `result()` and check the status if it's not FINISHED, so it's still in chunking phase.
    ```python
    result = preprocess.result()
    if result.data['process']['status'] == "FINISHED": 
       print(result.data['chunks'])
    ```

## Extra configs based on your needs
We're supporting extra info to be set based on your needs to enhance the chunking as you want, you can pass it on initialise as parameters or pass them all as dict later
| Parameter | Type     | Default |Description                |
| :-------- | :------- | :------- | :------------------------- |
| `max` | `int` | 1500 |The maximum length of one chunk can be, and if it's maximum that this, it'll be split into smaller parapraphs |
| `min` | `int` | 250 |The minimum length of one chunk can be, and if it's minimum than this will be merged with next or previous paragraph |
| `merge` | `bool` | False | To allow the system merging the smaller paragraphs or not |
| `repeat_title` | `bool` |  False | To allow the system repeat the title to each chunk or not |
| `repeat_table_header` | `bool` |  False | To allow the system repeat the table's header to each section from this table in case this table is too long and has to be chunked |
| `table_output_format` | `enum ['text', 'markdown', 'html']` |  `'text'` | This related to the table output, `'text'` is retutning the table as normal text, `'markdown'` returning the table in markdown way or `'html'` and this returning the table in html format |

You can pass each parameter from those while initialisation like that 
```python 
preprocess = Preprocess(api_key=YOUR_API_KEY, filepath="path/for/file", merge=True, repeat_title=True, max=2000, ...)
```

Or pass it later with `set_info` method but you've to pass them as `dict` 
```python
preprocess.set_info({"merge": True, "repeat_title": True, "max": 2000, ...})
```

## Other methods
Here is a list of some methods inside the SDK that may help you
- `set_filepath(path)` setting the file path after initialise the object.
- `set_process_id(id)` setting the process_id param by id.
- `set_process(process)` setting the process_id param by `PrepreocessResponse` object.
- `set_info(dict)` info for handle the chunking based on your needs.
- `to_json()` returning a json str representing the current object.
- `get_process_id()` returning the current process_id.
- `get_filepath()` returning the filepath.
- `get_info()` returning the info.