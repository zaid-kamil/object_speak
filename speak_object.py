from distutils.util import execute
import pyttsx3

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


if __name__ == "__main__":
    engine = setup()
    engine.say('OpenCV (Open Source Computer Vision Library) is an open-source computer vision and machine learning software library. OpenCV was built to provide a common infrastructure for computer vision applications and to accelerate the use of machine perception in commercial products.')
    engine.runAndWait()
    engine.stop()
