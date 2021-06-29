import logging
from typing import Union, Iterable, Generator

import spacy

from schemas import DeviceInfo


class DeviceRecognizer:
    def __init__(self):
        self.nlp = spacy.load("model")
        self.logger = logging.getLogger(__name__)

    def get_info(self, texts: Iterable[str]) -> Generator[DeviceInfo, None, None]:
        self.logger.debug(f"Getting info from texts. ")

        for doc in self.nlp.pipe(texts=texts):
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

            yield output
