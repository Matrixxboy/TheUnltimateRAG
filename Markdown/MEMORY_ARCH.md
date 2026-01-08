# Memory Architecture

The Ultimate RAG system employs a **Moving Window** consolidation pipeline to manage conversation history efficiently. This system distinguishes between **Short-Term Memory (STM)** (fast, active context) and **Long-Term Memory (LTM)** (summarized, persisted context).

## Architecture Diagram

```
[User Input] --> [Short-Term Memory (RAM)]
                        |
                        v
                +-------------------+
                | Threshold Check |  (Is Count > N?)
                +-------------------+
                        | Yes
                        v
                +-------------------+
                |   Consolidation   |
                +-------------------+
                | 1. Slice (Oldest N)
                | 2. LLM Summarization
                |    -> Summary
                |    -> Key Concepts
                | 3. Persist to DB (LTM)
                | 4. Flush from STM
                +-------------------+
                        |
                        v
            [Long-Term Memory (PostgreSQL)]
```

## Configuration

The logic is controlled by the `MEMORY_WINDOW_LIMIT` environment variable.

- **Variable**: `MEMORY_WINDOW_LIMIT`
- **Location**: `.env` file
- **Default**: `5` (messages)
- **Description**: The number of messages ($N$) to accumulate in Short-Term Memory before triggering a consolidation event.

### Example .env

```bash
MEMORY_WINDOW_LIMIT=10
```

## State Transition Guide (The "N+1" Rule)

1.  **Accumulation**: New messages are appended to the STM list.
2.  **Trigger**: Logic checks if `len(STM) > MEMORY_WINDOW_LIMIT`.
3.  **Consolidation Phase**:
    - **Input**: The oldest $N$ messages are selected.
    - **Processing**: These messages are sent to the LLM to generate a summary and extract key concepts.
    - **Persistence**: The result is saved to the `long_term_memories` table in PostgreSQL.
    - **Flush**: The oldest $N$ messages are **removed** from RAM.
    - **Result**: The STM now contains `len(original_STM) - N` messages (effectively starting the new window with the $(N+1)^{th}$ message).

### Preventing Data Loss

- The system uses a transactional approach (or at least ordered operations): Data is **persisted to DB first** before being **removed from RAM**.
- If the LLM or DB step fails, the STM is **not cleared**, ensuring the messages remain available for the next attempt (retry logic is implicit in the next user interaction).
