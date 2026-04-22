import urllib.request
import json
req = urllib.request.Request("http://127.0.0.1:8080/decrypt",
    data=b'{"private_key": "", "ciphertext_base64": "A", "wrapped_key_base64": "B", "nonce_base64": "C"}',
    headers={"Content-Type": "application/json"})
try:
    urllib.request.urlopen(req)
    print("Success")
except urllib.error.HTTPError as e:
    print(f"Error {e.code}: {e.read().decode('utf-8')}")
except Exception as e:
    print(e)
