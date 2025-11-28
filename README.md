# 🎮 AI-Powered Escape Room Game

A terminal-based escape room game powered by AI agents that generate puzzles, validate answers, provide hints, and narrate an immersive story.

## 📋 Overview

This project implements an escape room game using two different approaches:

1. **Custom Multi-Agent System** (`multi_agent_system.py`) - Built from scratch using OpenAI's function calling API
2. **LangChain Implementation** (`langchain_agent.py`) - Using LangChain's agent framework

Both implementations feature autonomous AI agents that collaborate to create an engaging puzzle-solving experience.

---

## 🎯 Features

### Core Gameplay
- **Dynamic Puzzle Generation**: AI generates riddles, math puzzles, and word puzzles
- **Intelligent Answer Validation**: Semantic validation accepts synonyms and variations (e.g., "4" = "four", "echo" = "an echo")
- **Progressive Hint System**: Hints become more direct with each request (subtle → direct → almost-the-answer)
- **Puzzle Validation**: Automatically detects and rejects ambiguous puzzles or incorrect answers
- **Immersive Narration**: Dramatic storytelling that reacts to player progress
- **Configurable Difficulty**: Choose number of puzzles, attempts per puzzle (default: 5), hints per puzzle (default: 3)

### AI Agents

Both implementations include four specialized agents:

1. **Puzzle Generator Agent**
   - Generates riddles, math puzzles, and word puzzles
   - Tools: `generate_riddle`, `generate_math_puzzle`, `generate_word_puzzle`, `random_puzzle`

2. **Game State Manager Agent**
   - Validates player answers with semantic understanding
   - Tools: `check_player_answer`

3. **Hint Master Agent**
   - Provides progressive hints based on attempt count
   - Tools: `get_hint`, `reset_hints`

4. **Narrator Agent**
   - Creates immersive storytelling
   - Tools: `intro_story`, `narrate_success`, `narrate_failure`, `ending`

---

## 🚀 Installation

### Prerequisites
- Python 3.8+
- OpenAI API key

### Setup

1. **Clone/Download the repository**
   ```bash
   cd escape-room-game
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

---

## 🎮 Usage

### Run the Custom Multi-Agent System
```bash
python multi_agent_system.py
```

### Run the LangChain Implementation
```bash
python langchain_agent.py
```

### Gameplay

1. **Start the game**: Enter number of puzzles (default: 2)
2. **Read the introduction** and press Enter
3. **Solve puzzles**:
   - Type your answer when prompted
   - Type `hint` to get a hint (max 3 per puzzle)
   - Type `quit` to exit
4. **Win**: Solve all puzzles
5. **Lose**: Fail a puzzle after 5 attempts

---

## 🏗️ Architecture

### Custom Implementation (`multi_agent_system.py`)

```
Orchestrator (Python class)
    ├─► Puzzle Generator Agent (Custom Puzzle_Agent)
    ├─► Game State Manager Agent (Custom Puzzle_Agent)
    ├─► Hint Master Agent (Custom Puzzle_Agent)
    └─► Narrator Agent (Custom Puzzle_Agent)
```

- Built from scratch using OpenAI's function calling API
- Full control over agent behavior
- Custom `Puzzle_Agent` class handles tool execution

### LangChain Implementation (`langchain_agent.py`)

```
Direct Agent Calls (Python function)
    ├─► Puzzle Generator Agent (LangChain create_agent)
    ├─► Game State Manager Agent (LangChain create_agent)
    ├─► Hint Master Agent (LangChain create_agent)
    └─► Narrator Agent (LangChain create_agent)
```

- Uses LangChain's agent framework
- `@tool` decorators for standardized tool definitions
- Fallback to direct tool calls for reliability

---

## 🔧 Technical Details

### Puzzle Validation

1. **Structure Validation**: Checks puzzle format
2. **Answer Correctness**: LLM validates the answer
3. **Ambiguity Detection**: Rejects puzzles with multiple valid answers
4. **Regeneration**: Max 3 attempts, then uses fallback puzzles

**Example:**
```
❌ REJECTED: "I can be cracked, made, told, and played"
   (Multiple answers: joke, laughter, riddle, code)

✓ ACCEPTED: "I speak without a mouth and hear without ears"
   (Single answer: echo)
```

### Answer Validation

AI intelligently validates answers:
- ✓ "echo", "an echo", "Echo", "ECHO" → All correct
- ✗ "sound", "voice" → Rejected (different concepts)

### Progressive Hints

1. **Subtle**: "Think about sound reflection..."
2. **Moderate**: "It's heard in caves or mountains..."
3. **Direct**: "Rhymes with 'gecko'..."

---

## 🎓 Design Decisions

### Why Two Implementations?

1. **Educational**: Understanding agents fundamentally
2. **Comparison**: Custom vs. framework approaches
3. **Trade-offs**: Build vs. use libraries

### Orchestrator Design

**Initially tried**: AI agent as orchestrator
- ❌ Too unpredictable for strict game rules
- ❌ Difficult to enforce limits

**Final approach**: Traditional Python orchestrator
- ✓ AI for creativity (puzzles, hints, narration)
- ✓ Code for mechanics (rules, state management)

---

## 📊 Performance

### Token Usage (per 3-puzzle game)
- Total: ~4,000-6,000 tokens
- Cost with GPT-4o-mini: ~$0.001-0.003 per game

---

## 🐛 Known Limitations

1. **LLM Arithmetic**: Small models sometimes fail at math
   - Validation catches most errors

2. **State Management**: Tracked across multiple locations
   - Clear separation of concerns

3. **Error Handling**: Basic try-catch blocks
   - Could add more detailed recovery

---

## 📝 Example Session

```
$ python multi_agent_system.py

Enter number of puzzles (default 2): 2

======================================================================
AI-POWERED ESCAPE ROOM
======================================================================

Narrator: Welcome! You're trapped in an ancient temple. Solve 2 puzzles 
to escape. You have 5 attempts per puzzle and 3 hints available...

Press Enter to continue...

[Generating Puzzles...]
  ✓ Puzzle 1 validated successfully
  ✓ Puzzle 2 validated successfully

======================================================================
PUZZLE 1/2
======================================================================

❓ I speak without a mouth and hear without ears. What am I?

🔓 Your answer (Attempt 1/5): hint

💡 Think about something that repeats sounds in caves...

🔓 Your answer (Attempt 1/5): echo

✓ Correct! The temple door clicks open...

======================================================================
🎉 CONGRATULATIONS! YOU ESCAPED! 🎉
======================================================================
```

---

## 🤝 Contributing

This is an educational project. Feel free to:
- Fork and experiment
- Add new puzzle types
- Enhance validation logic
- Improve narration

---

## 🙏 Acknowledgments

- **OpenAI** for GPT-4o-mini API
- **LangChain** for the agent framework
- **Code.Hub AI Engineer Academy** for the assignment

---

## 📞 Contact

**Stavros Lazaridis**
- AI Engineer Academy Graduate (October 2025)
- MSc in Data Science and Machine Learning

---

## 🎯 Future Enhancements

- [ ] Web interface (Flask/Streamlit)
- [ ] Multiplayer mode
- [ ] Difficulty levels
- [ ] Themed puzzle sets
- [ ] Timed challenges
- [ ] Image-based puzzles

---

**Enjoy your escape! 🎮🔓✨**