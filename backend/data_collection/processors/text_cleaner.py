"""Text cleaning and normalization utilities for review and description text.

This module provides methods to clean raw Steam text data by removing HTML,
normalizing whitespace, and stripping special Steam markup tokens.
"""

import html
import logging
import re
from typing import Optional

logger = logging.getLogger(__name__)


class TextCleaner:
    """Utilities for cleaning and normalizing text from Steam API responses.

    Handles HTML entity decoding, Steam BBCode tag removal, whitespace
    normalization, and special character handling. All methods are static
    for stateless text transformation.
    """

    # Regex patterns for various Steam and HTML markup
    HTML_TAG_PATTERN = re.compile(r"<[^>]+>")
    STEAM_BBCODE_PATTERN = re.compile(r"\[\w+\]|\[/\w+\]")
    MULTIPLE_WHITESPACE_PATTERN = re.compile(r"\s+")
    NEWLINE_PATTERN = re.compile(r"[\n\r\t]+")

    @staticmethod
    def strip_html(text: str) -> str:
        """Remove HTML tags from text.

        Args:
            text: Text potentially containing HTML tags.

        Returns:
            Text with HTML tags removed.
        """
        if not text:
            return ""

        text = TextCleaner.HTML_TAG_PATTERN.sub("", text)
        return text

    @staticmethod
    def unescape_html_entities(text: str) -> str:
        """Decode HTML entities to their character equivalents.

        Converts entities like &quot;, &amp;, &lt; to their actual characters.

        Args:
            text: Text containing HTML entities.

        Returns:
            Text with HTML entities decoded.
        """
        if not text:
            return ""

        return html.unescape(text)

    @staticmethod
    def remove_steam_bbcode(text: str) -> str:
        """Remove Steam BBCode formatting tags.

        Steam reviews sometimes contain BBCode markup like [h1], [b], [/h1], etc.

        Args:
            text: Text potentially containing Steam BBCode.

        Returns:
            Text with BBCode tags removed.
        """
        if not text:
            return ""

        text = TextCleaner.STEAM_BBCODE_PATTERN.sub("", text)
        return text

    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """Collapse multiple whitespace characters to single spaces.

        Converts newlines, tabs, and multiple spaces to single spaces.

        Args:
            text: Text with potentially irregular whitespace.

        Returns:
            Text with normalized whitespace.
        """
        if not text:
            return ""

        text = TextCleaner.NEWLINE_PATTERN.sub(" ", text)
        text = TextCleaner.MULTIPLE_WHITESPACE_PATTERN.sub(" ", text)
        return text.strip()

    @staticmethod
    def remove_urls(text: str) -> str:
        """Remove URLs from text.

        Removes http://, https://, and www. prefixed URLs.

        Args:
            text: Text potentially containing URLs.

        Returns:
            Text with URLs removed.
        """
        if not text:
            return ""

        url_pattern = re.compile(
            r"https?://[^\s]+ | www\.[^\s]+",
            re.VERBOSE,
        )
        text = url_pattern.sub("", text)
        return text

    @staticmethod
    def remove_special_characters(text: str) -> str:
        """Remove or normalize special characters.

        Keeps alphanumeric, spaces, and common punctuation.
        Removes control characters and unusual symbols.

        Args:
            text: Text potentially containing special characters.

        Returns:
            Text with special characters removed/normalized.
        """
        if not text:
            return ""

        text = re.sub(r"[^\w\s\-.,!?;:\'\"]", "", text)
        return text

    @classmethod
    def clean_review(cls, text: str) -> str:
        """Complete cleaning pipeline for review text.

        Applies all cleaning steps in optimal order:
        1. HTML tag stripping
        2. HTML entity unescaping
        3. BBCode removal
        4. Whitespace normalization

        Args:
            text: Raw review text from Steam API.

        Returns:
            Cleaned review text ready for NLP processing.
        """
        if not text:
            return ""

        text = cls.strip_html(text)
        text = cls.unescape_html_entities(text)
        text = cls.remove_steam_bbcode(text)
        text = cls.normalize_whitespace(text)

        if len(text) > 1000000:
            logger.warning("Cleaned review text exceeds 1MB, truncating")
            text = text[:1000000]

        return text

    @classmethod
    def clean_description(cls, text: str) -> str:
        """Complete cleaning pipeline for game description text.

        Similar to clean_review but with additional handling for longer
        descriptions that may contain more complex markup.

        Args:
            text: Raw game description from Steam API.

        Returns:
            Cleaned description text ready for processing.
        """
        if not text:
            return ""

        text = cls.strip_html(text)
        text = cls.unescape_html_entities(text)
        text = cls.remove_steam_bbcode(text)
        text = cls.normalize_whitespace(text)

        if len(text) > 5000000:
            logger.warning("Cleaned description exceeds 5MB, truncating")
            text = text[:5000000]

        return text

    @classmethod
    def clean_all(cls, text: str) -> str:
        """Most aggressive cleaning pipeline.

        Applies all cleaning techniques including URL and special character removal.
        Use for pre-processing before ML models.

        Args:
            text: Raw text from any source.

        Returns:
            Heavily cleaned text.
        """
        if not text:
            return ""

        text = cls.strip_html(text)
        text = cls.unescape_html_entities(text)
        text = cls.remove_steam_bbcode(text)
        text = cls.remove_urls(text)
        text = cls.normalize_whitespace(text)
        text = cls.remove_special_characters(text)

        return text.lower()
