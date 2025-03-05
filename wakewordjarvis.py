import tkinter as tk
from RealtimeSTT import AudioToTextRecorder
import keyboard

# Global variable to store the last transcription
last_transcription = ""

def on_transcription_update(text):
    global last_transcription
    # Calculate the new part of the transcription by removing what was already transcribed
    new_text = text[len(last_transcription):].strip()
    if new_text:
        # Append only the new text to the text widget
        transcription_text.insert(tk.END, new_text + " ")
        transcription_text.see(tk.END)  # Scroll to the end automatically
        # Update the last transcription to the current full text
        last_transcription = text

def on_recording_start():
    global last_transcription
    # Reset the transcription at the start of recording
    last_transcription = ""
    transcription_text.insert(tk.END, "\nRecording started!\n")

def on_recording_stop():
    transcription_text.insert(tk.END, "\nRecording stopped.\n")

def check_for_quit():
    if keyboard.is_pressed('q'):
        recorder.stop()
        recorder.shutdown()
        root.quit()
    root.after(100, check_for_quit)  # Check every 100ms

if __name__ == '__main__':
    # Set up the GUI window
    root = tk.Tk()
    root.title("Speech-to-Text Transcription")

    # Create a text widget for displaying transcription
    transcription_text = tk.Text(root, wrap=tk.WORD)
    transcription_text.pack(expand=True, fill='both')

    # Initialize the recorder (adjust parameters as needed)
    recorder = AudioToTextRecorder(
        enable_realtime_transcription=True,
        on_realtime_transcription_update=on_transcription_update,
        on_recording_start=on_recording_start,
        on_recording_stop=on_recording_stop,
        device="cuda",  # Use "cpu" if CUDA is unavailable
        model="base"    # Adjust model size based on your setup
    )

    # Start recording
    recorder.start()

    # Check for 'q' key to stop the program
    root.after(100, check_for_quit)

    # Run the GUI event loop
    root.mainloop()