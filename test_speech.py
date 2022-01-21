# Import the required module for text  
# to speech conversion
import pyttsx3
  
# init function to get an engine instance for the speech synthesis 
def test_1():
    engine = pyttsx3.init()
    
    # say method on the engine that passing input text to be spoken
    engine.say("Python speech Test 1!")
    
    # run and wait method, it processes the voice commands. 
    engine.runAndWait()

def test_2(text):

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        print(voice, voice.id)
        engine.setProperty('voice', voice.id)
        engine.say(text)
        engine.runAndWait()
        engine.stop()

def test_3(text,voice_id,rate,volume):
    engine = pyttsx3.init()
    engine.setProperty('voice', voice_id)
    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)
    engine.say(text)
    engine.runAndWait()
    engine.stop()
    

if __name__ == "__main__":
    test_1()
     
    test_2('OpenCV (Open Source Computer Vision Library) is an open-source computer vision and machine learning software library. OpenCV was built to provide a common infrastructure for computer vision applications and to accelerate the use of machine perception in commercial products.')
    
    test_text = "Test 2\nlife before death, hope before despair, journey before destination"
    rate = 170
    voice_id ='HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'
    
    test_3(test_text,voice_id,rate,1)
  