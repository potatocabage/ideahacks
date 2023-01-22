from flask import Flask, json, request, render_template
from flask_sock import Sock
from flask_cors import CORS, cross_origin
import os
import torch
import zipfile
import torchaudio
from glob import glob
import numpy as np
from scipy.io.wavfile import write
from textblob import TextBlob

SAMPLE_RATE = 400
projects = [{"id": 1, "name": "Demo One"},
            {"id": 2, "name": "Demo Two"}]

datasets = [{"id": 1, "name": "dataset1"},
            {"id": 2, "name": "dataset2"}]

data_stream = []

api = Flask(__name__)
sock = Sock(api)
cors = CORS(api)
api.config['CORS_HEADERS'] = 'Content-Type'
api.config["UPLOAD_DIR"] = "data"
device = torch.device('cpu')
model, decoder, utils = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                       model='silero_stt',
                                       language='en',  # also available 'de', 'es'
                                       device=device)
(read_batch, split_into_batches,
 read_audio, prepare_model_input) = utils


@api.route('/result', methods=['GET'])
@cross_origin()
async def get_result():
    await write("speech.wav", SAMPLE_RATE, np.array(data_stream))
    batches = split_into_batches(["speech.wav"], batch_size=10)
    input = prepare_model_input(read_batch(batches[0]),
                                device=device)
    output = model(input)
    text = TextBlob(decoder(output[0]))
    text = text.correct()
    return text


@api.route('/speech', methods=['POST'])
@cross_origin()
def post_speech(sock):
    # audio = request.files['file']
    # audio.save(os.path.join(api.config["UPLOAD_DIR"], "audio"))
    # print("audio saved")
    while True:
        data = sock.receive()
        data_stream.append(data)
    return 0


@api.route('/test', methods=['GET', 'POST'])
@cross_origin()
def test_post():
    # audio = request.files['file']
    # audio.save(os.path.join(api.config["UPLOAD_DIR"], "audio"))
    # print("audio saved")
    print(request.data)
    return 0


if __name__ == '__main__':
    api.run(host="0.0.0.0", port=5500)
