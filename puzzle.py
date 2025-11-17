from dataclasses import dataclass
from typing import List, Dict
import random


@dataclass
class Puzzle:
    """Represents a single puzzle in the escape room game."""
    puzzle_id: str
    type: str  # 'riddle', 'math', 'word', 'cipher'
    question: str
    answer: str
    hints: List[str]
    solved: bool = False
    attempts: int = 0


class Puzzle_Generator_Agent:
    """An agent that creates different puzzle types, ensuring that they are solvable."""
    
    def __init__(self):
        self.puzzle_counter = 0

    def load_puzzle_templates(self) -> Dict:
        """Load hand-crafted puzzle templates."""
        return {
            'riddles': [
                {
                    'question': "I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?",
                    'answer': "echo",
                    'hints': [
                        "Think about sounds that bounce back to you.",
                        "It's a phenomenon that occurs in caves and canyons.",
                        "It's the repetition of sound caused by reflection."
                    ]
                },
                {
                    'question': "The more you take, the more you leave behind. What am I?",
                    'answer': "footsteps",
                    'hints': [
                        "Think about walking.",
                        "You create these as you move.",
                        "They're impressions left on the ground."
                    ]
                },
                {
                    'question': "I have cities, but no houses. I have mountains, but no trees. I have water, but no fish. What am I?",
                    'answer': "map",
                    'hints': [
                        "It's a representation of something larger.",
                        "You use it for navigation.",
                        "It's usually made of paper and shows geography."
                    ]
                }
            ],
            'ciphers': [
                {
                    'plaintext': "ESCAPE",
                    'shift': 3,
                    'hints': [
                        "The letters have been shifted in the alphabet.",
                        "It's a Caesar cipher with a shift of 3.",
                        "Each letter moved forward by 3 positions: E→H, S→V, etc."
                    ]
                },
                {
                    'plaintext': "FREEDOM",
                    'shift': 5,
                    'hints': [
                        "This is a substitution cipher.",
                        "The shift is 5 positions in the alphabet.",
                        "Try moving each letter 5 positions back."
                    ]
                }
            ]
        }
    
    def generate_riddle(self) -> Puzzle:
        """Generate a riddle puzzle from templates."""
        riddle = random.choice(self.load_puzzle_templates()['riddles'])
        self.puzzle_counter += 1
        
        return Puzzle(
            puzzle_id=f"puzzle_{self.puzzle_counter}",
            type="riddle",
            question=riddle['question'],
            answer=riddle['answer'].lower(),
            hints=riddle['hints']
        )
    
    def generate_cipher(self) -> Puzzle:
        """Generate a cipher puzzle from templates."""
        cipher = random.choice(self.load_puzzle_templates()['ciphers'])
        self.puzzle_counter += 1
        
        # Simple Caesar cipher encoding
        encoded = ''.join(
            chr((ord(char) - 65 + cipher['shift']) % 26 + 65) if char.isupper() else
            chr((ord(char) - 97 + cipher['shift']) % 26 + 97) if char.islower() else char
            for char in cipher['plaintext']
        )
        
        return Puzzle(
            puzzle_id=f"puzzle_{self.puzzle_counter}",
            type="cipher",
            question=f"Decode this message: {encoded}\n(Hint: It's a Caesar cipher)",
            answer=cipher['plaintext'].lower(),
            hints=cipher['hints']
        )
    
    def generate_math_problem(self) -> Puzzle:
        """Generate a simple math problem."""
        a, b = random.randint(1, 20), random.randint(1, 20)
        operation = random.choice(['+', '-', '*'])
        if operation == '+':
            question = f"What is {a} + {b}?"
            answer = str(a + b)
        elif operation == '-':
            question = f"What is {a} - {b}?"
            answer = str(a - b)
        else:
            question = f"What is {a} * {b}?"
            answer = str(a * b)
        
        self.puzzle_counter += 1
        
        return Puzzle(
            puzzle_id=f"puzzle_{self.puzzle_counter}",
            type="math",
            question=question,
            answer=answer,
            hints=[
                f"Try calculating {a} {operation} {b} step by step.",
                f"Use basic arithmetic rules for {operation}.",
                f"The answer is {answer}."
            ]
        )
    
    def generate_word_puzzle(self) -> Puzzle:
        """Generate a simple word puzzle (e.g., anagram)."""
        words = ["listen", "triangle", "conversation", "astronomer", "schoolmaster"]
        word = random.choice(words)
        anagram = ''.join(random.sample(word, len(word)))
        
        # Make sure it's actually scrambled
        while anagram == word:
            anagram = ''.join(random.sample(word, len(word)))
        
        self.puzzle_counter += 1
        
        return Puzzle(
            puzzle_id=f"puzzle_{self.puzzle_counter}",
            type="word",
            question=f"Unscramble this word: {anagram}",
            answer=word,
            hints=[
                f"Look for common prefixes or suffixes in English words.",
                f"The word has {len(word)} letters.",
                f"The first letter is '{word[0]}'."
            ]
        )
    
    def generate_puzzle(self, puzzle_type: str = None) -> Puzzle:
        """Generate a puzzle of the specified type, or random if None."""
        if puzzle_type is None:
            puzzle_type = random.choice(['riddle', 'math', 'word', 'cipher'])
        
        generators = {
            'riddle': self.generate_riddle,
            'math': self.generate_math_problem,
            'word': self.generate_word_puzzle,
            'cipher': self.generate_cipher
        }
        
        return generators[puzzle_type]()
        
    def validate_puzzle(self, puzzle: Puzzle) -> bool:
        """Validate that the puzzle is solvable."""
        return (
            puzzle.question and 
            puzzle.answer and 
            len(puzzle.hints) > 0
        )


class PuzzleManager:
    """
    Game State Manager Agent: Manages the generation, validation, and tracking of puzzles.
    """
    
    def __init__(self):
        self.generator_agent = Puzzle_Generator_Agent()
    
    def create_puzzle(self, puzzle_type: str = None) -> Puzzle:
        """Create and validate a puzzle of the specified type."""
        puzzle = self.generator_agent.generate_puzzle(puzzle_type)
        if self.generator_agent.validate_puzzle(puzzle):
            return puzzle
        else:
            raise ValueError("Generated puzzle is invalid")
    
    def check_answer(self, puzzle: Puzzle, user_answer: str) -> bool:
        """Check if the user's answer is correct."""
        return user_answer.lower().strip() == puzzle.answer.lower().strip()
    
    def track_progress(self, puzzle: Puzzle, user_answer: str) -> bool:
        """
        Track progress by checking answer and updating puzzle state.
        Returns True if correct, False otherwise.
        """
        puzzle.attempts += 1
        
        if self.check_answer(puzzle, user_answer):
            puzzle.solved = True
            return True
        return False


class Hint_Agent:
    """
    Hint Master Agent: Provides escalating hints after repeated wrong attempts.
    """
    
    def __init__(self):
        self.hint_thresholds = [1, 3, 4]  # Attempts after which hints are given
    
    def should_provide_hint(self, attempts: int) -> bool:
        """Determine if a hint should be provided based on attempt count."""
        return attempts in self.hint_thresholds
    
    def provide_hint(self, puzzle: Puzzle) -> str:
        """
        Provide a hint based on the number of attempts.
        Returns the hint text or a message if no hints available.
        """
        if not self.should_provide_hint(puzzle.attempts):
            return "No hints available at this time."
        
        # Map attempts to hint index
        hint_index = self.hint_thresholds.index(puzzle.attempts)
        
        if hint_index < len(puzzle.hints):
            return puzzle.hints[hint_index]
        
        return "No more hints available."


class Narrator_Agent:
    """
    Narrator Agent: Provides immersive storytelling and reacts to player progress.
    """
    
    def opening_story(self) -> str:
        """Generate the opening story for the escape room."""
        return """
════════════════════════════════════════════════════════════════
                    WELCOME TO THE ESCAPE ROOM                  
                                                                
  You awaken in a dimly lit chamber, ancient stone walls       
  surrounding you. The air is thick with mystery and dust.     
  Strange inscriptions cover every surface, and a single       
  massive door - your only exit - stands sealed before you.    
                                                                
  A voice echoes from nowhere: "Only the wise may leave.       
  Solve the trials, and the door shall open. Fail, and         
  remain here forever..."                                      
                                                                
  The heavy door behind you slams shut with a loud CLANG.       
  Your journey begins now...                                    
════════════════════════════════════════════════════════════════
"""

    def intro_story(self, puzzle: Puzzle, puzzle_number: int, total_puzzles: int) -> str:
        """Generate an introductory story for the puzzle."""
        stage_descriptions = [
            "You approach the first sealed door. A stone pedestal rises before you with an inscription.",
            "Behind the first door lies another chamber. An ancient artifact hovers in the air, surrounded by runes.",
            "You press deeper into the temple. A massive gate blocks your path, its mechanism a complex puzzle.",
            "The chamber shifts around you. New symbols appear, glowing with an otherworldly light.",
            "You reach the final chamber. This is the ultimate test before freedom."
        ]
        
        description = stage_descriptions[min(puzzle_number - 1, len(stage_descriptions) - 1)]
        return f"""
─ CHALLENGE {puzzle_number}/{total_puzzles} ─────────────────────────────────
                                                                             
 {description}                                                               
                                                                             
 PUZZLE: {puzzle.question}                                                
                                                                             
─────────────────────────────────────────────────────────────────────────────
"""

    def success_story(self, puzzle: Puzzle, puzzle_number: int, total_puzzles: int) -> str:
        """Generate a success story for solving the puzzle."""
        progress = int((puzzle_number / total_puzzles) * 100)
        success_messages = [
            "The stone glows brightly and the first door swings open!",
            "The runes burst with light! You've unlocked the second chamber!",
            "The massive gate groans and slowly begins to open!",
            "The ancient mechanism clicks into place! Another barrier falls!",
            "The final seal breaks! Light floods through the opening door!"
        ]
        
        message = success_messages[min(puzzle_number - 1, len(success_messages) - 1)]
        
        return f"""
════════════════════════════════════════════════════════════════
                      ✓ PUZZLE SOLVED! ✓                      
                                                                
  {message}                                                     
                                                                
  Progress: {progress}% complete [{puzzle_number}/{total_puzzles}]
  The correct answer was: "{puzzle.answer.upper()}"          
                                                                
════════════════════════════════════════════════════════════════
"""

    def failure_story(self, puzzle: Puzzle, puzzle_number: int, total_puzzles: int) -> str:
        """Generate a failure story for failing to solve the puzzle."""
        return f"""
════════════════════════════════════════════════════════════════
                      ✗ PUZZLE FAILED ✗                                                                                      
  You've exhausted all your attempts. The mechanism remains     
  locked, and the chamber begins to shift ominously.            
  Dark shadows creep across the walls as your hope fades...     
                                                                
  Challenge: {puzzle_number}/{total_puzzles}                    
  The answer was: "{puzzle.answer.upper()}"                  
                                                                
              YOU HAVE BEEN TRAPPED IN THE CHAMBER...           
                      GAME OVER                                 
                                                                
════════════════════════════════════════════════════════════════
"""
    
    def hint_story(self, puzzle: Puzzle, hint: str, attempt: int) -> str:
        """Generate a story element for providing a hint."""
        hint_sources = [
            "A mysterious voice whispers",
            "Ancient engravings on the wall reveal",
            "An ethereal light shows you"
        ]
        source = hint_sources[min(attempt - 1, len(hint_sources) - 1)]
        
        return f"""
💡 HINT #{attempt}:
   {source}: "{hint}"
"""
    
    def game_over_story(self, puzzles: List[Puzzle]) -> str:
        """Generate a game over story based on whether all puzzles were solved."""
        if all(puzzle.solved for puzzle in puzzles):
            return """
════════════════════════════════════════════════════════════════
                   ✓ CONGRATULATIONS! ✓                       
                                                                
  You have solved all the puzzles and broken the ancient curse! 
  The final door swings open wide, and brilliant sunlight       
  floods into the chamber, washing away centuries of darkness.  
                                                                
  As you step through to freedom, you hear the voice again:     
  "Well done, traveler. You have proven yourself worthy.        
   The temple releases you from its grasp. Go forth, and        
   carry this wisdom with you..."                               
                                                                
  ✓ YOU HAVE ESCAPED! ✓                                         
                                                                
════════════════════════════════════════════════════════════════
"""
        else:
            return """
════════════════════════════════════════════════════════════════
                     GAME OVER - YOU ARE TRAPPED                
                                                                
  The temple's ancient magic proves too powerful. As the        
  chamber grows darker, you sink to the cold stone floor.       
  Your adventure ends here, in the depths of the forgotten      
  temple. Perhaps another brave soul will succeed where you     
  have failed...                                                
                                                                
════════════════════════════════════════════════════════════════
"""
        
    def narrate_progress(self, progress: Dict) -> str:
        """Narrate the user's progress through the puzzles."""
        percentage = int((progress['solved'] / progress['total']) * 100) if progress['total'] > 0 else 0
        bar_length = 20
        filled = int((percentage / 100) * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        return f"\nProgress: [{bar}] {percentage}% - {progress['solved']}/{progress['total']} puzzles solved\n"


class EscapeRoomGame:
    """
    Main orchestrator that coordinates all agents and manages game flow.
    """

    def __init__(self):
        self.puzzle_manager = PuzzleManager()
        self.hint_agent = Hint_Agent()
        self.narrator_agent = Narrator_Agent()
        self.puzzles: List[Puzzle] = []

    def start_game(self, num_puzzles: int = 5):
        """Start the escape room game by displaying the opening story."""
        print(self.narrator_agent.opening_story())
        self.num_puzzles = num_puzzles

    def attempt_puzzle(self, puzzle: Puzzle, user_answer: str, puzzle_number: int, total_puzzles: int) -> bool:
        """
        Handle a user's attempt to solve a puzzle.
        Returns True if correct, False otherwise.
        """
        if self.puzzle_manager.track_progress(puzzle, user_answer):
            success_story = self.narrator_agent.success_story(puzzle, puzzle_number, total_puzzles)
            print(success_story)
            return True
        else:
            # Check if we should provide a hint
            hint = self.hint_agent.provide_hint(puzzle)
            if hint != "No hints available at this time.":
                hint_story = self.narrator_agent.hint_story(puzzle, hint, puzzle.attempts)
                print(hint_story)
            else:
                print("Incorrect answer. Try again!\n")
            return False

    def end_game(self):
        """End the game and provide a final summary."""
        game_over_story = self.narrator_agent.game_over_story(self.puzzles)
        print(game_over_story)
        progress = {
            'solved': sum(1 for p in self.puzzles if p.solved),
            'total': len(self.puzzles)
        }
        progress_narration = self.narrator_agent.narrate_progress(progress)
        print(progress_narration)


def main():
    """Main entry point for the template-based escape room game."""
    print("\n" + "="*70)
    print("       ESCAPE ROOM - TEMPLATE-BASED VERSION")
    print("="*70 + "\n")
    
    try:
        num_puzzles_input = input("How many puzzles would you like to solve? (1-10, default: 3): ").strip()
        num_puzzles = int(num_puzzles_input) if num_puzzles_input else 3
        num_puzzles = max(1, min(num_puzzles, 10))  # Clamp between 1-10
    except ValueError:
        num_puzzles = 3
        print("Invalid input. Using default: 3 puzzles\n")
    
    game = EscapeRoomGame()
    game.start_game(num_puzzles=num_puzzles)

    max_attempts = 5
    
    try:
        for puzzle_idx in range(1, num_puzzles + 1):
            puzzle = game.puzzle_manager.create_puzzle()
            game.puzzles.append(puzzle)
            intro = game.narrator_agent.intro_story(puzzle, puzzle_idx, num_puzzles)
            print(intro)
            
            attempts = 0
            solved = False
            
            while attempts < max_attempts and not solved:
                attempts += 1
                remaining = max_attempts - attempts
                user_answer = input(f"Your answer (Attempt {attempts}/{max_attempts}): ").strip()
                
                if not user_answer:
                    print("Please enter an answer.\n")
                    attempts -= 1  # Don't count empty answers
                    continue
                
                if game.attempt_puzzle(puzzle, user_answer, puzzle_idx, num_puzzles):
                    solved = True
                elif remaining > 0:
                    print(f"Attempts remaining: {remaining}\n")
                else:
                    print("No attempts remaining.\n")
            
            if not solved:
                print(game.narrator_agent.failure_story(puzzle, puzzle_idx, num_puzzles))
                break
        
        if solved:
            game.end_game()
    
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Goodbye!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")


if __name__ == "__main__":
    main()