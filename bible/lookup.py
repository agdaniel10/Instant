import json
import os

# Load Bible JSON once
with open(os.path.join(os.path.dirname(__file__), "bible_data.json"), "r") as f:
    BIBLE_DATA = json.load(f)
    VERSES = BIBLE_DATA['verses']

def get_verse(book: str, chapter: int, verse_start: int, verse_end: int = None):
    """
    Retrieve Bible verse(s) from the loaded Bible data.
    
    Args:
        book: Book name (e.g., "John", "Genesis", "1 John")
        chapter: Chapter number
        verse_start: Starting verse number
        verse_end: Ending verse number (optional, defaults to verse_start)
    
    Returns:
        String containing the requested verse(s)
    """
    verse_end = verse_end or verse_start
    verses = []
    
    for v in range(verse_start, verse_end + 1):
        # Search for matching verse in the list
        found = [verse for verse in VERSES 
                 if verse['book_name'] == book 
                 and verse['chapter'] == chapter 
                 and verse['verse'] == v]
        
        if found:
            verses.append(found[0]['text'])
        else:
            verses.append(f"[Verse not found: {book} {chapter}:{v}]")
    
    return " ".join(verses)


# Optional: Helper function to get all available books
def get_available_books():
    """Returns a sorted list of all book names in the Bible."""
    books = set(verse['book_name'] for verse in VERSES)
    return sorted(books)


# Optional: Helper function to get chapter count for a book
def get_chapter_count(book: str):
    """Returns the number of chapters in a given book."""
    chapters = set(verse['chapter'] for verse in VERSES if verse['book_name'] == book)
    return max(chapters) if chapters else 0


# Optional: Helper function to get verse count for a chapter
def get_verse_count(book: str, chapter: int):
    """Returns the number of verses in a given chapter."""
    verses = [verse for verse in VERSES 
              if verse['book_name'] == book and verse['chapter'] == chapter]
    return len(verses)
