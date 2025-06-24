#!/bin/zsh
echo "Starting FastAPI server on all interfaces..."

source ~/miniconda3/bin/activate

conda activate speech-text-translator

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
