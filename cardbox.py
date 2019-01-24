import sqlite3
import random
import pandas as pd
from matcher import *
from quiz import anagram_question
import misc

conn = sqlite3.connect('cardbox.db')
c = conn.cursor()


def new_cardbox(cardbox_name):
    c.execute("CREATE TABLE " + cardbox_name + " (word text, last integer, weighted real, qnum integer)")


def add_to_cardbox(cardbox_name, new_words, rand=True):
    new_words = list(set(new_words))
    if rand:
        random.shuffle(new_words)

    old_words = list(read_table(cardbox_name)['word'])

    for i in new_words:
        if i not in old_words:
            c.execute("INSERT INTO " + cardbox_name + " VALUES (?, ?, ?, ?)", (i, 0, 0, 0))
    conn.commit()


def remove_from_cardbox(cardbox_name, *matchers):
    words = search(*matchers)

    words_in_cardbox = list(read_table(cardbox_name)['word'])

    for i in words:
        if i in words_in_cardbox:
            c.execute("DELETE FROM " + cardbox_name + " WHERE word = ?", (i))
    conn.commit()


def read_table(cardbox_name):
    return pd.read_sql_query("select * from " + cardbox_name, conn)


def questions_left(cardbox_name):
    df = read_table(cardbox_name)
    n = 0
    for i, row in df.iterrows():
        if row["qnum"] == 0:
            n += 1
    return n


def correct(cardbox_name):
    s = 0
    c = 0
    for i in read_table(cardbox_name).iterrows():
        s += i[-1]["last"]
        c += 1
    return (s / c)


def max_q(cardbox_name):
    df = read_table(cardbox_name)
    return max(df["qnum"].tolist())


"""
def ana_filt(df,l):
    print("phase 0")
    ana_l=[]
    for i in l:
        print("woah")
        ana_l+=search(Anagram(i,True))
    print("phase 1")
    words=df['word'].tolist()
    L=[]
    for i in words:
        if i[0] in l and i[0] not in L:
            L.append(i)
    ce=pd.DataFrame(columns=["word","last","weighted","qnum"])

    for i in L:
        d={"word":i[0],"last":i[1],"weighted":i[2],"qnum":i[3]}
        ce=ce.append(d,ignore_index=True)
    return ce
"""


def ana_filt(df, *matchers):
    alphagrams = misc.alphagrammize_list(misc.search(*matchers))

    words = df['word'].tolist()

    l2 = []
    for i in words:
        if misc.alphagrammize(i) in alphagrams and i not in l2:
            l2.append(i)

    return df[df['word'].isin(l2)]


def cardbox_quiz(cardbox_name, last_weight, weighted_weight, qnum_weight, rand_weight, *matchers):
    df = read_table(cardbox_name)

    """  
    if l!=[]:
        df=ana_filt(unfiltered_df,l)
    else:
        df=unfiltered_df
    """
    order = []

    maxq = df["qnum"].max()
    minq = df["qnum"].min()

    # df=df.ix[match(df['word'],*matchers)]

    for i, row in df.iterrows():
        if maxq != minq:
            qp = (row["qnum"] - minq) / (maxq - minq)
        else:
            qp = 0
        order.append((row["last"] * last_weight +
                      row["weighted"] * weighted_weight +
                      qp * qnum_weight +
                      random.random() * rand_weight) /
                     (qnum_weight + last_weight + weighted_weight + rand_weight))

    df = df.assign(order=pd.Series(order).values)

    # pd.options.display.max_rows = 250
    print(df)

    n = 0
    while True:
        x = df["order"].idxmin()
        word = df.iloc[x]["word"]
        """if len(matchers)!=0:
            while not misc.multi_match(word,*matchers):
                df=df.drop(index=x)
                x = df["order"].idxmin()
                word = df.iloc[x]["word"]
                print(min(df["order"]))
        print('w')
        print(df.iloc[df["order"].idxmin()]['order'])
        print(df["order"].min())
        print(df[df["order"] == df["order"].min()]["order"])
        print('w')
        print(df.iloc[x])"""

        result, answered = anagram_question(word)
        if not answered:
            break

        changes = pd.DataFrame(columns=["word", "last", "weighted", "qnum"])

        qnum = max(df["qnum"] + 1)

        ratio = 1
        if len(result["Correct"]) != 0:
            perc_wrong = len(result["Wrong"]) / len(result["Correct"] + result["Wrong"])

        n += len(result["Correct"] + result["Missed"])

        i = "Correct"
        for j in result[i]:
            ix = df.index[df['word'] == j].tolist()[0]
            df.loc[ix, "last"] = 1
            df.loc[ix, "weighted"] = df.loc[ix, "weighted"] / 2 + (1 - perc_wrong) / 2
            df.loc[ix, "qnum"] = qnum
            df.loc[ix, "order"] = df.loc[ix, "last"] * last_weight + df.loc[ix, "weighted"] * weighted_weight + df.loc[
                ix, "qnum"] * qnum_weight
            changes = changes.append({'word': j,
                                      'last': 1,
                                      'weighted': df.loc[ix, "weighted"],
                                      'qnum': qnum
                                      }, ignore_index=True)

        i = "Missed"
        for j in result[i]:
            ix = df.index[df['word'] == j].tolist()[0]
            df.loc[ix, "last"] = 0
            df.loc[ix, "weighted"] = df.loc[ix, "weighted"] / 2
            df.loc[ix, "qnum"] = qnum
            df.loc[ix, "order"] = df.loc[ix, "last"] * last_weight + df.loc[ix, "weighted"] * weighted_weight + df.loc[
                ix, "qnum"] * qnum_weight
            changes = changes.append({'word': j,
                                      'last': 0,
                                      'weighted': df.loc[ix, "weighted"],
                                      'qnum': qnum
                                      }, ignore_index=True)

        order = []

        maxq = df["qnum"].max()
        minq = df["qnum"].min()
        for i, row in df.iterrows():
            order.append(row["last"] * last_weight + row["weighted"] * weighted_weight + (
                    (row["qnum"] - minq) / (maxq - minq)) * qnum_weight + random.random() * rand_weight)

        df = df.assign(order=pd.Series(order).values)

        for row in changes.iterrows():
            row = row[1]
            c.execute('UPDATE ' + cardbox_name + ' SET last=?, weighted=?, qnum=? WHERE word = ?',
                      (row["last"], row["weighted"], row["qnum"], row["word"]))

        conn.commit()

    print(df.sort_values('order'))
    # print(str(questions_left(cardbox_name)) + " left")
    print(str(n) + " answered")
    print(correct(cardbox_name))


def in_cardbox(cardbox_name, *matchers):
    cardbox_words = read_table(cardbox_name)['word'].tolist()
    return misc.search(*matchers, l=cardbox_words)

if __name__=="__main__":
    from features import quiz_from_cardbox, default_cardbox
    quiz_from_cardbox(default_cardbox, 0.01, 3, 2, 1, Subanagram("..."))