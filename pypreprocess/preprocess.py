import os, requests, json, time
from urllib.parse import urlencode

from .preprocessresponse import PreprocessResponse

class Preprocess:
    def __init__(self, api_key, **kwargs) -> None:
        self._base_url = "https://api.preprocess.co/"

        if api_key is None or api_key == "":
            raise ValueError("Please provice an api key to be used while doing the auth with the system.")
        
        self._api_key = api_key
        self._headers = {
            'x-api-key': self._api_key
        }
        self._filepath = ""
        self._info = {}
        self._process_id = None
        self._response = None

        for key, value in kwargs.items():
            if key == "filepath": 
                self._filepath = value

            elif key == "process_id": 
                self._process_id = value

            elif key == "process" and isinstance(value, PreprocessResponse): 
                self._process_id = value.data["process"]["id"]

            elif key in ["merge", "max", "min", "min_min", "table_output", "repeat_title", "table_header", "lamguage"]:
                self._info[key] = value

        if self._filepath != "":
            if not os.path.exists(self._filepath):
                raise FileNotFoundError("Please provid an exist file, the proided path not exist.")
        
        check = self._post_request("check_connection", {})
        if check.status_code != 200:
            raise ConnectionError(f"The response code is: {check.status_code}, so please check your api key")
        elif check.status_code == 200:
            res = check.json()
            if res['status'] != "OK" or res['success'] != True:
                raise ConnectionError(f"There is error with the provided data, so please check your api key")

    def chunk(self) -> PreprocessResponse:
        if self._filepath == "":
            raise ValueError("Please provice path for file to be used.")
        
        file = {
            'file': (
                os.path.basename(self._filepath),
                open(self._filepath, 'rb')
            )
        }
        data = {}
        if self._info != {}:
            data = self._info

        request = self._post_request("chunk", data, file)

        if request.status_code != 200:
            raise ConnectionError(f"There is error with the provided data, so please check your api key")
        
        self._response = PreprocessResponse(**request.json())

        if self._response.status == "OK" and self._response.success:
            self._process_id = self._response.data["process"]["id"]

        return self._response

    def wait(self) -> PreprocessResponse:
        response = self.result()
        start_time = time.time()
        print(response)
        while not response.status in ["FINISHED", "OK"]:
            
            if time.time() - start_time > 300: 
                break

            time.sleep(15)
            response = self.result()
        
        if not response.status in ["FINISHED", "OK"]:
            raise TimeoutError("The waiting time is over 5 mins, please use result function to check the result later, or check your data in case something wrong.")
        
        return response

    def result(self) -> PreprocessResponse:
        if self._process_id in ["", None]:
            raise ValueError("Please make a successful chunk call first, or pass a process id")
        request = self._get_request('get_result', {"id": self._process_id})
        if request.status_code == 200:
            result = PreprocessResponse(**request.json())
            return result
        else:
            raise ConnectionError(f"The response code is: {request.status_code}, so please check your api key.")
        
    def set_process_id(self, id: str):
        if id in ["", None]:
            raise ValueError("Please provide a valid process id to use it.")
        self._process_id = id

    def set_process(self, process: PreprocessResponse):
        if process is None or process.data['process']['id'] in ["", None]:
            raise ValueError("Please provide a valid process to use it.")
        self._process_id = process.data['process']['id']

    def get_process_id(self):
        return self._process_id

    def set_filepath(self, filepath):
        if  filepath in ["", None]:
            raise ValueError("Please provice a file path to use it.")
        
        if not os.path.exists(filepath):
            raise FileNotFoundError("Please provid an exist file, the proided path not exist.")

        self._filepath = filepath
    
    def get_filepath(self):
        return self._filepath

    def set_info(self, **kwargs):
        for key, value in kwargs.items():
            if key in ["merge", "max", "min", "min_min", "table_output", "repeat_title", "table_header", "lamguage"]:
                self._info[key] = value

    def get_info(self):
        return self._info
    
    def to_json(self):
       return json.dumps(self, default=lambda o: o.__dict__)
    
    def __str__(self):
        return self.to_json()
    
    def _post_request(self, endpoint, data, file = None):
        url = self._base_url + endpoint
        if file != None:
            return requests.post(url, json=data, files=file, headers=self._headers, timeout=60)
        else:
            return requests.post(url, json=data, headers=self._headers, timeout=60)
    
    def _get_request(self, endpoint, data):
        url = self._base_url + endpoint
        data = urlencode(data)
        url += "?" + data
        return requests.get(url, headers=self._headers)