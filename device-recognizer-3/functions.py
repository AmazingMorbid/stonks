import spacy
from spacy import registry
from spacy.util import compile_infix_regex


@registry.callbacks("customize_tokenizer")
def make_customize_tokenizer():
    def customize_tokenizer(nlp: spacy.Language):
        # add '/' as a infix
        infixes = nlp.Defaults.infixes + [r'''/''']
        infix_regex = compile_infix_regex(infixes)
        nlp.tokenizer.infix_finditer = infix_regex.finditer

    return customize_tokenizer
