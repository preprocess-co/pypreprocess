# Preprocess SDK
_**This is a repository for sdk for preprocess that will be used to interact with the system.**_

## Initialise a connection
>First, you should have an api key to use it, otherwise you'll not be allowed to connect/interact with preprocess system
To get an api key, feel free to send a request to [Support](mailto:support@preprocess.co) asking for an api key.

```
1- preprocess = Preprocess(api_key=YOUR_API_KEY, filepath="path/for/file")
2- preprocess = Preprocess(api_key=YOUR_API_KEY, process_id="id_of_the_process")
3- preprocess = Preprocess(api_key=YOUR_API_KEY, process=ProcessResponse)
```

## Chunk
>Here you have to pass the filepath then call chunk method for chunking and it'll return to you a ProcessResponse object containing all info you'll need.

```
1- response = preprocess.chunk()
```

## Getting the results
>You can directly call one of those methods that'll be listed to get the result after getting a success chunk call, or whenever you want call them after initialise the Preprocess object with either `process_id` or `process` which is a PreprocessResponse object, and the result will be always a PreprocessResponse containing the chunks inside data parameter.

- If you want to wait until it finish use `wait()` method
    ```
    1, 2 and 3- result = preprocess.wait()
    - print(result.data['chunks'])
    ```
- If you don't want to wait consider calling `result()` and check the status if it's not FINISHED or OK, so it's still chunking.
    ```
    1, 2 and 3- result = preprocess.result()
    - if result.status in ["FINISHED", "OK"]: 
    -   print(result.data['chunks'])
    ```
## Other methods
>This part will containing some existing function may help you 

- `set_filepath(path)` setting the file path after initialise the object.
- `set_process_id(id)` setting the process_id param by id.
- `set_process(process)` setting the process_id param by PrepreocessResponse object.
- `set_info(dict)` info for handle the chunking based on your needs.
- `to_json()` returning a json str representing the current object.