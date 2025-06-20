import re, unicodedata
import collections
import num2words
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import string
   
#Data Preprocessing:
stop = []
with open('Stopword-List.txt', 'r') as f:
    for x in f:
        stop += x.split()

print(sorted(stop))

def stopwords_removal(x):
    line_without_stop = [word for word in x.split() if not word in stop]
    return line_without_stop

def stopwords_removal_words(x):
    if not x in stop:
        return False
    else:
        return True


def clean(term):
    ps = PorterStemmer() 
    term = term.lower()
    term = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", term) #Remove Unicode
    term = re.sub(r'[^\w\s]','',term)
    term = ps.stem(term)
    return term

ps = PorterStemmer()
ps.stem("Australian")

#Inverted Index:

inverted = {}
tokens = []
for i in range(1, 31):
    with open('Dataset/' + str(i) + '.txt', 'r') as f:
        # Removing punctations manually because some conventions are modified.
        f = f.read().replace(".", "").replace("n't", " not").replace("'", "").replace("]", " ").replace("[",
                                                                                                        "").replace(",",
                                                                                                                    " ").replace(
            "?", "").replace("\n", " ").replace("-", " ").replace('/', " ").split()
        for line in f:
            line = stopwords_removal(line)
            for word in line:
                tokens.append(clean(word))
                word = clean(word)
                if word in inverted:
                    inverted[word].add(i)
                else:
                    inverted[word] = {i}
print("Inverted Index: ")
for x in sorted(inverted.items(), key=lambda x: (x[0],x[1])):
    print(x[0],": ",sorted(x[1]))
print("Total no. of tokens: ",len(inverted))

ps=PorterStemmer()
def search(query):
  for k,v in inverted.items():
    if k == ps.stem(query):
      return (v)

#Boolean Queries:

posting = {}
docs = []
operand = []


def precedence(op):
    if op == 'not':
        return 1
    if op == 'and':
        return 2
    if op == 'or':
        return 3
    return 0


def applyOp(term1_set, term2_set, op):
    if term1_set and term2_set and op == 'and':
        posting = term1_set.intersection(term2_set)
        return posting
    elif op == 'and':
        return {}
    elif term1_set and term2_set and op == 'or':
        posting = term1_set.union(term2_set)
        return posting
    elif term1_set and op == 'or':
        return term1_set
    elif term2_set and op == 'or':
        return term2_set
    elif (term1_set and op == 'not') or (term2_set and len(term2_set) == 1 and op == 'not'):
        posting = set(range(1, 31)).symmetric_difference(term1_set)
        return posting
    elif op == 'not':
        return {}


def query_processing(tokens):
    for x in tokens:
        if x == ' ':
            continue
        elif x == '(':
            operand.append(x)
        elif x != 'and' and x != 'or' and x != 'not' and x != '(' and x != ')':
            docs.append(search(x))
            print(search(x))
        elif x == ')':

            while len(operand) != 0 and operand[-1] != '(':
                op = operand.pop()
                if op == 'not':
                    val1 = docs.pop()
                    val2 = {}
                else:
                    val1 = docs.pop()
                    val2 = docs.pop()

                docs.append(applyOp(val1, val2, op))

            # pop opening brace.
            operand.pop()


        else:
            while (len(operand) != 0 and precedence(operand[-1]) >= precedence(x)):
                if operand[-1] == 'not':
                    val1 = docs.pop()
                    val2 = {}
                    op = operand.pop()
                    docs.append(applyOp(val1, val2, op))
                else:
                    val2 = docs.pop()
                    val1 = docs.pop()
                    op = operand.pop()
                    docs.append(applyOp(val1, val2, op))
            operand.append(x)
    while operand:
        op = operand.pop()
        if op == 'not':
            if len(docs) == 0:
                docs.append({})
                break
            val1 = docs.pop()
            val2 = {}
            if not val1:
                val2 = {0}
                docs.append(applyOp({}, val2, op))
            else:
                docs.append(applyOp(val1, val2, op))
        else:
            val2 = docs.pop()
            val1 = docs.pop()
            docs.append(applyOp(val1, val2, op))
    return docs[-1]


#Positional Index:

positional={}
for i in range(1,31):
  with open('Dataset/'+str(i)+'.txt', 'r') as f:
    # Removing punctations manually because some conventions are modified.
    f = f.read().replace(".","").replace("n't"," not").replace("'","").replace("]"," ").replace("[","").replace(","," ").replace("?","").replace("\n"," ").replace("-"," ").replace('/'," ").split()
    pos=-1
    for word in f:
        pos=pos+1
        if not stopwords_removal_words(word):
            tokens.append(clean(word))
            word=clean(word)
            if word in positional:
                if i in positional[word]:
                    positional[word][i].add(pos)
                else:
                    positional[word][i]={pos}
            else:
                positional[word] = {i: {pos}}
print("Positional Index: ")
print()
for x in sorted(positional.items(), key=lambda x: (x[0],x[1])):
    if(x[1]):
      print(x[0])
      for y in sorted(x[1].items(), key=lambda y: (y[0],y[1])):
        print(y[0],": ",sorted(y[1]))
    else:
      print(x[0], ": ", sorted(x[1]))


#Proximity Queries:
intersect = set()


def positional_list(word):
    if ps.stem(word) in positional:
        list_ = positional[ps.stem(word)]
        result = set()
        for key, value in list_.items():
            result.add(key)
        return list_, result
    else:
        list=[]
        return list,set()


def document_positions(pos1_list, pos2_list, skip, fileNo):
    res=[]
    for pos1 in pos1_list:
        for pos2 in pos2_list:
            if (abs(pos1 - pos2) ) <= skip:
                res.append(fileNo)
    return res


def proximity(q):
    result=[]
    #     q= ["feature", "track", "/5"]
    w1 = clean(q[0])
    w2 = clean(q[1])
    q[2] = re.sub(r"/", "", q[2])
    skip = int(q[2])
    w1_posting, res1 = positional_list(w1)
    w2_posting, res2 = positional_list(w2)
    intersect = res1.intersection(res2)
    intersect = sorted(intersect)

    if intersect is not None:
        for x in intersect:
            index1 = []
            index2 = []
            for y in range(len(w1_posting)):
                for key, value in w1_posting.items():
                    if key == x:
                        index1 = value
            for y in range(len(w2_posting)):
                for key, value in w2_posting.items():
                    if key == x:
                        index2 = value
            result.append(document_positions(index1, index2, skip, x))
    print(result)
    result_=[]
    for x in result:
        if x and x[0]:
          result_.append(x[0])
        elif x:
            result_.append(x)
    print(result_)
    return (sorted(result_))


with open("inverted_index.txt", "w") as f:
    f.write("Inverted Index:\n")
    for term, doc_ids in sorted(inverted.items(), key=lambda x: (x[0], x[1])):
        f.write(f"{term}: {sorted(doc_ids)}\n")
    f.write(f"\nTotal number of tokens: {len(inverted)}\n")

with open("positional_index.txt", "w") as f:
    f.write("Positional Index:\n\n")
    for term, doc_map in sorted(positional.items(), key=lambda x: (x[0], x[1])):
        f.write(f"{term}\n")
        for doc_id, positions in sorted(doc_map.items()):
            f.write(f"{doc_id}: {sorted(positions)}\n")
        f.write("\n")

# Use spaces with brackets
# All Gold-Queries are tested for Simple Query Test Cases
# Complex Query Test Case:   ( psl or t20 ) and ( cricket or rohit or india ) and ( not ( impossible or pakistan ) )
# Output:                    {3, 5, 6, 8, 13, 14, 23, 24, 25}
# Phrasal Query Test Case:   t20 world
# Output:                    2 3 5 6 8 12 13 14 18 24 25
# Proximity Query Test Case: t20 cup /1                                                      In Proximity Query, stop words are not counted  between words.
# Output:                    2 3 5 6 8 12 13 14 18 24 25
def main():
    label["text"] = ""
    query = query_field.get()
    if query == "":
        label["text"] = " Kindly Enter Query For Search"
    else:
        query = query.lower()
        query_words = query.split()
        if ('and' in query_words or 'or' in query_words or 'not' in query_words or len(
                query_words) == 1):  # Boolean Queries
            res=sorted(query_processing(query_words))
            if res:
                label1["text"] = "Documents: "
                str1=''
                for x in res:
                    str1=str1+str(x)+', '
                label["text"] = str1
            else:
                label["text"] = " No Documents Retrieved For this Query"
        elif len(query_words) == 2:  # Phrasal Queries
            query_words.append("/0")
            res=proximity(query_words)
            if res:
                label1["text"] = "Documents: "
                str1 = ''
                for x in res:
                    str1 = str1+str(x) + ', '
                label["text"] = str1
            else:
                label["text"] = " No Documents Retrieved For this Query"

        else:
            res = proximity(query_words)
            if res:
                label1["text"] = "Documents: "
                str1 = ''
                for x in res:
                    str1 = str1+str(x) + ', '
                label["text"] = str1
            else:
                label["text"] = " No Documents Retrieved For this Query"  # Proximity Queries





from tkinter import *
import tkinter as tk
from PIL import ImageTk

if __name__ == "__main__":

    root = Tk()
    bgimg = ImageTk.PhotoImage(file="image1.png")
    # Specify the file name present in the same directory or else
    # specify the proper path for retrieving the image to set it as background image.
    limg = Label(root, i=bgimg)
    limg.place(x=0, y=0, relwidth=1, relheight=1)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.title("Boolean Retrival Model ")
    root.geometry("500x300")
    query = Label(root, text="Enter Query: ", bg="white", font=("Helvetica", 14))
    query.grid(row=4, column=0)
    query.place(anchor='center', relx=.15, rely=.1)
    query_field = Entry(root)
    query_field.bind("<Return>", query_field.focus_set())
    query_field.grid(row=4, column=1, ipadx="150")
    query_field.place(anchor='center', relx=.65, rely=.1, width=300)
    query = query_field.get()
    submit = Button(root, text="Search", fg="Black", bg="light green", command=main, font=("Helvetica", 14))
    submit.grid(row=30, column=1)
    submit.place(anchor='center', relx=.5, rely=.3)
    label = Label(root, text='', bg="white", fg="black", font=("Helvetica", 14))
    label.grid(row=40, column=1)
    label.place(anchor='center', relx=.5, rely=.7)
    label1 = Label(root, text='', bg="white", fg="black", font=("Helvetica", 20))
    label1.grid(row=39, column=1)
    label1.place(anchor='center', relx=.5, rely=.5)
    root.mainloop()
