
import pyttsx4
import speech_recognition as sr
# import openai  # free trial finished Apr 2023 - cannot use


class Avatar():
    '''
        # Avatar Class - this class is responsible for speaking and listening.

        # It can be imported into another Class that needs this functionality

        # Need to pre-install: pyttsx4, SpeechRecognition
        # add the following to end of pip install if you have SSL VERIFY errors
        #--trusted-host pypi.org --trusted-host files.pythonhosted.org

    '''
    name = "Mr Lai"
    useSR = True

    def __init__(self,name=None, useSR=True,vix=1):
        if name:
            self.name = name
        # self.initOpenAI()
        self.useSR = useSR
        self.__initVoice(vix)
        self.__initSR()

    # def initOpenAI(self):
    #     openai.api_key= "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"

    def __initVoice(self,vix=2):
        '''
        Method: Initialise Text to Speech
        '''
        self.__engine = pyttsx4.init()
        self.__voices = self.__engine.getProperty('voices')
        self.__vix = vix
        self.__rate = 250
        self.__voice = self.__voices[self.__vix].id
        self.__engine.setProperty('voice', self.__voice)
        self.__engine.setProperty('rate', self.__rate)
        self.__engine.setProperty('volume', 1.0)

    def __initSR(self):
        self.sample_rate = 48000
        self.chunk_size = 2048
        self.r = sr.Recognizer()
        #self.useSR = True  # set this to True if using Speech Recognition


    def introduce(self,person=None,show=True):
        if person:
            self.say(f"Hello {person.getName()}, my name is {self.getName()}",show=show)
        else:
            self.say(f"Hello, my name is {self.name}",show=show)

    def say(self, words, show=True, rate=None):
        if show:
            print(f"{words} ")
        if rate:
            self.__engine.setProperty('rate', rate)
        self.__engine.say(words, self.name)
        self.__engine.runAndWait()

        self.__engine.setProperty('rate', self.__rate)


    def listen(self,prompt, useSR=None, show=True):

        if useSR:
            self.useSR = useSR

        words = ""
        if self.useSR:
            try:
                with sr.Microphone(sample_rate=self.sample_rate, chunk_size=self.chunk_size) as source:
                    # listen for 1 second to calibrate the energy threshold for ambient noise levels
                    self.r.adjust_for_ambient_noise(source)
                    self.say(prompt,show)
                    audio = self.r.listen(source, timeout=5,phrase_time_limit=3)
                try:
                    print("Ok. Trying to understand what you just said...please wait.")
                    #print("You said: '" + r.recognize_google(audio)+"'")
                    words = self.r.recognize_google(audio,language ="en-US")

                except sr.UnknownValueError:
                    self.say("Could not understand what you said.",show)
                except sr.RequestError as e:
                    self.say(f"Could not request results; {e}",show)

            except Exception as e:
                print(f"Error listening:'{e}'. ")
                self.say(prompt,show)
                words = input("Please type your response:> ")
        else:
            #print("No SR")
            self.say(prompt,show=True)
            words = input(">")
        return words


#     # Uses OPENAI - but free use has expired
#     def listenAI(self,prompt, useSR=None, show=True):

#         if useSR:
#             self.useSR = useSR

#         words = ""
#         if self.useSR:
#             try:
#                 with sr.Microphone(sample_rate=self.sample_rate, chunk_size=self.chunk_size) as source:
#                     # listen for 1 second to calibrate the energy threshold for ambient noise levels
#                     self.r.adjust_for_ambient_noise(source)
#                     self.say(prompt,show)
#                     audio = self.r.listen(source, timeout=3)
#                     # write audio to file for openai
#                     with open("speech.wav", "wb") as audio_file:
#                         audio_file.write(audio.get_wav_data())
#                 try:
#                     #print("You said: '" + r.recognize_google(audio)+"'")
# #                    words = self.r.recognize_google(audio,language ="en-US")
#                     with open("speech.wav", "rb") as audio_file:
#                         words = openai.Audio.transcribe("whisper-1", audio_file)  # API has expired

#                 except sr.UnknownValueError:
#                     self.say("Could not understand what you said.",show)
#                 except sr.RequestError as e:
#                     self.say(f"Could not request results; {e}",show)

#             except Exception as e:
#                 print(f"Error listening:'{e}'. ")
#                 self.say(prompt,show)
#                 words = input(f"Please type your response:> ")
#         else:
#             #print("No SR")
#             self.say(prompt,show=True)
#             words = input(f">")
#         return words

    def getName(self):
        return self.name
#
# This is code to TEST DRIVER our Avatar Class
#
def main():
    george = Avatar("george")
    george.say(george.listen("speak"))

# def dummy():
#     bob = Avatar("bob")

#     bob.introduce()
#     george.introduce(bob)
#     george.say(f"You just said: {george.listen('How are you?')}")

if __name__ == "__main__":
    main()