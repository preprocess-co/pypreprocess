# Preprocess SDK ![V1.4.3](https://img.shields.io/badge/Version-1.4.3-333.svg?labelColor=eee) ![MIT License](https://img.shields.io/badge/License-MIT-333.svg?labelColor=eee)

[Preprocess](https://preprocess.co) is an API service that splits any kind of document into optimal chunks of text for use in language model tasks.
Given documents in input `Preprocess` splits them into chunks of text that respect the layout and semantics of the original document.
We split the content by taking into account sections, paragraphs, lists, images, data tables, text tables, and slides, and following the content semantics for long texts.
We support:
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
Alternatively, if you want to add it as a dependency with poetry: 
```bash
poetry add pypreprocess
poetry install
```

**You need a `Preprocess API Key` to use the SDK, to get one please reach out to [support@preprocess.co](mailto:support@preprocess.co) asking for an API key.**

## Getting started
Get the chunks from a file for use in your language model tasks.

```python
from pypreprocess import Preprocess

#init the SDK with a file
preprocess = Preprocess(api_key=YOUR_API_KEY, filepath="path/for/file")

#chunk the file
preprocess.chunk()
preprocess.wait()

#get the result
result = preprocess.result()
for i in result.data['chunks']:
    #use chunks

```


## Initialise a connection
You can initialize the SDK in 3 ways.

1- Passing a local `filepath`

_when you want to init the SDK to chunk a local file_
```python
from pypreprocess import Preprocess
preprocess = Preprocess(api_key=YOUR_API_KEY, filepath="path/for/file")
```

2- Passing a `process_id`

_when the chunking process starts `Preprocess` generate a process_id, you can use it to instance the SDK_
```python
from pypreprocess import Preprocess
preprocess = Preprocess(api_key=YOUR_API_KEY, process_id="id_of_the_process")
```

3- Passing a `PreprocessResponse` Object

_When you need to store the result of a chunking process permanently, you can later load them in the SDK via a PreprocessResponse object_
```python
import json
from pypreprocess import Preprocess, ProcessResponse
response = PreprocessResponse(**json.loads("The JSON result from calling chunk before."))
preprocess = Preprocess(api_key=YOUR_API_KEY, process=PreprocessResponse)
```

## Chunking options
We support a few options you can configure to get the best result for your ingestion pipeline.

> **Preprocess tries to output chunks of less than 512 tokens. Sometimes longer chunks can be produced to preserve the content integrity. We are currently working to allow you to set an arbitrary chunk token length, stay tuned.**


| Parameter | Type     | Default |Description                |
| :-------- | :------- | :------- | :------------------------- |
| `merge` | `bool` | False | If `True` small paragraphs will be merged to maximize chunk length |
| `repeat_title` | `bool` |  False | If `True` each chunk will start with the title of the section in which is contained |
| `repeat_table_header` | `bool` |  False | If `True` each chunk will start with the header of the table in which is contained |
| `table_output_format` | `enum ['text', 'markdown', 'html']` |  `'text'` | Return tables in the format you need for your ingestion pipelines |
| `keep_header` | `bool` | True | If set to `False`, the content of the headers will be removed. Headers may include page numbers, document titles, section titles, paragraph titles, and fixed layout elements. |
| `smart_header` | `bool` | True | If set to `True`, only relevant titles will be included in the chunks, while other information will be removed. Relevant titles are those that should be part of the body of the page as a title. If set to `False`, only the keep_header parameter will be considered. If keep_header is `False`, the smart_header parameter will be ignored. |
| `keep_footer` | `bool` | False | If set to `True`, the content of the footers will be included in the chunks. Footers may include page numbers, footnotes, and fixed layout elements. |
| `image_text` | `bool` | False | If set to `True`, the text contained in the images will be added to the chunks. |

You can pass each parameter from those during the SDK initialization
```python 
preprocess = Preprocess(api_key=YOUR_API_KEY, filepath="path/for/file", merge=True, repeat_title=True, ...)
```

Or set them later with the `set_options` method using a `dict` 
```python
preprocess.set_options({"merge": True, "repeat_title": True, ...})
```


## Chunk
After initing the SDK with a `filepath` you should call the `chunk()` method.

```python
from pypreprocess import Preprocess
preprocess = Preprocess(api_key=YOUR_API_KEY, filepath="path/for/file")
response = preprocess.chunk()
```
the response contains the `process_id` and details about the success of the API call.


## Getting the results
The conversion and chunking process may take a while.
You can use the built-in `wait()` method to wait and get the result as the process finishes.
```python
result = preprocess.wait()
print(result.data['chunks'])
```

In a more complex scenario, you can store the `process_id` after initiating the chunking process and then use it in a different flow.
```python
#initing the chunking process
from pypreprocess import Preprocess
preprocess = Preprocess(api_key=YOUR_API_KEY, filepath="path/for/file")
preprocess.chunk()
preocess_id = preprocess.get_process_id()

#in a different flow
from pypreprocess import Preprocess
preprocess = Preprocess(api_key=YOUR_API_KEY, process_id=process_id)
result = preprocess.wait()
print(result.data['chunks'])
```

If you want to implement a different logic for getting the result you can use the method `result()` and check if the status if it's `FINISHED`.
```python
result = preprocess.result()
if result.data['process']['status'] == "FINISHED": 
   print(result.data['chunks'])
```


## Other methods
Here is a list of some methods inside the SDK that may help you
- `set_filepath(path)` setting the file path after initializing the object.
- `set_process_id(id)` setting the process_id param by id.
- `set_process(PreprocessResponse)` setting the process_id param by `PreprocessResponse` object.
- `set_options(dict)` set the parameters for configuring chunking options.
- `to_json()` returning a JSON str representing the current object.
- `get_process_id()` returning the current process_id.
- `get_filepath()` returning the filepath.
- `get_options()` returning the current chunking options.