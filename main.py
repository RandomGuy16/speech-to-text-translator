from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from os import unlink
import googletrans as gtrans
import whisper
import tempfile
import shutil


app = FastAPI()
# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# load the whisper model at startup
model = whisper.load_model("base")


def translate_text(text, target_language='de'):
    translator = gtrans.Translator()
    translated = translator.translate(text=text, dest=target_language)

    idioma_detectado = translated.src
    nombre_origen = gtrans.LANGUAGES.get(idioma_detectado, "desconocido").capitalize()
    nombre_destino = gtrans.LANGUAGES.get(target_language, "desconocido").capitalize()

    print(f"🌐 Idioma detectado: {nombre_origen} ({idioma_detectado})")
    print(f"🌐 Traducido al: {nombre_destino} ({target_language})")

    return translated.text


@app.post("/translate/audio")
async def transcribe_audio(file: UploadFile = File(...), target: str='en'):
    try:
        # Create a temporary file to store the uploaded audio
        with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as temp_file:
            # copy the uploaded binary audio to a temporary file
            shutil.copyfileobj(file.file, temp_file)
            temp_path = temp_file.name

        # transcribe the audio
        result = model.transcribe(audio=temp_path)

        # clean the temporary file
        unlink(temp_path)

        translated_text = translate_text(result["text"], target)

        return {
            "translated": translated_text,
            "target": target
        }

    except Exception as e:
        print(e)
        return {"error": str(e)}

    finally:
        file.file.close()


class TextRequest(BaseModel):
    text: str
    target: str = "en"

@app.post("/translate/text")
def transcribe_text(req: TextRequest):
    try:
        return {
            "translated": translate_text(req.text, req.target),
            "target": req.target
        }
    except Exception as e:
        return {"error": str(e)}
