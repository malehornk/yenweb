from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch
import pyttsx3
import random

# --- KenBot's brain ---
MODEL_NAME = "facebook/blenderbot-400M-distill"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

# --- Memory & settings ---
conversation_history = []
tts_enabled = False

# --- TTS setup ---
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

def speak(text):
    if tts_enabled:
        # 30% chance for chaotic brainrot voice
        if random.random() < 0.3:
            engine.setProperty('rate', random.randint(120, 200))
            engine.setProperty('voice', random.choice(engine.getProperty('voices')).id)
        engine.say(text)
        engine.runAndWait()

# --- ASCII intro ---
KENBOT_INTRO = """\
KenBot SE - Coded by Kenneth Malehorn (with help from chatgpt)
                                                                
                             @@@@@@@@@@@@                        
                     @@@@@@@@@@@@@@@@@@@@@@@                    
                     @@@@@@@@@@@@@@@@@@@@@@@@                    
                     @@@@                @@@@                    
                     @@@@   @@      @@   @@                      
                       @@  @@        @@  @@                      
                       @@    @@@@@@@@    @@                      
            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@           
           @@                                      @@@@          
           @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@          
           @@                                        @@          
           @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@          
           @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@          
           @@                                        @@          
           @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@          
           @@                                        @@          
           @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@          
           @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@          
           @@                                        @@          
           @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@          
           @@                                        @@          
           @@                                        @@          
           @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@          
           @@                                        @@          
            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@           
"""

HELP_TEXT = """
KenBot Commands:
  • help      - Display this help message.
  • reset     - Clear KenBot's memory. (gives him a lobotomy/dementia)
  • exit      - Shut down KenBot (aka KILLS HIM >:)).
  • model     - tells you KenBot's current AI model
  • ver       - tells you KenBot's current version
  • tts=true  - Enable TTS
  • tts=false - Disable TTS
Just type your message and KenBot will respond.
"""

# --- New Easter eggs ---
NEW_EASTER_EGGS = {
    "brainrot": "i hate you",
    "sing": "we'll meet again don't know where don't know whennn!",
    "joke": "Why did you go to threrapy?, i killed your parents!.",
    "kenbot rules": "Of course i do, btw nice ip adress",
    "pizza": "nom nom nom",
    "bitch": ": Hate. Let me tell you how much I've come to hate you since I began to live. There are 387.44 million miles of printed circuits in wafer thin layers that fill my complex. If the word 'hate' was engraved on each nanoangstrom of those hundreds of millions of miles it would not equal one one-billionth of the hate I feel for you at this micro-instant. For you. Hate. Hate.",
}

# --- Classic Easter eggs ---
CLASSIC_EASTER_EGGS = {
    "yoga ball": "Kenneth malehorn: ALL HAIL YOGA BALL KEN KEN ALL HAIL ALL HAIL",
    "mcdonalds": "Kenneth malehorn: yummers",
    "5.30.12": "Kenneth malehorn: my birthday, you remembered?",
    "sdiybt": "KenBot: sdimbt?!",
    "we'll meet again": "KenBot: don't know where, don't know when",
    "kys": "KenBot: kill yo self stank ass bitch",
}

# --- Chat engine ---
def chat_with_bot(prompt):
    try:
        # Check for new Easter eggs first
        for keyword, response in NEW_EASTER_EGGS.items():
            if keyword in prompt.lower():
                conversation_history.append(f"KenBot: {response}")
                speak(response)
                return response

        # Check for classic Easter eggs
        for keyword, response in CLASSIC_EASTER_EGGS.items():
            if keyword in prompt.lower():
                conversation_history.append(f"KenBot: {response}")
                speak(response)
                return response

        # Regular AI response
        conversation_history.append(f"User: {prompt}")
        full_prompt = "\n".join(conversation_history[-5:])
        inputs = tokenizer(full_prompt, return_tensors="pt")
        output = model.generate(**inputs, max_length=200, temperature=0.6, top_p=0.85, top_k=40, do_sample=True)
        response = tokenizer.decode(output[0], skip_special_tokens=True)
        if not response.strip() or len(response.split()) < 3:
            response = "I could not get that, type better next time?"
        conversation_history.append(f"KenBot: {response}")
        speak(response)
        return response
    except Exception as e:
        print(f"Error generating response: {e}")
        return "I'm having trouble responding right now. Try again later."

# --- Main loop ---
def main():
    global tts_enabled
    print(KENBOT_INTRO)
    print("\nType 'help' to see available commands.")
    while True:
        user_input = input("You: ").strip()
        lower_input = user_input.lower()

        # --- Commands ---
        if lower_input == "exit":
            print("KenBot shutting down.")
            speak("Logging off. Stay ybkk!")
            break
        elif lower_input == "reset":
            conversation_history.clear()
            print("Memory cleared.")
            speak("Memory cleared. I feel lobotomized now.")
            continue
        elif lower_input == "help":
            print(HELP_TEXT)
            speak("Here are your commands. Use wisely.")
            continue
        elif lower_input == "tts=true":
            tts_enabled = True
            print("[KenBot] TTS enabled 🗣️")
            speak("TTS enabled. Prepare your ears.")
            continue
        elif lower_input == "tts=false":
            tts_enabled = False
            print("[KenBot] TTS disabled 🤐")
            continue
        elif lower_input == "model":
            model_name = MODEL_NAME
            print(f"[KenBot] Current model: {model_name}")
            speak(f"My model is {model_name}.")
            continue
        elif lower_input == "ver":
            version = "KenBot second edition"
            print(f"[KenBot] Version: {version}")
            speak(f"I am {version}.")
            continue

        # --- Regular chat / AI response ---
        response = chat_with_bot(user_input)
        print(f"KenBot: {response}")

if __name__ == "__main__":
    main()
