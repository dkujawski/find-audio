import argparse
import speech_recognition as sr


def transcribe(audio_file):

    # Create a recognizer instance
    r = sr.Recognizer()

    # Open the audio file (or use microphone as source)
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source, duration=30)  # Read the entire audio file
        while audio:
            # Perform speech recognition using Google Web Speech API
            try:
                text = r.recognize_google(audio)
                print("Transcription: " + text)
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
            except Exception as e:
                print(e)
                break
            audio = r.record(source, duration=30)  # Read the entire audio file

def main():
    parser = argparse.ArgumentParser(description="Transcribe audio file")
    parser.add_argument("target", type=str, help="Path to a target audio file or directory.")
    
    args = parser.parse_args()
    transcribe(args.target)

if __name__ == "__main__":
    main()

