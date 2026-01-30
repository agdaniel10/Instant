import re

# Original pattern (keeps colon format)
VERSE_REGEX_COLON = re.compile(r'\b([1-3]?\s?[A-Za-z]+)\s+(\d+):(\d+)(?:-(\d+))?\b')

# New pattern (handles spoken formats without colon)
VERSE_REGEX_NO_COLON = re.compile(
    r'\b([1-3]?\s?[A-Za-z]+)\s+(?:chapter\s+)?(\d+)\s+(?:v(?:erse)?\.?\s+)?(\d+)(?:\s*(?:through|to|-)\s*(\d+))?\b',
    re.IGNORECASE
)

# Pattern for "John 316" format (no space, no colon)
VERSE_REGEX_COMPACT = re.compile(r'\b([1-3]?[A-Za-z]+)\s*(\d{1,3})(\d{1,3})\b')

def detect_verses(text):
    matches = []
    
    # Try colon format first: "John 3:16"
    for match in VERSE_REGEX_COLON.finditer(text):
        book = match.group(1).strip()
        chapter = int(match.group(2))
        verse_start = int(match.group(3))
        verse_end = int(match.group(4)) if match.group(4) else verse_start
        matches.append((book, chapter, verse_start, verse_end))
    
    # Try spoken format: "John chapter 3 verse 16"
    if not matches:
        for match in VERSE_REGEX_NO_COLON.finditer(text):
            book = match.group(1).strip()
            chapter = int(match.group(2))
            verse_start = int(match.group(3))
            verse_end = int(match.group(4)) if match.group(4) else verse_start
            matches.append((book, chapter, verse_start, verse_end))
    
    # Try compact format: "John316" or "John 316"
    if not matches:
        for match in VERSE_REGEX_COMPACT.finditer(text):
            book = match.group(1).strip()
            # Split the number part intelligently
            full_number = match.group(2) + match.group(3)
            
            # Heuristic: if 3+ digits, first 1-2 are chapter, rest are verse
            if len(full_number) >= 3:
                if int(full_number[0]) > 0:  # Valid chapter
                    chapter = int(full_number[:-2] if len(full_number) > 3 else full_number[0])
                    verse_start = int(full_number[-2:])
                    verse_end = verse_start
                    matches.append((book, chapter, verse_start, verse_end))
    
    return matches