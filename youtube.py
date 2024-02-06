from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command

from pytube import YouTube
import os
import uuid

def dowload_video(url, type='audio'):

    yt = YouTube(url)

    print(f'Название: {yt.title}')
    print(f'Продолжительность: {yt.length} сек')
    print(f'Размер: {yt.streams.get_highest_resolution().filesize / 1024 ** 2:.2f} мб')

    audio_id = uuid.uuid4().fields[-1]
    if type == 'audio':
        yt.streams.get_highest_resolution().download(r'audio', f'{audio_id}.mp3')
        return f"{audio_id}.mp3"
    elif type == 'video':
        yt.streams.get_highest_resolution().download(r'audio', f'{audio_id}.mp4')
        return f"{audio_id}.mp4"
