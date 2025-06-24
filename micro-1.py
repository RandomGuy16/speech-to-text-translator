# ========== INSTALADOR SEGURO ==========
import importlib.util
import subprocess
import sys
import os
import datetime

def instalar_librerias():
    requeridas = {
        "speech_recognition": "speechrecognition",
        "textblob": "textblob",
        "googletrans": "googletrans==4.0.0-rc1",
        "qrcode": "qrcode",  # Puedes eliminar esta línea si no usarás más QR
        "docx": "python-docx",
        "pyaudio": "pyaudio",
        "PIL": "pillow"
    }
    for modulo, paquete in requeridas.items():
        if importlib.util.find_spec(modulo) is None:
            print(f"Instalando {paquete}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", paquete])

instalar_librerias()

# ========== IMPORTACIONES ==========
import speech_recognition as sr
from textblob import TextBlob
import googletrans as gtrans
from googletrans import LANGUAGES
import asyncio
from docx import Document


# ========== UTILS ==========
def timestamp():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


# ========== FUNCIONES ==========
def transcribe_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("🎙️ Habla ahora...")

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    print("✅ Audio capturado")

    try:
        text = recognizer.recognize_google(audio, language="es-ES")
        print(f"📝 Texto detectado: {text}")
        return text
    except sr.UnknownValueError:
        print("❌ No se entendió el audio.")
        return None
    except sr.RequestError:
        print("❌ Error con el servicio de reconocimiento.")
        return None


async def translate_text(text, target_language='de'):
    translator = gtrans.Translator()
    translated = translator.translate(text=text, dest=target_language)
    
    idioma_detectado = translated.src
    nombre_origen = LANGUAGES.get(idioma_detectado, "desconocido").capitalize()
    nombre_destino = LANGUAGES.get(target_language, "desconocido").capitalize()
    
    print(f"🌐 Idioma detectado: {nombre_origen} ({idioma_detectado})")
    print(f"🌐 Traducido al: {nombre_destino} ({target_language})")
    
    return translated.text


async def traducir_archivo_docx(ruta, idioma_destino='de'):
    try:
        if not os.path.exists(ruta):
            print("❌ Archivo no encontrado.")
            return

        doc = Document(ruta)
        texto = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        if texto:
            print(f"\n📄 Texto extraído:\n{texto}")
            traduccion = await translate_text(texto, idioma_destino)
            print(f"\n🌐 Traducción:\n{traduccion}")
        else:
            print("⚠️ El archivo está vacío.")
    except Exception as e:
        print(f"❌ Error al traducir archivo Word: {e}")


async def analizar_entrada_voz(idioma_destino='de'):
    texto = transcribe_speech()
    if not texto:
        return

    traduccion = await translate_text(texto, idioma_destino)
    print(f"🌍 Traducción al {idioma_destino}:\n{traduccion}")


async def traducir_texto_manual(texto, idioma_destino='de'):
    traduccion = await translate_text(texto, idioma_destino)
    print(f"🌍 Traducción:\n{traduccion}")


# ========== MAIN ==========
async def main():
    print("\n=== MENÚ DE TRADUCCIÓN ===")
    print("1. Traducir desde voz")
    print("2. Traducir archivo Word (.docx)")
    print("3. Traducir texto manual")
    opcion = input("Elige una opción (1-3): ")

    if opcion == "1":
        await analizar_entrada_voz("de")
    elif opcion == "2":
        ruta = input("Nombre del archivo Word (.docx): ")
        await traducir_archivo_docx(ruta, "de")
    elif opcion == "3":
        texto = input("Escribe el texto a traducir: ")
        await traducir_texto_manual(texto, "de")
    else:
        print("❌ Opción no válida.")

if __name__ == '__main__':
    asyncio.run(main())
