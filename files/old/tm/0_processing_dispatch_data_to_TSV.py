# the script converts Dispatch data into TSV and prepares text for topic modeling

import re, os, io
import gensim
from gensim.utils import simple_preprocess
import pandas as pd

source = "./Dispatch/"
target = "./Dispatch_Processed_TSV/"  # needs to be created beforehand!

def remove_words(texts, word_list_filter):
    return [[word for word in simple_preprocess(str(doc)) if word not in word_list_filter] for doc in texts]

def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations

def convertDispatchToCSV(source, target, YEAR):
    print("Collecting data for year: %s" % YEAR)
    issueVar = []
    lof = os.listdir(source)
    for f in lof:
        if f.startswith("dltext"):  # fileName test
            c = 0  # technical counter
            with open(source + f, "r", encoding="utf8") as f1:
                text = f1.read()
                date = re.search(r'<date value="([\d-]+)"', text).group(1)

                if date[:4] == str(YEAR):
                    split = re.split("<div3 ", text)

                    for s in split[1:]:
                        c += 1
                        s = "<div3 " + s  # a step to restore the integrity of items

                        try:
                            unitType = re.search(
                                r'type="([^\"]+)"', s).group(1)
                        except:
                            unitType = "noType"

                        try:
                            header = re.search(
                                r'<head.*</head>', s).group(0)
                            header = re.sub("<[^<]+>", "", header)

                        except:
                            header = "NO HEADER"

                        text = s
                        text = re.sub("<[^<]+>", " ", text)
                        text = re.sub(r"\t", " ", text)
                        text = re.sub(" +\n|\n +", "\n", text)
                        text = text.strip()
                        text = re.sub("\n+", ";;; ", text)
                        text = re.sub(" +", " ", text)
                        text = re.sub(r" ([\.,:;!])", r"\1", text)

                        itemID = date + "_" + unitType + "_%04d" % c

                        if len(re.sub("\W+", "", text)) != 0:
                            var = "\t".join(
                                [itemID, date, unitType, header, text])
                            issueVar.append(var)

    print("\tcollected: %d items" % len(issueVar))
    issueNew = "\n".join(issueVar)
    header = "\t".join(["id", "date", "type", "header", "text"])
    final = header + "\n" + issueNew


    # Now, we prepare text data for TM (into a separate column)
    entitiesFinalStringIO = io.StringIO(final)
    df = pd.read_csv(entitiesFinalStringIO, sep="\t", header=0)

    dispatch = df
    # drop=True -- use it to avoid creating a new column with the old index values
    dispatch = dispatch.reset_index(drop=True)

    # add a column with all dates of each month changed to 1 (we can use that to aggregate our data into months)
    dispatch["month"] = [re.sub("-\d\d$", "", str(i)) for i in dispatch["date"]]

    # reorder columns
    dispatch = dispatch[["id", "month", "date", "type", "header", "text"]]

    dispatch["month"] = pd.to_datetime(dispatch["month"], format="%Y-%m")
    dispatch["date"] = pd.to_datetime(dispatch["date"], format="%Y-%m-%d")

    dispatch = dispatch[dispatch.type != "ad-blank"]
    dispatch = dispatch.reset_index(drop=True)

    dispatch["textData"] = dispatch["text"]
    dispatch["textData"] = [re.sub("\W+", " ", str(i).lower()) for i in dispatch["textData"]]
    dispatch["textData"] = [re.sub(" +", " ", str(i).lower()) for i in dispatch["textData"]]

    dispatch["textDataLists"] = list(sent_to_words(dispatch["textData"].copy()))

    # you can expand the stop word list by adding more high frequency words
    stop_words_custom = ["the", "of", "and", "to", "in", "a", "that", "for", "on", "was", "is", "at", "be", "by",
                    "from", "his", "he", "it", "with", "as", "this", "will", "which", "have", "or", "are",
                    "they", "their", "not", "were", "been", "has", "our", "we", "all", "but", "one", "had",
                    "who", "an", "no", "i", "them", "about", "him", "two", "upon", "may", "there", "any",
                    "some", "so", "men", "when", "if", "day", "her", "under", "would", "c", "such", "made",
                    "up", "last", "j", "time", "years", "other", "into", "said", "new", "very", "five",
                    "after", "out", "these", "shall", "my", "w", "more", "its", "now", "before", "three",
                    "m", "than", "h", "th", "o'clock", "o", "old", "being", "left", "can", "s", "man", "only", "same",
                    "act", "first", "between", "above", "she", "you", "place", "following", "do", "per",
                    "every", "most", "near", "us", "good", "should", "having", "great", "also", "over",
                    "r", "could", "twenty", "people", "those", "e", "without", "four", "received", "p", "then",
                    "what", "well", "where", "must", "says", "g", "large", "against", "back", "through",
                    "b", "off", "few", "me", "sent", "while", "make", "number", "many", "much", "give",
                    "six", "down", "several", "high", "since", "little", "during", "away", "until",
                    "each", "year", "present", "own", "t", "here", "d", "found", "reported",
                    "right", "given", "age", "your", "way", "side", "did", "part", "long", "next", "fifty",
                    "another", "1st", "whole", "10", "still", "among", "3", "within", "get", "named", "f",
                    "l", "himself", "ten", "both", "nothing", "again", "n", "thirty", "eight", "took",
                    "never", "came", "called", "small", "passed", "just", "brought", "4", "further",
                    "yet", "half", "far", "held", "soon", "main", "8", "second", "however", "say",
                    "heavy", "thus", "hereby", "even", "ran", "come", "whom", "like", "cannot", "head",
                    "ever", "themselves", "put", "12", "cause", "known", "7", "go", "6", "once", "therefore",
                    "thursday", "full", "apply", "see", "though", "seven", "tuesday", "11", "done",
                    "whose", "let", "how", "making", "immediately", "forty", "early", "wednesday",
                    "either", "too", "amount", "fact", "heard", "receive", "short", "less", "100",
                    "know", "might", "except", "supposed", "others", "doubt", "set", "works"]

    # TEXT CLEANING
    dispatch["textDataLists"] = remove_words(dispatch["textDataLists"], stop_words_custom)
    dispatch = dispatch[["id", "month", "date", "type", "header", "text", "textDataLists"]]
    dispatch.to_csv(target + "Dispatch_%s_tmReady.tsv" % str(YEAR), sep="\t", index=False)


convertDispatchToCSV(source, target, 1860)
convertDispatchToCSV(source, target, 1861)
convertDispatchToCSV(source, target, 1862)
convertDispatchToCSV(source, target, 1863)
convertDispatchToCSV(source, target, 1864)
convertDispatchToCSV(source, target, 1865)
