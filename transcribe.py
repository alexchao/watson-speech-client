# -*- coding: utf-8 -*-
import argparse
import urllib
import requests

import private


API_BASE_URI = 'https://stream.watsonplatform.net/speech-to-text/api'
ENDPOINT_RECOGNIZE = '/v1/recognize'


CHUNK_SIZE = 1024


# assume `continuous=true` to force transcribing the entire audio stream
def make_recognize_uri():
    return ''.join([
        API_BASE_URI,
        ENDPOINT_RECOGNIZE,
        '?',
        'continuous=true'
    ])


def stream_file(file_path):
    with open(file_path, 'rb') as f:
        data = f.read(CHUNK_SIZE)
        while data:
            yield data
            data = f.read(CHUNK_SIZE)


def transcribe(file_path):
    uri = make_recognize_uri()
    auth = requests.auth.HTTPBasicAuth(private.USERNAME, private.PASSWORD)
    headers = {
        'Content-Type': 'audio/flac',
        'Transfer-Encoding': 'chunked'
    }
    r = requests.post(
        uri,
        auth=auth,
        headers=headers,
        data=stream_file(file_path),
    )
    print(r.text)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', help='Path to audio file.')
    args = parser.parse_args()
    transcribe(args.file_path)
