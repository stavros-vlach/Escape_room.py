# Stage 1: Research & Technology Decisions
## Escape Room Puzzle Master Agent

## 1. Executive Summary

This document presents the research findings and technology decisions for building a terminal-based Escape Room Puzzle Master Agent system. The project requires multiple cooperating agents without relying on external AI frameworks like LangChain or crewAI. I have analyzed different approaches for three critical aspects: puzzle generation, state management, and hint systems, ultimately choosing a **hybrid strategy** that balances innovation with practicality.

---

## 2. Puzzle Generation Approaches

### 2.1 Approaches Evaluated

**Approach 1: Hand-Crafted Templates**
- **Description**: Puzzles are predefined in Python dictionaries or JSON files
- **Implementation**: Store question, answer, and hints as structured data
- **Pros**: Full quality control, predictable, no dependencies
- **Cons**: Limited variety, tedious to create many puzzles

**Approach 2: Algorithmic Generation**
- **Description**: Puzzles generated programmatically using algorithms
- **Examples**: Random math problems, word scrambles, pattern sequences
- **Pros**: Unlimited variety, no external dependencies, deterministic
- **Cons**: Limited to structured puzzle types, less creative

**Approach 3: LLM-Based Generation (Local)**
- **Description**: Use Hugging Face Transformers to load local LLMs (Mistral, Phi-2, Llama)
- **Implementation**: Generate puzzles via prompt engineering
- **Pros**: Creative variety, adaptive, demonstrates AI integration skills
- **Cons**: Slower, requires model download, unpredictable quality


### 2.2 Comparative Analysis

| Criterion | Templates | Algorithmic | Local LLM |
|-----------|-----------|-------------|-----------|
| Quality | ✓✓✓ | ✓✓ | ✓✓ | 
| Variety | ✗ | ✓✓ | ✓✓✓ | 
| Speed | ✓✓✓ | ✓✓✓ | ✗ | 
| Cost | ✓✓✓ Free | ✓✓✓ Free | ✓✓✓ Free | 
| Offline | ✓✓✓ | ✓✓✓ | ✓✓✓* | 
| Dependencies | ✓✓✓ None | ✓✓✓ None | ✓ Heavy | 
| AI Integration | ✗ | ✗ | ✓✓✓ | 

*After initial model download

### 2.3 Decision: Dual Implementation

**Final Choice:** Implement **both** approaches:
1. **Template + Algorithmic** (puzzle.py) - Fast, reliable baseline
2. **Local LLM** (llm_room.py) - Demonstrates AI integration

**Rationale:**
- The assignment mentions "lightweight LLM integration" as an option to compare
- **Local LLM (Mistral-7B-Instruct)** selected over API because:
  - ✅ Truly "lightweight" - runs on consumer hardware
  - ✅ No API costs or internet dependency after download
  - ✅ Demonstrates modern AI/ML skills (Hugging Face ecosystem)
  - ✅ Satisfies "compare 2-3 approaches" requirement
- **Mistral-7B-Instruct chosen over alternatives:**
  - Phi-2 (2.7B): Too small, lower quality outputs
  - Llama-3-8B: Larger, slower, similar quality
  - **Mistral-7B**: Best balance of quality, size, and instruction-following

**Implementation Strategy:**
- **puzzle.py**: Production-ready, fast, reliable
- **llm_room.py**: Innovative, demonstrates LLM skills
- Both share same game flow architecture
- Users can choose which version to play

---

## 3. State Management Approaches

### 3.1 Approaches Evaluated

**Approach 1: Simple Data Structures (Dictionaries/Lists)**
- **Description**: Game state stored in nested dictionaries and lists
- **Implementation**: Pure functions manipulating data structures
- **Pros**: Minimal code, easy to understand
- **Cons**: Hard to maintain as complexity grows, no encapsulation

**Approach 2: Object-Oriented Design (Classes)**
- **Description**: Encapsulate each agent as a class with methods and state
- **Implementation**: `PuzzleGenerator`, `GameStateManager`, `HintMaster`, `Narrator` classes
- **Pros**: Modular, maintainable, testable, industry standard
- **Cons**: More initial setup, requires OOP understanding

### 3.2 Comparative Analysis

| Criterion | Dicts/Lists | OOP Classes | 
|-----------|-------------|-------------|
| Simplicity | ✓✓✓ | ✓✓ | 
| Maintainability | ✗ | ✓✓✓ | 
| Scalability | ✗ | ✓✓✓ | 
| Testability | ✗ | ✓✓✓ | 
| Learning Curve | ✓✓✓ | ✓✓ | 
| Multi-Agent Fit | ✗ | ✓✓✓ | 

### 3.3 Decision: Object-Oriented Design (OOP)

**Rationale:**
- **Perfect fit for multi-agent architecture**: Each agent = one class with clear responsibilities
- **Encapsulation**: Agents manage their own state (puzzles, attempts, hints)
- **Maintainability**: Easy to modify individual agents without affecting others
- **Professional practice**: Industry standard for game development and multi-agent systems
- **Testability**: Can unit test each agent independently
- **Extensibility**: Easy to add new puzzle types or agents later

**Implementation Details:**
- **Python `@dataclass`** for Puzzle structure:
  - Type safety with type hints
  - Automatic `__init__`, `__repr__`, `__eq__`
  - Cleaner than TypedDict (which doesn't support defaults)
  - Modern Python best practice
  
```python
@dataclass
class Puzzle:
    puzzle_id: str
    type: str
    question: str
    answer: str
    hints: List[str]
    solved: bool = False
    attempts: int = 0
```

- **Agent Classes**: Each with focused responsibilities (Single Responsibility Principle)
- **Orchestrator Pattern**: `EscapeRoomGame` class coordinates all agents

---

## 4. Hint Generation Approaches

### 4.1 Approaches Evaluated

**Approach 1: Pre-Scripted Hints**
- **Description**: Hints manually written for each puzzle
- **Implementation**: Stored as progressive arrays: `[vague, moderate, clear]`
- **Pros**: High quality, controlled messaging, narrative coherence
- **Cons**: Time-consuming to write, not adaptive

**Approach 2: LLM-Generated Adaptive Hints**
- **Description**: Use LLM to generate hints based on player's wrong answers
- **Implementation**: Pass puzzle and wrong answer to LLM for contextual hint
- **Pros**: Highly adaptive, can address specific misconceptions
- **Cons**: Slow, requires LLM, unpredictable quality

### 4.2 Comparative Analysis

| Criterion | Pre-Scripted | LLM-Generated |
|-------------|---------------|
| Quality | ✓✓✓ | ✓✓ |
| Speed | ✓✓✓ | ✗ |
| Adaptability | ✗ | ✓✓✓ |
| Narrative Fit | ✓✓✓ | ✓✓ |
| Implementation | ✓✓✓ | ✗ |

### 4.3 Decision: Hybrid with Attempt-Based Triggers

**Final Choice:** Pre-scripted hints with algorithmic fallbacks

**Hint Delivery Thresholds:**
- **After 1st wrong attempt**: Vague hint (guides thinking direction)
- **After 3rd wrong attempt**: Moderate hint (more specific clue)
- **After 4th wrong attempt**: Clear hint (near-solution or partial answer)

**Rationale:**
- **Pre-scripted for quality**: Hand-written hints ensure they align with narrative and puzzle intent
- **Algorithmic for math/logic**: Math puzzles use algorithmic hints (show equation steps)
- **Attempt-based escalation**: Creates natural difficulty curve without player request
- **No LLM for hints**: Keeps game responsive (LLM hint generation is too slow for gameplay)

**Implementation:**
```python
class Hint_Agent:
    def __init__(self):
        self.hint_thresholds = [1, 3, 4]
    
    def should_provide_hint(self, attempts: int) -> bool:
        return attempts in self.hint_thresholds
```

---

## 5. Additional Design Decisions

### 5.1 Why Two Implementations?

**Decision:** Provide both `puzzle.py` (templates) and `llm_room.py` (LLM-generated)

**Justification:**
1. **Satisfies "compare approaches" requirement**: Shows understanding of trade-offs
2. **Demonstrates versatility**: Can implement both classical and modern AI approaches
3. **Practical choice**: Template version is production-ready, LLM version is innovative
4. **Educational value**: Highlights when to use LLM vs when simpler approaches suffice


---

---

## 6. Comparison Matrix: Final Solution

### Template-Based vs LLM-Based

| Aspect | puzzle.py (Templates) | llm_room.py (LLM) |
|--------|----------------------|-------------------|
| **Speed** | Instant | 30-60s per puzzle |
| **Variety** | Limited (3-4 of each type) | Virtually unlimited |
| **Quality** | Consistent, high | Variable, creative |
| **Dependencies** | None (stdlib only) | transformers, torch |
| **Disk Space** | <1MB | ~15GB (model) |
| **RAM Usage** | <50MB | ~8-12GB |
| **Offline** | ✓ Yes | ✓ Yes (after download) |
| **Reliability** | ✓✓✓ | ✓✓ |
| **Innovation** | ✓ | ✓✓✓ |

**Conclusion:** Both approaches have merit. The dual implementation demonstrates:
1. Understanding of when LLMs add value
2. Ability to implement both classical and modern approaches
3. Practical engineering judgment (providing fallback option)

---

## 7. Learning Outcomes & Skills Demonstrated

This project demonstrates understanding of:

1. **Multi-Agent System Design**
   - Agent coordination without frameworks
   - Clear separation of concerns
   - Inter-agent communication patterns

2. **LLM Integration**
   - Local model deployment with Hugging Face
   - Prompt engineering for puzzle generation
   - Handling LLM unpredictability

3. **Software Architecture**
   - OOP design principles
   - Dataclass usage for type safety
   - Error handling and fallback strategies

4. **Comparative Analysis**
   - Evaluating trade-offs between approaches
   - Choosing appropriate tools for constraints
   - Justifying decisions with data

5. **Python Best Practices**
   - Type hints for code clarity
   - Modular code organization
   - Comprehensive documentation

---

## 8. Conclusion

The chosen architecture emphasizes **practical innovation balanced with reliability**. By implementing both a template-based and LLM-based version, this project showcases versatility and understanding of when to use cutting-edge AI versus proven classical approaches.

**Key Takeaway:** "Lightweight LLM integration" doesn't mean sacrificing quality—it means choosing the right tool for the job. Mistral-7B running locally provides the creativity of LLMs without the cost and complexity of API calls, while the template-based version ensures the game is always playable regardless of hardware constraints.

This design serves as a strong foundation for demonstrating both **technical problem-solving** and **creative AI integration skills**, fully satisfying the assignment's requirements while going beyond with dual implementations.

---

**References:**
- Hugging Face Transformers Documentation: https://huggingface.co/docs/transformers
- Mistral-7B-Instruct Model Card: https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2
- Python Dataclasses: https://docs.python.org/3/library/dataclasses.html
