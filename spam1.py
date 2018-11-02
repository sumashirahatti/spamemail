import os
from collections import Counter
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split as tts
from sklearn.metrics import accuracy_score
import cPickle as c

def save(classifier, name):
    with open(name, 'wb') as fp:
        c.dump(classifier, fp)
    print "saved"



def make_dict():
    directory = "emails/"
    root = os.listdir(directory)
    emails = [directory + email for email in root]
    words = []
    count = len(emails)
    for email in emails:
        y = open(email)
        z = y.read()
        words += z.split(" ")
        print count
        count -= 1

    for j in range(len(words)):
        if not words[j].isalpha():
            words[j] = ""

    dictionary = Counter(words)
    del dictionary[""]
    return dictionary.most_common(3000)


def make_feature_vector(dictionary):
    directory = "emails/"
    root = os.listdir(directory)
    emails = [directory + email for email in root]
    feature_set = []
    labels = []
    count = len(emails)

    for email in emails:
        datalist = []
        y = open(email)
        words = y.read().split(' ')
        for key in dictionary:
            datalist.append(words.count(key[0]))
        feature_set.append(datalist)

        if "ham" in email:
            labels.append(0)
        if "spam" in email:
            labels.append(1)
        print count
        count = count - 1
    return feature_set, labels


dict = make_dict()
features, labels = make_feature_vector(dict)
#print len(features),len(labels)
p_train,p_test,q_train,q_test=tts(features,labels,test_size=0.2)
classifier=MultinomialNB()
classifier.fit(p_train,q_train)
preds=classifier.predict(p_test)
print accuracy_score(q_test,preds)
save(classifier, "model.mdl")


