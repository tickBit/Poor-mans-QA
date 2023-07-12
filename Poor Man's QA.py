"""
The first prompt asks a Wikipedia page of a person.
The second prompt is question about the person.
"""

# the following is used for NER extraction and grammar parsing...
import spacy
nlp = spacy.load('en_core_web_trf')

# the following is used for semantic similarity
import spacy_sentence_bert
nlp_sim = spacy_sentence_bert.load_model('en_allenai_specter')

import wikipediaapi
import dateparser

wiki_wiki = wikipediaapi.Wikipedia('en')

BIRTH = 0
PROFESSION = [1,2,3]

# Questions to ask, understans two types of questions. The second question has three examples.
questions = ["When was PERSON born?", "What did PERSON do?", "What is the profession of PERSON?", "What field was PERSON on?"]

def get_full_name(sent0):
    # get the full name of the PERSON in the first sentence
    full_name = ''
    final_full_name = ''

    # search for the first PERSON entity in the first sentence
    for ent in sent0.ents:
        if ent.label_ == 'PERSON':
            full_name = ent.text
            full_name += " " + ent.root.head.text

    for n in nlp(full_name):
        # check if n is a proper noun
        if n.pos_ == 'PROPN':
            final_full_name += n.text + " "
    final_full_name = final_full_name.strip()
    
    return final_full_name

def get_birth_date(full_name):

    # get the birth date of the PERSON in the first sentence
    dates = []

    for ent in sent0.ents:
        # the name of the person is in variable final_full_name
        if ent.label_ == 'PERSON':
            if ent.root.head.text == full_name.split()[-1]:
                # get the date related to root entity
                for child in ent.root.head.children:
                
                    if child.ent_type_ == 'DATE':
                        for token in child.subtree:
                            if token.ent_type_ == 'DATE':
                                dates.append(token.text)
        elif ent.label_ == 'DATE':
            dates.append(ent.text)

    if len(dates) == 0:
        return None, None
    
    # format the date
    if len(dates) == 6:
        bdate = dates[0] + ' ' + dates[1] + ' ' + dates[2]
        ddate = dates[3] + ' ' + dates[4] + ' ' + dates[5]
    elif len(dates) == 3:
        bdate = dates[0]
        ddate = dates[2]
    elif len(dates) == 2:
        bdate = dates[0]
        ddate = dates[1]
    elif len(dates) == 1:

        dates = str(dates[0]).replace(' – ', '-').split("-")
        bdate = dates[0]
        
        try:
            ddate = dates[1]
        except:
            ddate = None

    bdate = dateparser.parse(bdate)
    bdate = bdate.strftime('%d %B %Y')
    
    if ddate != None:
        ddate = dateparser.parse(ddate)
        ddate = ddate.strftime('%d %B %Y')

    return bdate, ddate

def get_profession(sent0):
    # what was the profession of the PERSON in the first sentence
    professions = []

    for token in sent0:
        if token.pos_ == 'AUX':
        
            for child in token.head.children:
                if child.dep_ == 'attr':
                    skip = False
                    for tok in child.subtree:
                        if tok.dep_ == 'acl': break
                        if tok.pos_ == "ADJ": skip = False
                        # if previous token is ADP, skip the none
                        if tok.dep_ == 'poss':
                            skip = True
                        if tok.pos_ == 'NOUN' and skip == False:
                            professions.append(tok.text)

    # compuound for example "computer" and "scientist" to "computer scientist"
    for p in professions:
        for token in sent0:
            if token.dep_ == "amod" and token.head.text == p:
                if token.text[0] != token.text[0].upper():
                    # if p is earlier in the sentence than token.text, add p to token.text
                    if sent0[:token.i].text.find(p) != -1:
                        professions.append(p + ' ' + token.text)
                    else:
                        professions.append(token.text + ' ' + p)

            if token.dep_ == 'compound' and token.head.text == p:
                if token.text[0] != token.text[0].upper(): professions.append(token.text + ' ' + p)

    # remove for example separate "computer" and "scientist", if "computer scientist" now exists
    toRemove = []

    for p1 in professions:
        pp = p1.split()
        if len(pp) > 1:
            for p in pp:
                toRemove.append(p)
    
    # remove items that are in toRemove
    professions = [x for x in professions if x not in toRemove]

    for p in professions:
    # remove items, that have a verb in them
        if len(nlp(p)) > 1:
            for token in nlp(p):
                if token.pos_ == 'VERB':
                    professions.remove(p)

    return professions

while True:

    person = input("Enter a person to know about (Wikipedia): ")    

    page_py = wiki_wiki.page(person)

    if page_py.exists() == False:
        print("No such page exists. Try again.")
        continue

    page_summary = page_py.summary

    doc = nlp(page_summary)

    sentences = list(doc.sents)
    sentence = sentences[0]

    filtered_sentence = [w for w in sentence if w.text.strip() != '']
    sent0 = nlp(' '.join(map(str, filtered_sentence)))

    full_name = get_full_name(sent0)

    while True:
        question = input("Ask a question about the person with his/her name: ")
        if question.strip() == "": break

        # find similar semantic similarity between the question and the question in the list
        similarity = []
        for q in questions:
            similarity.append(nlp_sim(q).similarity(nlp_sim(question)))

        # get the index of the most similar question
        index = similarity.index(max(similarity))

        # is question similar to the first question?
        if index == 0:

            # get the birth date of the person
            bdate, ddate = get_birth_date(full_name)
            
            if bdate != None:
                print("The birth date of {} is {} ".format(full_name, bdate.replace('–','')))

            if ddate != None:
                print("The death date of {} is {}.".format(full_name, ddate))
                            
            if bdate == None and ddate == None:
                print("I don't know the birthday of of {}.".format(full_name))
                
        elif index in [1,2,3]:
            professions = get_profession(sent0)
            professions_str = ''

            for p in range(len(professions)-1):
                professions_str += professions[p] + ', '
            professions_str += professions[-1] + "."

            print("The profession of {} was/is {} ".format(full_name, professions_str))

        

