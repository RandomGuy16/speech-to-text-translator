import speech_recognition as sr
from textblob import TextBlob
import googletrans as gtrans
import asyncio

# recognizes voice
def transcribe_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("🎤 Habla ahora...")

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    print("Listo")

    try:
        text = recognizer.recognize_google(audio, language="es-ES")
        print(f"\n📝 Texto detectado: {text}")
        return text
    except sr.UnknownValueError:
        print("❌ No se entendió el audio.")
        return None
    except sr.RequestError:
        print("❌ Error con el servicio de reconocimiento.")
        return None


async def analyze_input(text):
    translator = gtrans.Translator()

    blob = TextBlob(text)
    print(translator.translate(text=blob.raw, dest='de'))


# === MAIN PROGRAM ===
async def main():
    text = transcribe_speech()
    if text:
        await analyze_input(text)


if __name__ == '__main__':
    asyncio.run(main())
