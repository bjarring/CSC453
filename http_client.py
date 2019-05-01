import requests
from requests_toolbelt import MultipartEncoder

addr = 'https://iot-sleep-analysis.mybluemix.net/'
test_url = addr + '/upload'

m = MultipartEncoder(fields={'image': ('image.jpg', open('test.jpg', 'rb'))})

# prepare headers for http request
content_type = 'image/jpeg'
headers = {'content-type': m.content_type}

# send http request with image and receive response
response = requests.post(test_url, data=m, headers=headers)
# decode response
print(response.text)
