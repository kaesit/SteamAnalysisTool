"""Unit tests for TextCleaner module."""

from data_collection.processors.text_cleaner import TextCleaner


class TestTextCleaner:
    """Test suite for TextCleaner class."""

    def test_strip_html(self):
        """Test HTML tag removal."""
        raw = "<p>Hello <b>world</b>!</p>"
        cleaned = TextCleaner.strip_html(raw)
        assert "<p>" not in cleaned
        assert "<b>" not in cleaned
        assert "Hello" in cleaned
        assert "world" in cleaned

    def test_unescape_html_entities(self):
        """Test HTML entity decoding."""
        raw = "&quot;Test&quot; &amp; &lt;tag&gt;"
        cleaned = TextCleaner.unescape_html_entities(raw)
        assert "&quot;" not in cleaned
        assert "&amp;" not in cleaned
        assert '"Test"' in cleaned
        assert "&" in cleaned

    def test_remove_steam_bbcode(self):
        """Test Steam BBCode removal."""
        raw = "[h1]Title[/h1] [b]Bold[/b] text"
        cleaned = TextCleaner.remove_steam_bbcode(raw)
        assert "[h1]" not in cleaned
        assert "[/h1]" not in cleaned
        assert "[b]" not in cleaned
        assert "Title" in cleaned
        assert "Bold" in cleaned

    def test_normalize_whitespace(self):
        """Test whitespace normalization."""
        raw = "Multiple   spaces\n\nDouble newlines\r\n\r\nTabs\t\there"
        cleaned = TextCleaner.normalize_whitespace(raw)
        assert "   " not in cleaned
        assert "\n\n" not in cleaned
        assert "\r" not in cleaned
        assert "Multiple spaces" in cleaned

    def test_clean_review(self):
        """Test complete review cleaning pipeline."""
        raw = """
        <p>This game is <b>absolutely amazing</b>!</p>
        Great gameplay and storyline.
        Check out my channel: http://youtube.com/user123
        [h1]Highly Recommended[/h1]
        &quot;Must play&quot; - IGN
        """
        cleaned = TextCleaner.clean_review(raw)

        # Check that HTML/BBCode is removed
        assert "<p>" not in cleaned
        assert "<b>" not in cleaned
        assert "[h1]" not in cleaned

        # Check that content is preserved
        assert "amazing" in cleaned
        assert "gameplay" in cleaned
        assert "Highly Recommended" in cleaned
        assert "Must play" in cleaned

        # Check that whitespace is normalized
        assert "\n\n" not in cleaned
        assert "   " not in cleaned

    def test_clean_description(self):
        """Test description cleaning pipeline."""
        raw = "<h2>Game Description</h2><p>Long description with <b>formatting</b></p>"
        cleaned = TextCleaner.clean_description(raw)

        assert "<h2>" not in cleaned
        assert "<p>" not in cleaned
        assert "<b>" not in cleaned
        assert "Game Description" in cleaned
        assert "Long description" in cleaned
        assert "formatting" in cleaned

    def test_remove_urls(self):
        """Test URL removal."""
        raw = "Check out http://example.com and https://github.com/user/repo"
        cleaned = TextCleaner.remove_urls(raw)

        assert "http://" not in cleaned
        assert "https://" not in cleaned
        assert "example.com" not in cleaned

    def test_clean_all_aggressive(self):
        """Test aggressive cleaning with URL removal."""
        raw = """
        <p>Visit http://example.com for more!</p>
        [b]Amazing[/b] game with &quot;reviews&quot;
        """
        cleaned = TextCleaner.clean_all(raw)

        assert "http://" not in cleaned
        assert "<p>" not in cleaned
        assert "[b]" not in cleaned
        assert "amazing" in cleaned.lower()  # Text may be lowercased
        assert "reviews" in cleaned

    def test_empty_input(self):
        """Test handling of empty input."""
        assert TextCleaner.clean_review("") == ""
        assert TextCleaner.clean_description("") == ""
        assert TextCleaner.clean_all("") == ""

    def test_whitespace_only_input(self):
        """Test handling of whitespace-only input."""
        cleaned = TextCleaner.clean_review("   \n\n\t\t   ")
        assert cleaned.strip() == ""
