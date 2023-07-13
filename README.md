# Poor man's QA system

This is just a small experiment to extract info for 2 different types of questions from Wikipedia with spaCy. All information is assumed to be found in the first sentence of person's Wikipedia page..

The user can ask about the following:
- When was person born?
- What field was the person on?

SpaCy's similarity method is used, so the questions don't have to be exactly in only one form. In addition, for the second question 3 examples are used.

## Some instructions

Press just enter when in "ask about person" prompt to go back to Wikipedia prompt.
CTRL+C to quit..

## Python modules needed

- spacy
  - model: "en_core_web_trf"; python -m spacy download "en_core_web_trf"
    it is needed at least to extract information from Gottfried Wilhelm Leibniz's Wikipedia-page
- spacy_sentence_bert
- wikipediaapi
- dateparser

## Picture of the program running

![QA2](https://github.com/tickBit/Poor-mans-QA/assets/61118857/6cee8bd8-8cf4-4e6c-8d2f-126a1c12a132)

