from google.cloud import translate


def translate_text(text:str="Hello, world!", project_id: str="evident-display-407715", source_language: str="en-US") -> str:
    """
    Translates text via Google Translate Api from source language to english.
    """
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": source_language,
            "target_language_code": "en-US",
        }
    )



    return " ".join([transl.translated_text for transl in response.translations])

