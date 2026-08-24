# AI Work Log

This directory records how AI assistance was used while developing the circuit simulator. The goal is to preserve the main project context, decisions, and lessons learned.

## How to record a session

Add a new entry at the top of this file after a meaningful coding session. Use the date and a short description as the heading.

## Entry format

```
## YYYY-MM-DD: Short description

- AI Model: Which AI model was used, and any relevant settings.

**Prompt**

What was asked of the AI?

**Result**

What changed or was investigated?

**Notes**

Important decisions, tests, lessons, or follow-up work.
```


---

## 2026-08-23: Start implementation 

- **AI Model**: GitHub Copilot Chat, Auto (only choice on Student package). **Selected Model**: GPT5.6-Luna.

**Prompt**

Let's start to work on this Circuit Simulator project following the project specification attached here. Dispatch work and design full loop to check the goal of Milestone 1: Netlist parser and viewer

- parse the restricted language;
- normalize case and whitespace;
- remove comments;
- validate element syntax and node identifiers;
- store typed-by-convention dictionaries;
- display the parsed circuit using real electrical symbols.

**Result**

First draft of implementation for both parser and viewer. Parser is working, but the viewer is not yet displaying the circuit correctly (diagonal links).
 
**Notes**
 
Visualisation was subpar (diagonals links), but the parser was working. Iterates a few times. Provides an example of a simple diagram drawing. Adds voltmeter, ammeter and voltage source.

---

## 2026-08-15: 1st session, Prompt Engineering.

- **AI Model**: MS365 Copilot Chat, GTP5.6-Think.

**Prompt**

Provide a prompt that you enable me to go chapter by chapter in this book, understand the concepts presented and code the suggested methods. FIrst look at the book in general to see its format regarding the code. WHat would be a good prompt for a AI agent?

**Result**

Detailled prompt, learning oriented. See attached file `docs/ai-work-log/prompt1.md`.

**Notes**

I asked to implement in Python instead of C.
