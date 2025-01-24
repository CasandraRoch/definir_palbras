import pyttsx3
import speech_recognition as sr
from nltk.corpus import wordnet

# Function to recognize voice
def recognize_voice(prompt):
    r = sr.Recognizer()
    with sr.Microphone(device_index=0) as source:
        print(prompt)
        audio = r.listen(source, phrase_time_limit=5)
        try:
            text = r.recognize_google(audio, language='en-UK')
            print("You said: {}".format(text))
            return text
        except sr.UnknownValueError:
            print("Could not understand the audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None

# Function to play a message using pyttsx3 with voice settings
def play_message(message):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    voices = engine.getProperty('voices')
    
    # Set voice and rate properties
    engine.setProperty('voice', voices[1].id)  
    engine.setProperty('rate', rate - 50)  
    
    engine.say(message)
    engine.runAndWait()

# Function to get word definition from WordNet
def get_word_definition(word):
    # Find synsets for the word
    synsets = wordnet.synsets(word)
    
    # Check if any synsets were found
    if synsets:
        # Get the first definition from the first synset
        definition = synsets[0].definition()
        return definition
    else:
        return "No definition found for the word."

# Main function to ask for name, greet the user, ask for a word, and provide its definition
def main():
    # Ask for the user's name
    play_message("Hello, my name is Aletza. Please tell me your name.")
    name = recognize_voice("Speak your name now: ")
    
    if name:
        # Greet the user with their name
        greeting = f"Hello {name}, how are you today?"
        play_message(greeting)
        
        continue_program = True
        
        while continue_program:
            # Ask for a word to define
            play_message("Please tell me a word you would like to define.")
            word = recognize_voice("Speak the word now: ")
            
            if word:
                # Get the definition of the word
                definition = get_word_definition(word)
                
                # Confirm the word and provide its definition
                confirmation = f"Thank you, {name}. The word you want to define is '{word}'. Here is the definition: {definition}"
                play_message(confirmation)
                
                # Ask if the user wants to define another word
                play_message("Would you like to define another word? Please say 'yes' or 'no'.")
                answer = recognize_voice("Speak 'yes' or 'no' now: ")
                
                if answer and answer.lower() in ['yes', 'yeah', 'yep']:
                    continue_program = True
                else:
                    play_message("Thank you for using the word definition service. Goodbye!")
                    continue_program = False
            else:
                play_message("I did not understand the word, please try again.")
    else:
        play_message("I did not understand your name, please try again later.")

# Call the main function
main()
