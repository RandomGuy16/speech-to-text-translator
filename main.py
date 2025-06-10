import speech_recognition as sr
from textblob import TextBlob
import googletrans as gtrans

# recognizes voice
def transcribe_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("🎤 Habla ahora...")

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=10)
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


async def translate_text(translator, target):
    return await translator.translate(text=target.raw, dest='de')


async def analyze_feeling(text):
    translator = gtrans.Translator()

    blob = TextBlob(text)
    print(await translate_text(translator, blob.raw))
    sentiment = blob.sentiment.polarity

    if sentiment > 0.1:
        estado = "Positivo 😀"
    elif sentiment < -0.1:
        estado = "Negativo 😠"
    else:
        estado = "Neutral 😐"

    print(f"\n📊 Sentimiento: {estado} (polarity={sentiment:.2f})")

# === MAIN PROGRAM ===
def main():
    text = transcribe_speech()
    if text:
        analyze_feeling(text)


if __name__ == '__main__':
    main()

