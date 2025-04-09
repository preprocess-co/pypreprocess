# Preprocess SDK ![V1.5](https://img.shields.io/badge/Version-1.5-333.svg?labelColor=eee) ![MIT License](https://img.shields.io/badge/License-MIT-333.svg?labelColor=eee)

[Preprocess](https://preprocess.co) is an API service that splits various types of documents into optimal chunks of text for use in language model tasks. It divides documents into chunks that respect the layout and semantics of the original content, accounting for sections, paragraphs, lists, images, data tables, text tables, and slides.

We support the following formats:
- PDFs
- Microsoft Office documents (Word, PowerPoint, Excel) 
- OpenOffice documents (ODS, ODT, ODP)
- HTML content (web pages, articles, emails)
- Plain text

## Installation
To install the Python `Preprocess` library, use:
```bash
pip install pypreprocess
```
Alternatively, to add it as a dependency with Poetry: 
```bash
poetry add pypreprocess
poetry install
```

**Note: You need a `Preprocess API Key` to use the SDK. To obtain one, please contact [support@preprocess.co](mailto:support@preprocess.co).**

## Getting Started
Retrieve chunks from a file for use in your language model tasks:

```python
from pypreprocess import Preprocess

# Initialize the SDK with a file
preprocess = Preprocess(api_key=YOUR_API_KEY, filepath="path/for/file")

# Chunk the file
preprocess.chunk()
preprocess.wait()

# Get the result
result = preprocess.result()
for chunk in result.data['chunks']:
    # Use the chunks
```

## Initialization Options
You can initialize the SDK in three different ways:

1- **Passing a local `filepath`:**

_Use this when you want to chunk a local file:_
```python
from pypreprocess import Preprocess
preprocess = Preprocess(api_key=YOUR_API_KEY, filepath="path/for/file")
```

2- **Passing a `process_id`:**

_When the chunking process starts, `Preprocess` generates a `process_id` that can be used to initialize the SDK later:_
```python
from pypreprocess import Preprocess
preprocess = Preprocess(api_key=YOUR_API_KEY, process_id="id_of_the_process")
```

3- **Passing a `PreprocessResponse` Object:**

_When you need to store and reload the result of a chunking process later, you can use the `PreprocessResponse` object:_
```python
import json
from pypreprocess import Preprocess, PreprocessResponse
response = PreprocessResponse(**json.loads("The JSON result from a previous chunking process."))
preprocess = Preprocess(api_key=YOUR_API_KEY, process=response)
```

## Chunking Options
Preprocess offers several configuration options to tailor the chunking process to your needs.

> **Note: Preprocess attempts to output chunks with less than 512 tokens. Longer chunks may sometimes be produced to preserve content integrity. We are currently working to allow user-defined chunk lengths.**

| Parameter | Type     | Default |Description                |
| :-------- | :------- | :------- | :------------------------- |
| `merge` | `bool` | False | If `True` small paragraphs will be merged to maximize chunk length. |
| `repeat_title` | `bool` |  False | If `True` each chunk will start with the title of the section it belongs to. |
| `repeat_table_header` | `bool` |  False | If `True`, each chunk that contains part of a table will include the table header. |
| `table_output_format` | `enum ['text', 'markdown', 'html']` |  `'text'` | Output table format. |
| `keep_header` | `bool` | True | If set to `False`, the content of the headers will be removed. Headers may include page numbers, document titles, section titles, paragraph titles, and fixed layout elements. |
| `smart_header` | `bool` | True | If set to `True`, only relevant headers will be included in the chunks, while other information will be removed. Relevant headers are those that should be part of the body of the page as a section/paragraph title. If set to `False`, only the `keep_header` parameter will be considered. If keep_header is `False`, the `smart_header` parameter will be ignored. |
| `keep_footer` | `bool` | False | If set to `True`, the content of the footers will be included in the chunks. Footers may include page numbers, footnotes, and fixed layout elements. |
| `image_text` | `bool` | False | If set to `True`, the text contained in the images will be added to the chunks. |


You can pass these parameters during SDK initialization:
```python 
preprocess = Preprocess(api_key=YOUR_API_KEY, filepath="path/for/file", merge=True, repeat_title=True, ...)
preprocess = Preprocess(api_key=YOUR_API_KEY, filepath="path/for/file", options={"merge": True, "repeat_title": True, ...})
```

Or, set them later using the `set_options` method with a `dict`:
```python
preprocess.set_options({"merge": True, "repeat_title": True, ...})
preprocess.set_options(merge=True, repeat_title=True, ...)
```
> **Note: if the parameter is present inside options dictionary, it will override the parameter passed in the function.**

## Chunking Files
After initializing the SDK with a `filepath`, use the `chunk()` method to start chunking the file:
```python
from pypreprocess import Preprocess
preprocess = Preprocess(api_key=YOUR_API_KEY, filepath="path/for/file")
response = preprocess.chunk()
```
The response contains the `process_id` and details about the API call's success.

## Retrieving Results
The chunking process may take some time. You can wait for completion using the `wait()` method:
```python
result = preprocess.wait()
print(result.data['chunks'])
```

In more complex workflows, store the `process_id` and retrieve the result later:
```python
# Start chunking process
preprocess = Preprocess(api_key=YOUR_API_KEY, filepath="path/for/file")
preprocess.chunk()
process_id = preprocess.get_process_id()

# In a different flow
preprocess = Preprocess(api_key=YOUR_API_KEY, process_id=process_id)
result = preprocess.wait()
print(result.data['chunks'])
```

Alternatively, use the `result()` method to check if the process is complete:
```python
result = preprocess.result()
if result.data['process']['status'] == "FINISHED": 
    print(result.data['chunks'])
```

## Other Useful Methods
Here are additional methods available in the SDK:

- `set_filepath(path)`: Set the file path after initialization.
- `set_process_id(id)`: Set the `process_id` parameter by ID.
- `set_process(PreprocessResponse)`: Set the `process_id` using a `PreprocessResponse` object.
- `set_options(dict)`: Set chunking options using a dictionary.
- `to_json()`: Return a JSON string representing the current object.
- `get_process_id()`: Retrieve the current `process_id`.
- `get_filepath()`: Retrieve the file path.
- `get_options()`: Retrieve the current chunking options.