# anki-code-highlighter
A simple command-line tool to format code snippets for the open-source Anki flashcards program to be styled with CSS.
When run, program copies data from clipboard, parses into valid HTML, and pastes to clipboard. If output flag _-o_ is set, outputs to output.txt.
Additionally, filters out Anki-style cloze deletions.
