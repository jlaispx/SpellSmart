'''
    pip install openai
    pip install sounddevice
    pip install scipy
'''

import archive.openaiSR as openaiSR
import sounddevice as sd
from scipy.io.wavfile import write

class Avatar:

    def __init__(self):
