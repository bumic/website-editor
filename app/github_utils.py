import ujson
import base64
import requests
from dotenv import load_dotenv
import os

load_dotenv()


def update_file(filename, github_path):
    # Get current SHA
    res = requests.get(github_path)
    sha = ujson.loads(res.text)['sha']

    with open(filename, 'rb') as f:
        js_text = f.readlines()[0]  # JS should all be on a single line

    base64_bytes = base64.b64encode(js_text)
    base64_string = base64_bytes.decode('utf-8')

    return requests.put(
        github_path,
        headers={"Authorization": "token " + os.getenv("GITHUB_ACCESS_TOKEN")},
        json={
            "message": "Data Update",
            "committer": {
                "name": "Devin de Hueck",
                "email": "d.dehueck@gmail.com"
            },
            "content": base64_string,
            "sha": sha
    })
