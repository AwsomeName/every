import pyttsx3

text = "今天天气很好，晴朗"
pyttsx3.speak(text)
exit()

engine = pyttsx3.init()
engine.setProperty("voice", 'zh')

rate = engine.getProperty("rate")
engine.setProperty("rate", rate - 50)

engine.say(text)
engine.runAndWait()


