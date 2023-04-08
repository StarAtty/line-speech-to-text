# LINE Speech to Text
This is a minimal self-hosted LINE bot using OpenAI's Whisper to transcribe audio messages to text. It runs on Flask and use Gunicorn as WSGI server.
Change `initial_prompt` to fit your need (language, puctuation, names, etc.)

## Setup
```
pip install flask openai-whisper gunicorn
```
Grab your Channel secret and Channel access token, than replace the placeholders in `line_stt.py`.

## Run
```
gunicorn wsgi:app
```
