import speech_recognition as sr
import whisper

#recognizer = sr.Recognizer()
#with sr.Microphone() as source:
#    recognizer.adjust_for_ambient_noise(source=source)
#    print("speak")
#    audio = recognizer.listen(source)
#    print("done")

#with open("grabacion.wav", "wb") as f:
#    f.write(audio.get_wav_data())

model = whisper.load_model("base")
#result = model.transcribe(audio="grabacion.wav")
result2 = model.transcribe(audio="whatsaudio1.wav")
result3 = model.transcribe(audio="whatsaudio2.wav")
#print(f'result: {result["text"]}')
print(f'result2: {result2["text"]}')
print(f'result3: {result3["text"]}')

