import pyttsx3
import threading
import queue

def setup(rate=170, volume=1):
    engine = pyttsx3.init()
    try:
        voice_id ='HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'
        engine.setProperty('voice', voice_id)
    except:
        voices = engine.getProperty('voices') 
        engine.setProperty('voice',voices[1].id)
    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)
    return engine

class TTSThread(threading.Thread):
    def __init__(self, queue, rate=170, volume=1):
        threading.Thread.__init__(self)
        self.queue = queue
        self.daemon = True
        self.rate =rate
        self.volume = volume
        self.start()

    def run(self):
        tts_engine = pyttsx3.init()
        try:
            voice_id ='HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'
            tts_engine.setProperty('voice', voice_id)
        except:
            voices = engine.getProperty('voices') 
            tts_engine.setProperty('voice',voices[1].id)
        tts_engine.setProperty('rate', self.rate)
        tts_engine.setProperty('volume', self.volume)
        tts_engine.startLoop(False)
        t_running = True
        while t_running:
            if self.queue.empty():
                tts_engine.iterate()
            else:
                data = self.queue.get()
                if data == "exit":
                    t_running = False
                else:
                    tts_engine.say(data)
        tts_engine.endLoop()


if __name__ == "__main__":
    engine = setup()
    engine.say('OpenCV (Open Source Computer Vision Library) is an open-source computer vision and machine learning software library. OpenCV was built to provide a common infrastructure for computer vision applications and to accelerate the use of machine perception in commercial products.')
    engine.runAndWait()
    engine.stop()
