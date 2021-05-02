
import spacy

from schemas import DeviceInfo


class DeviceRecognizer:
    def __init__(self):
        self.nlp = spacy.load("offers_model")

    def get_info(self, text: str) -> DeviceInfo:
        doc = self.nlp(text)

        output = DeviceInfo()
        for ent in doc.ents:
            ent_label = ent.label_

            if ent_label == "Model urządzenia":
                output.model = ent.text
            elif ent_label == "RAM / VRAM":
                output.memory = ent.text
            elif ent_label == "Pamięć":
                output.storage = ent.text
            elif ent_label == "Kolor":
                output.color = ent.text
            elif ent_label == "Przekątna ekranu":
                output.screen_size = ent.text

        return output
