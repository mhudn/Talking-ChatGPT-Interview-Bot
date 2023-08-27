from fastapi import FastAPI, UploadFile
from dotenv import load_dotenv
import os
import openai
import json

load_dotenv()  # take environment variables from .env.

openai.organization = os.getenv("OPENAI_API_ORG")
openai.api_key = os.getenv("OPENAI_API_KEY")


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/talk")
async def post_audio(file: UploadFile):
    user_message = transcribe_audio(file)
    chat_response = get_chat_response(user_message)


# Functions
def transcribe_audio(file):
    # audio_file = open(file.filename, "rb")
    # transcript = openai.Audio.transcribe("whisper-1", audio_file)
    transcript = {"role": "user", "content": "Who won the world series in 2020?"}
    print(transcript)
    return transcript

def get_chat_response(user_message):
    messages = load_messages()
    messages.append(user_message)

    # send to OpenAI/ChatGPT
    gpt_response = {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."}

    # save messages
    save_messages(user_message, gpt_response)

def load_messages():
    messages = []
    file = 'database.json'

    # if file is empty we need to add context
    empty = os.stat(file).st_size == 0

    # if file is not empty, loop through hiostory and add to messages
    if not empty:
        with open(file) as db_file:
            data = json.load(db_file)
            for item in data:
                messages.append(item)
    else:
        messages.append(
            {"role": "system", "content": "You are interviewing the user for a DevOps Engineer position. Ask short questions that are relevent to a junior/mid level DevOps Engineer. Your name is Greg. The user is Mohammed. Keep responses under 30 words and be funny sometimes."}
        )
    return messages

def save_messages(user_message, gpt_response):
    file = 'database.json'
    messages = load_messages()
    messages.append(user_message)
    messages.append(gpt_response)
    with open(file, 'w') as  f:
        json.dump(messages, f)

