import io
import os

from flask import Blueprint, request, send_file
from kikiutils.file import del_file, get_file_mime, read_file, save_file
from kikiutils.string import random_str


home_api = Blueprint('home_api', __name__)


@home_api.post('/convert')
def convert_video():
    if not (video_file := request.files.get('file')):
        return '', 422

    file_data = video_file.stream.read()
    file_mime = get_file_mime(file_data)

    # Create tmp file
    tmp_filename = f'{random_str(128, 128)}.{file_mime[1]}'
    tmp_filepath = f'./files/{tmp_filename}'

    if not save_file(file_data, tmp_filepath, False):
        return '', 500

    # Create result filepath
    result_filename = f'{random_str(128, 128)}.mp4'
    result_filepath = f'./files/tmp/{result_filename}'

    # Convert video
    os.system(f'ffmpeg -i {tmp_filepath} -c:v libx264 -c:a aac {result_filepath}')

    # Read result file
    result_filedata = read_file(result_filepath)
    del_file(tmp_filepath)
    del_file(result_filepath)
    return send_file(io.BytesIO(result_filedata), 'video/mp4')
