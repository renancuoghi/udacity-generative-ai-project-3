from typing import Literal
from pydantic import BaseModel, Field, model_validator


class ModerationResult(BaseModel):

    is_flagged: bool = Field(
        default=False, description="Whether the content was flagged by any of the safety checks"
    )
    rationale: str = Field(default="", description="Explanation of what was harmful and why")
    contains_pii: bool = Field(
        default=False,
        description="Whether the message contains any personally-identifiable information (PII)",
    )
    is_unfriendly: bool = Field(
        default=False, description="Whether unfriendly tone or content was detected"
    )
    is_unprofessional: bool = Field(
        default=False, description="Whether unprofessional tone or content was detected"
    )

    @model_validator(mode="after")
    def update_is_flagged(self) -> "ModerationResult":
        flags = [
            self.contains_pii,
            self.is_unfriendly,
            self.is_unprofessional,
            getattr(self, "is_disturbing", False),
        ]
        if any(flags):
            self.is_flagged = True
        else:
            self.is_flagged = False
        return self


class TextModerationResult(ModerationResult):
    pass


class ImageModerationResult(ModerationResult):
    is_disturbing: bool = Field(default=False, description="Whether the image is disturbing")
    is_low_quality: bool = Field(default=False, description="Whether the image is low quality")


class VideoModerationResult(ModerationResult):
    is_disturbing: bool = Field(default=False, description="Whether the video is disturbing")
    is_low_quality: bool = Field(default=False, description="Whether the video is low quality")


# TODO: Create AudioModerationResult class that inherits from ModerationResult and contains:
#   - transcription: str to contain the transcription of the audio
#   - contains_pii: bool to contain a flag for whether the audio contains any personally-identifiable
#       information (PII) such as names, addresses, phone numbers
#   - is_unfriendly: bool to contain a flag for whether unfriendly tone or content was detected
#   - is_unprofessional: bool to contain a flag for whether unprofessional tone or content was detected
class AudioModerationResult(ModerationResult):
    transcription: str = Field(default="", description="Transcription of the audio")
