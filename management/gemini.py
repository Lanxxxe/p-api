from google import genai
from google.genai import errors as genai_errors
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))


# ---------------------------------------------------------------------------
# Custom exceptions
# ---------------------------------------------------------------------------

class GeminiError(Exception):
    """Base class for Gemini-related errors."""


class GeminiRateLimitError(GeminiError):
    """Raised when the Gemini API quota or rate limit is exceeded."""

    def __str__(self):
        return (
            'Gemini API rate limit reached. '
            'You may have hit the free-tier daily quota — please try again later.'
        )


class GeminiServiceError(GeminiError):
    """Raised when the Gemini service is temporarily unavailable."""

    def __str__(self):
        return 'Gemini service is currently unavailable. Please try again in a moment.'


class GeminiTimeoutError(GeminiError):
    """Raised when the Gemini API call times out."""

    def __str__(self):
        return 'The Gemini request timed out. Please try again.'


class GeminiEmptyResponseError(GeminiError):
    """Raised when Gemini returns an empty or unusable response."""

    def __str__(self):
        return 'Gemini returned an empty response. Please try again.'


# ---------------------------------------------------------------------------
# Internal helper
# ---------------------------------------------------------------------------

def _call_gemini(prompt: str) -> str:
    """
    Execute a Gemini API call and translate SDK/HTTP errors into
    friendly GeminiError subclasses so callers never deal with raw SDK exceptions.
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=prompt,
        )
    except genai_errors.ClientError as exc:
        # 4xx — 429 is quota/rate-limit; everything else is a config/auth issue
        if exc.code == 429:
            raise GeminiRateLimitError() from exc
        raise GeminiError(f'Gemini client error ({exc.code}): {exc.message}') from exc
    except genai_errors.ServerError as exc:
        # 5xx — 503 service unavailable, 504 deadline exceeded
        if exc.code == 504:
            raise GeminiTimeoutError() from exc
        raise GeminiServiceError() from exc
    except genai_errors.APIError as exc:
        raise GeminiError(f'Gemini API error ({exc.code}): {exc.message}') from exc
    except Exception as exc:
        raise GeminiError(f'Unexpected error calling Gemini: {exc}') from exc

    text = getattr(response, 'text', None)
    if not text or not text.strip():
        raise GeminiEmptyResponseError()

    return text.strip()


# ---------------------------------------------------------------------------
# Public functions
# ---------------------------------------------------------------------------

def enhance_note(notes: str, internship_role: str = 'Intern') -> str:
    """
    Enhance a daily internship note using Gemini.

    Parameters:
        notes           – the raw note written by the intern
        internship_role – the intern's position (e.g. 'Web Developer Intern')

    Returns:
        A single plain-text string with the enhanced note.

    Raises:
        GeminiRateLimitError  – free-tier quota exceeded
        GeminiServiceError    – API temporarily unavailable
        GeminiTimeoutError    – request timed out
        GeminiEmptyResponseError – API returned empty text
        GeminiError           – any other API failure
    """
    prompt = (
        f"You are helping a '{internship_role}' improve their daily internship journal entry. "
        "Rewrite the note below so it is clearer, more professional, and better structured, "
        "while keeping all the original details and staying in the first person. "
        "Return ONLY the rewritten note text — no headings, no labels, no markdown, "
        "no introductory phrases, and no closing remarks.\n\n"
        f"Original note:\n{notes}"
    )
    return _call_gemini(prompt)


def summarize_week_notes(notes_entries: list, week_label: str, internship_role: str = 'Intern') -> str:
    """
    Summarize all daily notes for a given week using Gemini.

    Parameters:
        notes_entries   – list of dicts with keys: 'day_name', 'date', 'notes'
        week_label      – human-readable week range (e.g. 'February 23 – March 1, 2026')
        internship_role – the intern's position

    Returns:
        A plain-text weekly summary string.

    Raises:
        GeminiRateLimitError  – free-tier quota exceeded
        GeminiServiceError    – API temporarily unavailable
        GeminiTimeoutError    – request timed out
        GeminiEmptyResponseError – API returned empty text
        GeminiError           – any other API failure
    """
    if not notes_entries:
        return 'No notes were recorded for this week.'

    entries_text = '\n\n'.join(
        f"{entry['day_name']} ({entry['date']}):\n{entry['notes']}"
        for entry in notes_entries
    )

    prompt = (
        f"You are helping a '{internship_role}' create a weekly summary of their internship journal. "
        "Below are their daily notes. Write a concise, professional weekly summary that captures "
        "the key activities, learnings, and achievements across the week. Keep it in the first person. "
        "Return ONLY the summary text — no headings, no labels, no markdown, "
        "no introductory phrases, and no closing remarks.\n\n"
        f"Week: {week_label}\n\n"
        f"Daily Notes:\n{entries_text}"
    )
    return _call_gemini(prompt)
