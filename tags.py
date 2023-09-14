from pydantic import BaseModel, Field
from enum import Enum, auto

class Sentiment(str, Enum):
    positive = "positive"
    neutral = "neutral"
    negative = "negative"

class Tone(str, Enum):
    positive = "positive"
    negative = "negative"
    neutral = "neutral"
    mixed = "mixed"
    happy = "happy"
    sad = "sad"
    angry = "angry"
    surprised = "surprised"
    fearful = "fearful"
    confident = "confident"
    uncertain = "uncertain"
    excited = "excited"
    disgusted = "disgusted"
    hopeful = "hopeful"
    cautious = "cautious"

class Language(str, Enum):
    spanish = "spanish"
    english = "english"
    french = "french"
    german = "german"
    italian = "italian"
    dutch = "dutch"
    portuguese = "portuguese"
    russian = "russian"
    chinese = "chinese"
    japanese = "japanese"
    arabic = "arabic"
    hindi = "hindi"
    korean = "korean"
    turkish = "turkish"

class Tags(BaseModel):
    sentiment: Sentiment = Field(..., description="Describes the sentiment of the statement.")
    tone: Tone = Field(
        ...,
        description="Describes the tone of the statement.",
    )
    language: Language = Field(
        ...,
        description="Specifies the language of the text.",
    )


