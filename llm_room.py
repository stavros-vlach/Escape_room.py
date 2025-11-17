from transformers import pipeline
import json
import re
from typing import Dict, List
from dataclasses import dataclass


pipe = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct-v0.2")

@dataclass
class PuzzleData:
    """Data structure for LLM-generated puzzles."""
    question: str
    answer: str
    hints: List[str]


def generate_text(prompt, max_new_tokens=1000, temperature=1.6):
    """
    Generate text based on the given prompt using the specified language model.

    Args:
        prompt (str): The input text prompt to generate text from.
        max_new_tokens (int): The maximum number of new tokens to generate.
        temperature (float): Controls randomness. Higher = more creative/random, Lower = more deterministic.
                           Range: 0.0 to 2.0

    Returns:
        str: The generated text.
    """

    result = pipe(prompt, max_new_tokens=max_new_tokens, num_return_sequences=1, 
                    truncation=True, do_sample=True, temperature=temperature, return_full_text=False)
    return result[0]['generated_text']
    

def generate_puzzles(num_puzzles=3):
    """
    Generate escape room puzzles using an LLM.
    
    Args:
        num_puzzles (int): Number of puzzles to generate.
    
    Returns:
        List[Dict]: List of puzzle dictionaries with question, answer, and hints.
    """
    prompt = f"""
    You are an expert escape room puzzle designer. Generate {num_puzzles} text-based puzzles for an ancient temple theme.

    CRITICAL REQUIREMENTS:
    - Puzzles must be completely solvable using ONLY the text provided in the question
    - NO references to physical objects, rooms, engravings, symbols, or images the player can see
    - NO phrases like "Find the...", "Look at...", "In this room...", or "The symbol shows..."
    - All information needed to solve must be included in the question text itself
    - Player is solving puzzles in a terminal with text only - no visual context

    PUZZLE TYPES (choose from these):
    1. Logic puzzles with all clues stated in the question
    2. Math puzzles with numbers provided in the question
    3. Word puzzles (anagrams, riddles) with complete information
    4. Pattern recognition with the pattern written out in text

    Each puzzle needs:
    - "question": A self-contained puzzle with all necessary information
    - "answer": The exact solution (one or two words maximum)
    - "hints": Array of 3 progressive hints using only information from the question

    GOOD EXAMPLES:
    {{"question": "Three temple guardians always tell the truth, lie, or alternate. Guardian A says 'I am a liar.' Guardian B says 'A is telling the truth.' Guardian C says 'B is a liar.' Who tells the truth?", "answer": "Guardian C", "hints": ["A cannot be a liar if saying they're a liar", "Consider what B claims about A", "Only C's statement is consistent"]}}

    {{"question": "The ancient code uses: 1=A, 2=B, 3=C, etc. Decode this message: 20-5-13-16-12-5", "answer": "TEMPLE", "hints": ["Convert each number to its letter position", "20 is the 20th letter of alphabet", "Put the letters together"]}}

    BAD EXAMPLES (avoid these):
    - "Find the symbol on the wall that matches..."
    - "Look at the hieroglyphs and count..."
    - "The door shows three numbers..."
    - "Examine the ancient tablet..."

    Generate exactly {num_puzzles} puzzles in JSON format.
    Return only valid JSON objects, one per line, without any additional text.
    Format: {{"question": "...", "answer": "...", "hints": ["...", "...", "..."]}}
"""

    print("Generating puzzles with LLM...\n")
    

    generated_text = generate_text(prompt, temperature=1.2, max_new_tokens=1500)
    
    json_pattern = r'\{[^{}]*"question"[^{}]*"answer"[^{}]*"hints"[^{}]*\}'
    matches = re.findall(json_pattern, generated_text, re.DOTALL)
    
    puzzles = []
    for match in matches:
        clean_match = match.rstrip(',').strip()
        puzzle = json.loads(clean_match)
        
        if 'question' in puzzle and 'answer' in puzzle and 'hints' in puzzle:
            if isinstance(puzzle['hints'], str):
                puzzle['hints'] = [puzzle['hints']]
            
            puzzles.append(puzzle)
            
            if len(puzzles) >= num_puzzles:
                break
    
    if len(puzzles) < num_puzzles:
        print(f"⚠️  Warning: Only generated {len(puzzles)} puzzles instead of {num_puzzles}")
        print("Filling with fallback puzzles...\n")
        
        # Fallback puzzles if LLM generation fails
        fallback_puzzles = [
            {
                "question": "I speak without a mouth and hear without ears. What am I?",
                "answer": "echo",
                "hints": ["Think about sound", "It bounces back", "Found in caves"]
            },
            {
                "question": "What has keys but no locks, space but no room, and you can enter but can't go inside?",
                "answer": "keyboard",
                "hints": ["It's an input device", "You use it for typing", "On every computer"]
            },
            {
                "question": "If 2+3=10, 8+4=96, 7+2=63, then 6+5=?",
                "answer": "66",
                "hints": ["Look at the pattern", "Multiply then concatenate", "First×Second, then concat"]
            }
        ]
        
        while len(puzzles) < num_puzzles and fallback_puzzles:
            puzzles.append(fallback_puzzles.pop(0))
    
    print(f"Successfully generated {len(puzzles)} puzzles!\n")
    return puzzles[:num_puzzles]


    
def generate_dynamic_story(story_type, puzzle_num=None, total_puzzles=None):
    """
    Generate dynamic story text using the LLM for narrative variety.
    
    Args:
        story_type (str): Type of story - 'opening', 'intro', 'success', 'failure', 'game_over'
        puzzle_num (int): Current puzzle number (optional)
        total_puzzles (int): Total number of puzzles (optional)
    
    Returns:
        str: Generated story text (approximately 3-5 lines)
    """
    prompts = {
        'opening': "Write a 3-4 line atmospheric introduction to an ancient temple escape room. Make it mysterious and immersive. Keep it around 60-80 words.\n",
        
        'intro': f"Write a 2-3 line atmospheric description of entering chamber {puzzle_num} of an ancient temple with {total_puzzles} total chambers. Make it mysterious and varied, around 40-60 words. Don't mention specific puzzles.\n",
        
        'success': f"Write a 2-3 line celebratory message about solving puzzle {puzzle_num} out of {total_puzzles} in an ancient temple. Make it varied and encouraging. Around 40-60 words.\n",
        
        'failure': "Write a 3-4 line dramatic message about failing to escape an ancient temple due to puzzle failure. Make it mysterious and atmospheric. Around 50-70 words.\n",
        
        'game_over': "Write a 4-5 line epic epilogue message for successfully escaping an ancient temple after solving all puzzles. Make it satisfying and triumphant. Around 60-80 words.\n"
    }
    
    prompt = prompts.get(story_type, prompts['intro'])
    
    full_response = generate_text(prompt, temperature=0.8, max_new_tokens=200)
    
    story_text = full_response
        
    story_text = re.sub(r'\s+', ' ', story_text).strip()
    
    return story_text 


def create_narrator_agent():
    """Create a narrator agent for story elements with LLM-generated content."""
    class SimpleNarrator:
        def opening_story(self):
            dynamic_story = generate_dynamic_story('opening')
            return f"""
════════════════════════════════════════════════════════════════
                    WELCOME TO THE ESCAPE ROOM                  
                                                                
  {dynamic_story}
                                                                
  The heavy door behind you slams shut with a loud CLANG.       
  Your journey begins now...                                    
════════════════════════════════════════════════════════════════
"""
        
        def intro_story(self, puzzle_num, total_puzzles):
            dynamic_story = generate_dynamic_story('intro', puzzle_num, total_puzzles)
            return f"""
─ CHALLENGE {puzzle_num}/{total_puzzles} ─────────────────────
                                                                 
  {dynamic_story}
                                                                 
──────────────────────────────────────────────────────────────
"""
        
        def success_story(self, puzzle_num, total_puzzles):
            progress = int((puzzle_num / total_puzzles) * 100)
            dynamic_story = generate_dynamic_story('success', puzzle_num, total_puzzles)
            return f"""
════════════════════════════════════════════════════════════════
                      ✓ PUZZLE SOLVED! ✓                        
                                                                
  {dynamic_story}
                                                                
  Progress: {progress}% complete [{puzzle_num}/{total_puzzles}]
                                                                
════════════════════════════════════════════════════════════════
"""
        
        def failure_story(self, puzzle_num):
            dynamic_story = generate_dynamic_story('failure')
            return f"""
════════════════════════════════════════════════════════════════
                      ✗ PUZZLE FAILED ✗                         
                                                                
  {dynamic_story}
                                                                
              YOU HAVE BEEN TRAPPED IN THE TEMPLE...            
                      GAME OVER                                 
                                                                
════════════════════════════════════════════════════════════════
"""
        
        def hint_story(self, hint, attempt):
            return f"""
💡 HINT #{attempt}:
   A mysterious voice whispers: "{hint}"
"""
        
        def game_over_story(self, success):
            if success:
                dynamic_story = generate_dynamic_story('game_over')
                return f"""
════════════════════════════════════════════════════════════════
                   ✓ CONGRATULATIONS! ✓                       
                                                                
  {dynamic_story}
                                                                
  ✓ YOU HAVE ESCAPED! ✓                                         
                                                                
════════════════════════════════════════════════════════════════
"""
            else:
                dynamic_story = generate_dynamic_story('failure')
                return f"""
════════════════════════════════════════════════════════════════
                     GAME OVER - YOU ARE TRAPPED                
                                                                
  {dynamic_story}
                                                                
════════════════════════════════════════════════════════════════
"""
    
    return SimpleNarrator()


def run_llm_escape_room(num_puzzles=3):
    """
    Run an interactive LLM-generated escape room game.
    
    Args:
        num_puzzles (int): Number of puzzles to generate and solve.
    """
    puzzles = generate_puzzles(num_puzzles)
    
    if not puzzles:
        print("Error: Could not generate or load puzzles.")
        return
    
    narrator = create_narrator_agent()
    print(narrator.opening_story())
    
    max_attempts = 5
    total_solved = 0
    game_completed = True
    
    try:
        for puzzle_idx, puzzle_data in enumerate(puzzles, 1):
            print(narrator.intro_story(puzzle_idx, num_puzzles))
            
            question = puzzle_data.get('question', 'Unknown puzzle')
            answer = puzzle_data.get('answer', '').lower().strip()
            hints = puzzle_data.get('hints', [])
            
            if isinstance(hints, str):
                hints = [hints]
            
            print(f"PUZZLE: {question}\n")
            
            attempts = 0
            solved = False
            hint_index = 0
            
            while attempts < max_attempts and not solved:
                attempts += 1
                remaining = max_attempts - attempts
                
                user_answer = input(f"Your answer (Attempt {attempts}/{max_attempts}): ").strip().lower()
                
                if not user_answer:
                    print("Please enter an answer.\n")
                    attempts -= 1  
                    continue
                
                if user_answer == answer:
                    solved = True
                    total_solved += 1
                    print(narrator.success_story(puzzle_idx, num_puzzles))
                else:
                    if attempts in [1, 3, 4] and hint_index < len(hints):
                        hint_text = hints[hint_index]
                        print(narrator.hint_story(hint_text, attempts))
                        hint_index += 1
                        if remaining > 0:
                            print(f"Attempts remaining: {remaining}\n")
                    else:
                        if remaining > 0:
                            print(f"Incorrect! Attempts remaining: {remaining}\n")
                        else:
                            print(f"Incorrect! No attempts remaining.\n")
            
            if not solved:
                print(narrator.failure_story(puzzle_idx))
                print(f"The correct answer was: {answer.upper()}\n")
                game_completed = False
                break
        
        print(narrator.game_over_story(game_completed))
    
    except KeyboardInterrupt:
        print("\n\n  Game interrupted. Goodbye!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")


def main():
    """Main entry point for the LLM-based escape room game."""
    print("\n" + "="*70)
    print("       ESCAPE ROOM - LLM-GENERATED VERSION")
    print("="*70 + "\n")
    

    num_puzzles_input = input("How many puzzles would you like to solve? (1-5, default: 3): ").strip()
    num_puzzles = int(num_puzzles_input) if num_puzzles_input else 3
    run_llm_escape_room(num_puzzles=num_puzzles)


if __name__ == "__main__":
    main()