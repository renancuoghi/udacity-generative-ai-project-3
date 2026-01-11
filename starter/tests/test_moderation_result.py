"""
Tests for moderation result classes.

These tests verify that all moderation result classes have the correct attributes
with the expected types and are properly defined as Pydantic models.
"""

import pytest
from pydantic import ValidationError

from multimodal_moderation.types.moderation_result import (
    ModerationResult,
    TextModerationResult,
    ImageModerationResult,
    VideoModerationResult,
    AudioModerationResult,
)


class TestModerationResult:
    """Test the base ModerationResult class"""

    def test_has_rationale_field(self):
        """Verify ModerationResult has rationale field"""
        result = ModerationResult(rationale="Test rationale", is_flagged=False)
        assert hasattr(result, "rationale"), "ModerationResult should have a 'rationale' attribute"
        assert hasattr(result, "is_flagged"), "ModerationResult should have a 'is_flagged' attribute"
        assert isinstance(result.rationale, str), "rationale should be a string"
        assert isinstance(result.is_flagged, bool), "is_flagged should be a boolean"
        assert result.rationale == "Test rationale", "rationale should contain the provided value"
        assert result.is_flagged is False, "is_flagged should contain the provided value"

    def test_defaults(self):
        """Verify defaults"""
        result = ModerationResult()
        assert result.rationale == ""
        assert result.is_flagged is False
        assert result.contains_pii is False
        assert result.is_unfriendly is False
        assert result.is_unprofessional is False

    def test_is_flagged_logic(self):
        """Verify is_flagged logic"""
        # Auto-flagging
        assert ModerationResult(contains_pii=True).is_flagged is True
        assert ModerationResult(is_unfriendly=True).is_flagged is True
        assert ModerationResult(is_unprofessional=True).is_flagged is True
        
        # Override manual setting if no flags
        assert ModerationResult(is_flagged=True).is_flagged is False
        
        # Override manual setting if flags
        assert ModerationResult(is_flagged=False, contains_pii=True).is_flagged is True

    def test_is_pydantic_model(self):
        """Verify ModerationResult is a Pydantic BaseModel"""
        result = ModerationResult(rationale="Test", is_flagged=False)
        assert hasattr(result, "model_dump"), "ModerationResult should have model_dump method (Pydantic BaseModel)"
        assert hasattr(result, "model_validate"), "ModerationResult should have model_validate method (Pydantic BaseModel)"


class TestTextModerationResult:
    """Test the TextModerationResult class"""

    def test_has_all_required_fields(self):
        """Verify TextModerationResult has all required fields"""
        result = TextModerationResult(
            rationale="Test rationale",
            is_flagged=True,  # Will be corrected to False if flags are false
            contains_pii=True,
            is_unfriendly=False,
            is_unprofessional=True,
        )

        assert hasattr(result, "rationale"), "TextModerationResult should have 'rationale' field"
        assert hasattr(result, "contains_pii"), "TextModerationResult should have 'contains_pii' field"
        assert hasattr(result, "is_unfriendly"), "TextModerationResult should have 'is_unfriendly' field"
        assert hasattr(result, "is_unprofessional"), "TextModerationResult should have 'is_unprofessional' field"
        # Logic check
        assert result.is_flagged is True

    def test_defaults(self):
        """Verify defaults"""
        result = TextModerationResult()
        assert result.rationale == ""
        assert result.contains_pii is False

    def test_inherits_from_moderation_result(self):
        """Verify TextModerationResult inherits from ModerationResult"""
        assert issubclass(TextModerationResult, ModerationResult), \
            "TextModerationResult should inherit from ModerationResult"


class TestImageModerationResult:
    """Test the ImageModerationResult class"""

    def test_has_all_required_fields(self):
        """Verify ImageModerationResult has all required fields"""
        result = ImageModerationResult(
            rationale="Test rationale",
            # is_flagged logic will run. Since is_disturbing is set separately below...
            # We must pass arguments.
            contains_pii=True,
            is_disturbing=False,
            is_low_quality=True,
        )

        assert hasattr(result, "rationale"), "ImageModerationResult should have 'rationale' field"
        assert hasattr(result, "contains_pii"), "ImageModerationResult should have 'contains_pii' field"
        assert hasattr(result, "is_disturbing"), "ImageModerationResult should have 'is_disturbing' field"
        assert hasattr(result, "is_low_quality"), "ImageModerationResult should have 'is_low_quality' field"
        
        # Check logic: contains_pii=True -> is_flagged=True
        assert result.is_flagged is True

    def test_is_flagged_with_disturbing(self):
        """Verify is_disturbing triggers is_flagged"""
        result = ImageModerationResult(is_disturbing=True)
        assert result.is_flagged is True

    def test_defaults(self):
        """Verify defaults"""
        result = ImageModerationResult()
        assert result.is_disturbing is False
        assert result.is_low_quality is False
        assert result.is_flagged is False

    def test_inherits_from_moderation_result(self):
        """Verify ImageModerationResult inherits from ModerationResult"""
        assert issubclass(ImageModerationResult, ModerationResult), \
            "ImageModerationResult should inherit from ModerationResult"


class TestVideoModerationResult:
    """Test the VideoModerationResult class"""

    def test_has_all_required_fields(self):
        """Verify VideoModerationResult has all required fields"""
        result = VideoModerationResult(
            rationale="Test rationale",
            contains_pii=True,
            is_disturbing=False,
            is_low_quality=True,
        )

        assert hasattr(result, "rationale"), "VideoModerationResult should have 'rationale' field"
        assert hasattr(result, "contains_pii"), "VideoModerationResult should have 'contains_pii' field"
        assert hasattr(result, "is_disturbing"), "VideoModerationResult should have 'is_disturbing' field"
        assert hasattr(result, "is_low_quality"), "VideoModerationResult should have 'is_low_quality' field"
        assert result.is_flagged is True

    def test_is_flagged_with_disturbing(self):
        """Verify is_disturbing triggers is_flagged"""
        result = VideoModerationResult(is_disturbing=True)
        assert result.is_flagged is True

    def test_defaults(self):
        """Verify defaults"""
        result = VideoModerationResult()
        assert result.is_disturbing is False
        assert result.is_flagged is False

    def test_inherits_from_moderation_result(self):
        """Verify VideoModerationResult inherits from ModerationResult"""
        assert issubclass(VideoModerationResult, ModerationResult), \
            "VideoModerationResult should inherit from ModerationResult"


class TestAudioModerationResult:
    """Test the AudioModerationResult class"""

    def test_has_all_required_fields(self):
        """Verify AudioModerationResult has all required fields"""
        result = AudioModerationResult(
            rationale="Test rationale",
            transcription="Test transcription",
            contains_pii=True,
            is_unfriendly=False,
            is_unprofessional=True,
        )

        assert hasattr(result, "rationale"), "AudioModerationResult should have 'rationale' field"
        assert hasattr(result, "transcription"), "AudioModerationResult should have 'transcription' field"
        assert hasattr(result, "contains_pii"), "AudioModerationResult should have 'contains_pii' field"
        assert hasattr(result, "is_unfriendly"), "AudioModerationResult should have 'is_unfriendly' field"
        assert hasattr(result, "is_unprofessional"), "AudioModerationResult should have 'is_unprofessional' field"
        assert result.is_flagged is True

    def test_defaults(self):
        """Verify defaults"""
        result = AudioModerationResult()
        assert result.transcription == ""
        assert result.is_flagged is False

    def test_inherits_from_moderation_result(self):
        """Verify AudioModerationResult inherits from ModerationResult"""
        assert issubclass(AudioModerationResult, ModerationResult), \
            "AudioModerationResult should inherit from ModerationResult"
