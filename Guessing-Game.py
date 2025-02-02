import tkinter as tk
from tkinter import messagebox
import urllib.request
import json
import random

# Game configuration
GUESS_LIMIT = 3

# Fallback list of words if the API fetch fails
FALLBACK_WORDS = ["cat", "dog", "apple", "python", "tree"]

def fetch_random_word():
    """
    Attempts to fetch a random word from a free public API using built-in urllib.
    If the API request fails, a word is randomly selected from the FALLBACK_WORDS list.
    Returns:
        str: The secret word in lowercase.
    """
    try:
        url = "https://random-word-api.herokuapp.com/word?number=1"
        with urllib.request.urlopen(url, timeout=5) as response:
            if response.status == 200:
                data = response.read()
                words = json.loads(data.decode('utf-8'))
                if isinstance(words, list) and len(words) > 0:
                    return words[0].lower()
    except Exception as e:
        print("API error:", e)
    fallback_word = random.choice(FALLBACK_WORDS)
    print("Falling back to local word list. Selected word:", fallback_word)
    return fallback_word.lower()

class WordGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Guessing Game")
        self.secret_word = fetch_random_word()
        self.guess_count = 0
        
        # Instruction label
        self.instruction_label = tk.Label(root, text=f"Guess the secret word! (You have {GUESS_LIMIT} guesses)")
        self.instruction_label.pack(pady=10)
        
        # Entry for user guess
        self.guess_entry = tk.Entry(root, font=("Arial", 14))
        self.guess_entry.pack(pady=5)
        self.guess_entry.bind("<Return>", self.process_guess)  # Press Enter to submit
        
        # Submit button
        self.submit_button = tk.Button(root, text="Submit Guess", command=self.process_guess)
        self.submit_button.pack(pady=5)
        
        # Feedback label for messages
        self.feedback_label = tk.Label(root, text="", font=("Arial", 12))
        self.feedback_label.pack(pady=10)
        
        # Reset button to start a new game, initially disabled
        self.reset_button = tk.Button(root, text="Reset Game", command=self.reset_game, state=tk.DISABLED)
        self.reset_button.pack(pady=5)
    
    def process_guess(self, event=None):
        """
        Handles the user's guess submission. Updates the guess count,
        checks the guess against the secret word, and provides feedback.
        """
        guess = self.guess_entry.get().strip().lower()
        if not guess:
            messagebox.showwarning("Input Error", "Please enter a guess.")
            return
        
        self.guess_count += 1
        
        if guess == self.secret_word:
            self.feedback_label.config(text="Congratulations! You guessed correctly!")
            self.end_game(win=True)
        else:
            if self.guess_count < GUESS_LIMIT:
                remaining = GUESS_LIMIT - self.guess_count
                self.feedback_label.config(text=f"Incorrect guess. You have {remaining} guess{'es' if remaining > 1 else ''} left.")
            else:
                self.feedback_label.config(text=f"Out of guesses! The correct word was '{self.secret_word}'.")
                self.end_game(win=False)
        
        # Clear the entry widget for the next guess
        self.guess_entry.delete(0, tk.END)
    
    def end_game(self, win):
        """
        Ends the game by disabling input and enabling the reset button.
        Displays a message box with the result.
        """
        self.guess_entry.config(state=tk.DISABLED)
        self.submit_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.NORMAL)
        if win:
            messagebox.showinfo("Game Over", "You Win!")
        else:
            messagebox.showinfo("Game Over", "Out of Guesses, YOU LOSE!")
    
    def reset_game(self):
        """
        Resets the game state: fetches a new word, resets the guess count,
        clears feedback, and re-enables input.
        """
        self.secret_word = fetch_random_word()
        self.guess_count = 0
        self.feedback_label.config(text=f"New game started! Guess the word. (You have {GUESS_LIMIT} guesses)")
        self.guess_entry.config(state=tk.NORMAL)
        self.submit_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.DISABLED)
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus()

if __name__ == "__main__":
    # Create the main window and run the game
    root = tk.Tk()
    game = WordGuessingGame(root)
    root.mainloop()
