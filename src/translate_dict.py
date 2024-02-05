import json
from src.SampleTranslation05.translation_01 import translate_text_multiple

class TranslateDict:

    def __init__(self, json_path:str="/Users/robinfeldmann/TopicAnalysisRUWTweets/src/BertTopic07/translated.json"):
        self.to_translate: dict[str,list[str]] = {"de":[], "it":[], "sp":[], "fr":[],"ru":[],"uk":[] }
        self.dict = {}
        self.json_path = json_path

        self.load_from_json()


    def load_from_json(self):

        with open(self.json_path, 'r') as this:
            self.dict = json.loads(this.read())

    def look_up(self, word: str, source_language: str):
        if word in self.dict[source_language]:
            return
        
        if word in self.to_translate[source_language]:
            return
        self.to_translate[source_language].append(word)

    def translate_api(self, source_language=""):
        if not self.to_translate:
            return
        
        for lang in self.to_translate:
            if len(self.to_translate[lang])>0:
                for i in range(0, len(self.to_translate), 1000):
                    translated = translate_text_multiple(self.to_translate[lang][i:i+1000],source_language=source_language)
                    for word, trans in zip(self.to_translate[lang][i:i+1000], translated):
                        self.dict[lang][word] = trans
            self.to_translate[lang] = []

        with open(self.json_path, 'w') as this:
            this.write(json.dumps(self.dict))

    def batch_translate(self, words:list[str], source_language: str) -> list[str]:
        if source_language=="en":
            return words
        for word in words:
            self.look_up(word, source_language)

        self.translate_api(source_language=source_language)

        return [self.dict[source_language][word] for word in words]