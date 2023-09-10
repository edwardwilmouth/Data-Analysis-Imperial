from fuzzywuzzy import fuzz
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.corpus import words
import nltk
import csv
import string
import re
from difflib import get_close_matches
#from statistics import mode
import Levenshtein
from english_words import get_english_words_set
from tkinter import *
import tkinter as tk
import pandas as pd
from tkinter import filedialog
from tkinter.filedialog import askopenfile

import pandas as pd
import numpy as np
from datetime import datetime

'''
FOR NEURAL NETWORK

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
'''


nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('words', quiet=True)

def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def stop(sentence):  # remove stopwords
    stop_words = set(stopwords.words('english'))
 
    word_tokens = word_tokenize(sentence)
    # converts the words in word_tokens to lower case and then checks whether
    #they are present in stop_words or not
    filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
    #with no lower case conversion
    filtered_sentence = []
    
    for w in word_tokens:
        if w not in stop_words and w not in string.punctuation:
            filtered_sentence.append(w)

    return filtered_sentence

def readfile(path):  # open file
    with open(path, 'r') as theFile:
        reader = csv.DictReader(theFile)
        headers = reader.fieldnames
        lines = { key : list([]) for key in headers}
        #lines['year'] = ['teh']
        #print(lines)
        for line in reader:
            # line is {'year': '1958', 'month': '3', 'decimal date': '1958.2027',
            # 'average': '315.70', 'deseasonalized': '314.43', 'ndays': '-1', 
            # 'sdev': '-9.99', 'unc': '-0.99'}
            for key in line:
                temp = lines[str(key)]
                temp.append(line[key])
                lines[key] = temp
                
                #print(line[key], key)
        #print(lines[headers[0]])
        #print(lines['average'])
        #print(headers)
        return headers, lines

# information would be [year, month, decimal date etc.]
def search(header, body, data):  # final step - looking for correct row
    
    headers, lines = data
    uniqueHeaderSearch = set()
    for i in header:
        uniqueHeaderSearch.add(i[0])
        #uniqueHeaderSearch.add(headers.index(i[0]))
    #print(uniqueHeaderSearch)
    #print(body)

    listforkey = []
    for i in range(len(list(lines.values())[0])):
        listforkey.append(i)
    #print(list(lines.values())[0])

    extras = set()
    lineno2acc = dict.fromkeys(listforkey, 0)
    for i in body:
        count = 0
        #print(i)
        for j in lines[headers[i[2]]]:
            extras.add(headers[i[2]])
            if j == i[0] and i[1] > 0.55:
                # print(i)
                lineno2acc[count] += i[1] # counts.append(count)
            count += 1
    keys = list(lineno2acc.keys())
    values = list(lineno2acc.values())
    # mode = keys[values.index(max(values))]
    m = max(values)
    items = [i for i, j in enumerate(values) if j == m]
    mode = []
    for i in items:
        mode.append(keys[i])
    uniqueHeaderSearch = list(uniqueHeaderSearch)
    #if len(mode) > 1:
    return uniqueHeaderSearch, mode, extras


def syns(word):  # Synonyms
    ls = []
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            ls.append(l.name())
            #print(ls)
    return ls

def isfloat(item):

    # A float is a float
    if isinstance(item, float):
        return True

    # Ints are okay
    if isinstance(item, int):
        return True

   # Detect leading white-spaces
    if len(item) != len(item.strip()):
        return False

    # Some strings can represent floats or ints ( i.e. a decimal )
    if isinstance(item, str):
        # regex matching
        int_pattern = re.compile("^[0-9]*$")
        float_pattern = re.compile("^[0-9]*.[0-9]*$")
        if float_pattern.match(item) or int_pattern.match(item):
            return True
        else:
            return False

def question(query, headers, lines):  # Removing stopwords, looking for synonyms in header
    web2lowerset = get_english_words_set(['web2'], lower=True)
    #for i in lines:
    #    pass
    headerConnect = []
    CSVConnect = []

    for a in stop(query):
        ls = get_close_matches(a, web2lowerset)
        ls.append(a)

        if a not in words.words() and a.lower() not in words.words() and not isfloat(a):
            temp = []
            for i in ls:
                for j in syns(i):
                    temp.append(j)
            for i in temp:
                ls.append(i)
            ls.remove(a)
        else:
            for i in syns(a):
                ls.append(i)
        ls = list(set(ls))
        for i in ls:
            for j in headers:
                connection = fuzz.token_sort_ratio(i, j)
                if connection > 65:
                    headerConnect.append([j, connection])
                    #print(difflib.SequenceMatcher(None, 'February', 'Feb').ratio())
                    #print(Levenshtein.ratio('Feb', 'February'))
            value = 0
            oldc = 0
            countheaders = 0
            data = (oldc, value, countheaders)
            for j in lines.values():
                for k in j:
                    connection = Levenshtein.ratio(i, k)
                    if connection > oldc:
                        oldc = connection
                        value = k
                        data = (connection, k, countheaders, i)

                countheaders += 1
            CSVConnect = Connect(CSVConnect, data)
            
    #CSV = []
    #for i in CSVConnect:
    #    CSV.append(i[0])
    return headerConnect, CSVConnect

def Connect(CSV, data):
    oldc, value, ch, original = data
    if CSV == []:
        CSV.append([value, oldc, ch, original])
        return CSV
    else:
        for j in range(len(CSV)):
            i = CSV[j]
            if i[2] == ch:
                if oldc > i[1]:
                    #if CSV[] == CSV[]:
                    #    CSV.pop(j)
                    # Need to delete that entry
                    # Then add this entry
                    CSV.pop(j)
                    CSV.append([value, oldc, ch, original])
                    return CSV
                else:
                    if oldc == i[1]:
                        CSV.append([value, oldc, ch, original])
                        return CSV
                    else:
                        return CSV
            else:
                CSV.append([value, oldc, ch, original])
                return CSV         

def printer(uniqueHeaderSearch, mode, extras, lines):  # Prints results
    print('\033[1m' + "Here's what I found: ")
    for i in mode:
        for j in uniqueHeaderSearch:
            print('\033[1m', '\033[92m', string.capwords(j) + ": " + string.capwords(lines[j][i]), end = "  ")
        print('\033[0m', "", end = "")
        if len(mode) > 1:
            for j in extras:
                print(string.capwords(j) + ": " + string.capwords(lines[j][i]), end = "  ")
        print()

'''        
FOR NEURAL NETWORK

def build_model(input_dim, output_dim):
    model = Sequential()
    model.add(Dense(64, activation='relu', input_shape=(input_dim,)))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(output_dim))  # Output layer for concentration prediction
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def convert_query_to_features(query):
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts([query])
    tokens = tokenizer.texts_to_sequences([query])[0]

    # Extract the date from the query (optional)
    date_str = None
    for i, token in enumerate(tokens):
        if token == 'date' and i + 1 < len(tokens):
            date_str = tokenizer.index_word.get(tokens[i + 1])
            break

    if date_str is None:
        print("Error: Date not found in the query.")
        return None

    # Convert the date to a numerical representation (e.g., timestamp)
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        date_timestamp = int(date.timestamp())
    except ValueError as e:
        print(f"Error: Invalid date format in the query. {e}")
        return None

    # Other preprocessing steps (if needed) for additional parts of the query

    # Return the numerical features (timestamp in this case)
    return date_timestamp, tokens
'''


def main():

    path = input("File Directory: ")
    
    '''
    COULD PUT INTO AN APPLICATION:
    #window = tk.Tk()
    #window.mainloop()
    #window.geometry("400x300")  # Size of the window 
    #window.title(path)
    '''

    query = input("Query: ")
    count = 0
    hardCoded = True
    if hardCoded:
        l = 3
        printProgressBar(count, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
        headers, lines = readfile(path)
        count += 1
        printProgressBar(count, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
        header, body = question(query, headers, lines)
        count += 1
        printProgressBar(count, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
        uniqueHeaderSearch, mode, extras = search(header, body, (headers, lines))
        count += 1
        printProgressBar(count, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
        #print(temp)
        printer(uniqueHeaderSearch, mode, extras, lines)
    else:
        pass

        '''
        SIMPLE NEURAL NETWORK DESIGN

        # Load your spreadsheet data into a pandas DataFrame
        # For simplicity, let's assume your CSV file has columns 'date' and 'concentration'
        data = pd.read_csv(path)

        # Function to convert the query to features


        # Build the neural network model


        queries = [
            "What was the concentration on 2023-08-06?",
            "Tell me the concentration on 2022-12-25.",
            "Concentration on 2021-10-15?"
        ]

        # Get features for each query and pad sequences to a fixed length
        features_list = []
        for query in queries:
            features, _ = convert_query_to_features(query)
            features_list.append(features)

        # Pad sequences to a fixed length (e.g., 1) for feeding into the neural network
        max_sequence_length = 1
        padded_features = pad_sequences(features_list, maxlen=max_sequence_length)

        # Load your neural network model
        input_dim = 1  # Adjust this based on the dimension of your input features
        output_dim = 1  # Adjust this based on the number of output values (e.g., concentration)
        model = build_model(input_dim, output_dim)

        # Train your neural network (you should use your own training data)
        # model.fit(X_train, y_train, epochs=50, batch_size=16)

        # Get predictions for the queries using the trained model
        predictions = model.predict(padded_features)

        # Print the predictions
        print("Predictions:")
        for i, query in enumerate(queries):
            print(f"Query: {query} - Concentration: {predictions[i][0]}")
        '''

if __name__ == "__main__":
    main()
