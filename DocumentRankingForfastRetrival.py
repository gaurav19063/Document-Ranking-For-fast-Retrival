import itertools
import math
import os
import  pickle

import re

import numpy
from nltk import word_tokenize
from nltk.corpus import stopwords
from num2words import num2words
import collections


def fixit(dict1):
    dict2 = {}

    for x in dict1.keys():
        dict2[x]=sorted(dict1[x][1:])
        dict2[x].insert(0,dict1[x][0])
    return dict2

def loadData_info():
    path="/home/gaurav/Desktop/IIITD/IR/Assignments/Assignment3/20_newsgroups/"
    all_doc = []
    dict_ordered_docs={}
    i=0
    for dirpath, dirs, files in os.walk(path):
        if i==0:
            i=i+1
            continue
        files=(sorted(files))
        dict_ordered_docs[dirpath]=files
    all_dirs_sorted=sorted(dict_ordered_docs)
    dict_ordered_docs_sorted={}
    for x in all_dirs_sorted:
        dict_ordered_docs_sorted[x]=dict_ordered_docs[x]
    # print(dict_ordered_docs_sorted)
    for x in dict_ordered_docs_sorted.keys():
        for y in  dict_ordered_docs_sorted[x]:
            # path2 =  x + "/" + y
            # print(y)
            all_doc.append(y)
            # f = open(path2, encoding='windows-1252')
            #
            # i = i + 1
            # print(i)
            # terms = word_tokenize(f.read())
            # terms = set(terms)
            # # print(terms)
            # for w in terms:
            #     # print(w)
            #     if w in dict1.keys():
            #         dict1[w][0] = dict1[w][0] + 1
            #         dict1[w].append(int(y))
            #
            #     else:
            #         dict1[w] = [1]
            #         dict1[w].append(int(y))
# print(dict1)
    return dict_ordered_docs_sorted,all_doc
def loadReviews():
    path="/home/gaurav/Desktop/IIITD/IR/Assignments/Assignment3/file.txt"
    f = open(path, encoding='windows-1252')
    # print(f.read())
    reviews = (f.read()).split()
    dict_review={}
    i=0
    # flag=0
    for x in reviews:
        if(i%2)==0:
            dict_review[reviews[i]]=int(reviews[i+1])
        i=i+1


    return dict_review


dir_info_sorted,alldocs=loadData_info()
# reviews=loadReviews()
# print(dir_info_sorted)
# print(alldocs)
# print(reviews)
# print(len(alldocs),len(reviews))
# dict_reviews={}
# i=0
# for x in alldocs:
#     i=i+1
#     dict_reviews[x]=reviews[str(i)]
# print(dict_reviews)
# with open('review_dict', 'wb') as handle:
#     pickle.dump(dict_reviews, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('review_dict', 'rb') as handle:
    review_dict = pickle.load(handle)
# print(review_dict)
# print(list(review_dict.keys()))
# for x in review_dict.keys():
#     print(x)
def choose_r(l):
    if l<10:
        return l

    return 10
def find_idf(df,l):
    return math.log10(l/df)

    # return  df
# def get_index(doc_words,w,y):
#     indexes=[index for index in range(len(doc_words)) if doc_words[index] == w]
#     # print(w,y,indexes)
#     return indexes



def make_champion_list(dir_info_sorted,l,review_dict):
    # print(dir_info_sorted)
    i=0
    dict1={}
    dict4={}
    dict1_positional={}
    for x in dir_info_sorted.keys():
        # print(x)

        for y in dir_info_sorted[x]:

            path=x+'/'+y
            # if i<50:
            #   print(path)
            print(i)
            list2 = [0] * l
            dict_temp = {}


            stop_words = set(stopwords.words('english'))

            f = open(path , encoding='ISO-8859-1')
            # print(n)
            doc_words = word_tokenize(f.read().lower()) #all words in a document
            doc_words1 = doc_words.copy()
            terms = set(doc_words1)                      #unique words in a document
            t=0
            for w in terms:
                dict_temp_positional = {}

                # print(t)

                # if w in stop_words:
                #     continue

                # if w in dict1.keys():
                #     dict1_positional[w][y]=[doc_words.count(w)]+[index for index in range(len(doc_words)) if doc_words[index] == w]
                #     dict1[w][y] = doc_words.count(w)
                #
                #
                # else:
                #     dict_temp_positional[y]=[doc_words.count(w)]+[index for index in range(len(doc_words)) if doc_words[index] == w]
                #     dict_temp[y] = doc_words.count(w)
                #     dict1_positional[w]=dict_temp_positional
                #     dict1=dict_temp
                #     # print(len(dict1))
                if w in dict1.keys():
                    # print(w)
                    dict1[w][y]=doc_words.count(w)
                    dict1_positional[w][y] = [doc_words.count(w)] + [index for index in range(len(doc_words)) if doc_words[index] == w]


                else:
                    dict_temp[y]=doc_words.count(w)
                    dict1[w]=dict_temp
                    dict_temp_positional[y] = [doc_words.count(w)] +[index for index in range(len(doc_words)) if doc_words[index] == w]
                    dict1_positional[w] = dict_temp_positional

                # print(w,dict1_positional[w])

                # print(doc_words)



            # print(dict1)
            # print(dict1_positional[w])
            # print(len(dict1_positional))
            # n = n + 1

            i = i + 1

            # print(dict1)
    dict2={}
    dict3_temp={}
    # print(len(dict1))
    c=0
    for x in dict1.keys():
        c=c+1
        print(c)
        dict_temp2={}
        # print(len(dict1[x]),l)

        # idf=find_idf(len(dict1[x]),l)
        sorted_dict = {k: v for k, v in sorted((dict1[x]).items(), key=lambda item: item[1],reverse=True)}
        # dict1[x] = list(sorted_dict)
        l2=len(dict1[x])
        high_list=list(dict(itertools.islice(sorted_dict.items(), choose_r(l2))))
        # print(list(high_list))
        low_list = list(dict(itertools.islice(sorted_dict.items(), choose_r(l2),l2)))
        q=0
        low_list_temp=low_list.copy()
        for z in low_list:
            if review_dict[z]>2:
                high_list.append(z)
                low_list_temp.remove(z)
            q=q+1
        low_list=low_list_temp.copy()

        dict_temp2['idf']=find_idf(len(dict1[x]),l)
        dict_temp2["high"]=high_list
        dict_temp2["low"] = low_list
        dict2[x]=dict_temp2

    # print(len(dict1))
    # print(len(dict1_positional))
    # print(len(dict2))

    return dict1,dict1_positional,dict2

def cosine_score_cal(query_vector,doc_vector):
    # print(len(query_vector),len(doc_vector))
    nom=numpy.dot(query_vector,doc_vector)
    denom=math.sqrt(numpy.dot(query_vector,query_vector))*math.sqrt(numpy.dot(doc_vector,doc_vector))
    return nom/denom
def gdScore(review_dict,d,Min,Max):
    return (review_dict[d]-Min)/(Max-Min)



def find_Ranked_docs(query,inverted_index_tf_dict1,dict_positional,champ_dict1,review_dict,k):
    query_words=word_tokenize(query)
    # stop_words = set(stopwords.words('english'))
    # for x in query_words:
        # if x  in stop_words:
        #     query_words.remove(x)
    print(query_words)
    # l=len(inverted_index_tf_dict1)
    query_vector=[]
    query_distinct=list(set(query_words))
    print(query_distinct)
    all_docs_high=[]
    # for x in query_distinct:
    #     tf=query_words.count(x)
    #     query_vector.append(champ_dict1[x]['idf']*math.log2(1+tf))
    #     all_docs_high=all_docs_high+champ_dict1[x]['high']
    for x in inverted_index_tf_dict1.keys():
        if x in query_distinct:
            tf=query_words.count(x)
            idf=champ_dict1[x]['idf']
            query_vector.append(idf*math.log2(1+tf))
        else:
            query_vector.append(0)

    # print(sum(query_vector))
    # print(len(query_vector))




    all_docs_low=[]
    # print(query_vector)
    if len(all_docs_high)<k:
        for x in query_distinct:

            all_docs_low = all_docs_low + champ_dict1[x]['low']
    all_docs=all_docs_low+all_docs_high
    print(all_docs)
    print(len(all_docs))
    cosine_score_dict={}
    min_static_score=min(review_dict.values())
    max_static_score = max(review_dict.values())
    i=0
    for d in all_docs:
        doc_vector=[]
        for w in inverted_index_tf_dict1.keys():
            if d not in inverted_index_tf_dict1[w].keys():
                doc_vector.append(0)
            else:
                idf=champ_dict1[w]['idf']
                tf=inverted_index_tf_dict1[w][d]
                doc_vector.append(idf*math.log2(tf))
        i=i+1
        # print(i)
        # cosine_score_vector.append(query_vector,doc_vector)

        cosine_score_dict[d]=cosine_score_cal(query_vector,doc_vector)+gdScore(review_dict,d,min_static_score,max_static_score)
        # cosine_score_dict[d] = cosine_score_cal(query_vector, doc_vector)

        # print(len(doc_vector))
        # print(sum(doc_vector))
    # print(i)
    print(cosine_score_dict)
    dict3 = sorted(cosine_score_dict, key=cosine_score_dict.get, reverse=True)
    print(champ_dict1['sink'])

    print(dict3[0:k])








    # list_high=[]
    # for x in list(set(query_words)):
    #     list_high=list_high+champ_dict1[x]['high']
    # if k>len(list_high):
    #     for x in query_words:
    #         list_high=list_high+champ_dict1[x]['low']
    # print("done")






    return 0


# inverted_index_tf_dict,positional_index ,champ_dict=make_champion_list(dir_info_sorted, len(alldocs),review_dict) #function calling for inverter index with champion list
# for x in positional_index.keys():
#     print(x,positional_index[x])

# print("dict received")
# with open('inverted_index_dict.pickle', 'wb') as handle:
#     pickle.dump(inverted_index_tf_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
# print("stored")
# with open('dict_positional.pickle', 'wb') as handle:
#     pickle.dump(positional_index , handle, protocol=pickle.HIGHEST_PROTOCOL)
# with open('champ_dict.pickle', 'wb') as handle:
#     pickle.dump(champ_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
# inverted_index_tf_dict1={}
# dict_positional={}
# champ_dict1={}
with open('inverted_index_dict.pickle', 'rb') as handle:
    inverted_index_tf_dict1 = pickle.load(handle)
with open('dict_positional.pickle', 'rb') as handle:
    dict_positional = pickle.load(handle)
with open('champ_dict.pickle', 'rb') as handle:
    champ_dict1 = pickle.load(handle)
#



# print("pickle_done")
# for x in inverted_index_tf_dict1.keys():
#     print(x,inverted_index_tf_dict1[x])
# for x in dict_positional.keys():
#     print(x,dict_positional[x])
# for x in champ_dict1.keys():
#     print(x,champ_dict1[x])
# print(len(inverted_index_tf_dict1))
# print(len(dict_positional))
# print(len(champ_dict1))
query="1"
while(query!='-1'):
    print("Enter Query: ")

    query=input()
    print("Enter k value: ")
    k=int(input())
    # k=10
    find_Ranked_docs(query,inverted_index_tf_dict1,dict_positional,champ_dict1,review_dict,k)
