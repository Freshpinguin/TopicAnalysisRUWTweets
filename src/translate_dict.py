import json
from src.SampleTranslation05.translation_01 import translate_text_multiple

class TranslateDict:

    def __init__(self, json_path:str="/Users/robinfeldmann/TopicAnalysisRUWTweets/src/BertTopic07/translated.json"):
        self.to_translate: list[str] = []
        self.dict = {}
        self.json_path = json_path

        self.load_from_json()


    def load_from_json(self):

        with open(self.json_path, 'r') as this:
            self.dict = json.loads(this.read())

    def look_up(self, word: str):
        if word in self.dict:
            return
        
        if word in self.to_translate:
            return
        self.to_translate.append(word)

    def translate_api(self, source_language=""):
        if not self.to_translate:
            return
        
        for i in range(0, len(self.to_translate), 1000):
            translated = translate_text_multiple(self.to_translate[i:i+1000],source_language=source_language)
            for word, trans in zip(self.to_translate[i:i+1000], translated):
                self.dict[word] = trans

        with open(self.json_path, 'w') as this:
            this.write(json.dumps(self.dict))

    def batch_translate(self, words:list[str], source_language="") -> list[str]:
        for word in words:
            self.look_up(word)

        self.translate_api(source_language=source_language)

        return [self.dict[word] for word in words]