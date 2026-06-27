from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summaries import summarize,generate_title
from core.extractor import extract_action_items,extract_key_decisions,extract_questions
import os 
from dotenv import load_dotenv
load_dotenv()

source = "https://www.youtube.com/watch?v=QEnR7F7OtVc"
language = "english"

chunks = process_input(source)

transcript = transcribe_all(chunks,language=language)

print("TESTTTT")
print(transcript)

title = generate_title(transcript)
summary = summarize(transcript)

print('**********************************SUMMARY*************************')
print( f"Tittle ==>{title}" )
print(f"SUMMARYY ==> {summary}")

print("************************************************")
action_item = extract_action_items(transcript)
decision = extract_key_decisions(transcript)
questions = extract_questions(transcript)

print("ACTIONSSSSSSS")
print(action_item)
print("DECISIONSSSS")
print(decision)
print("QUESTIONSSSS")
print(questions)