# Poor man's QA system

This is just a small experiment to extract info for 2 different types of questions from Wikipedia with spaCy. All information is assumed to be found in the first sentence of person's Wikipedia page..

The user can ask about the following:
- When was person born?
- What field was the person on?

SpaCy's similarity method is used, so the questions don't have to be exactly in only one format. In addition, for the second questions 3 examples are used.

## Some instructions

Press just enter when in "ask about person" prompt to go back to Wikipedia prompt.
CTRL+C to quit..

## Python modules needed

- spacy
  - model: "en_core_web_trf"; python -m spacy download "en_core_web_trf"
    "en_core_web_trf" is needed at least to extract information from Gottfried Wilhelm Leibniz's Wikipedia-page
- spacy_sentence_bert
- wikipediaapi
- dateparser

