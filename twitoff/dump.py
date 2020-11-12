import spacy
import pickle

if __name__ == "__main__":
    nlp = spacy.load('en_core_web_sm')

    f = open('final_pickle', 'wb')
    pickle.dump(nlp, f)
    f.close()