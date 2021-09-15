import numpy as np

def word2int(words, word2idx):
    '''
    from https://github.com/tonifuc3m/relation-extraction-ddi/blob/master/preprocessing.py
    Map words to integers
    
    Parameters
    ----------
    words: list
        List of lists. Every item is a tokenized sentence (a list of words)
    word2idx: word_index
        Dictionary relating every word with an integer. That integer tells us 
        the position in the embedding matrix for the embedding of that word.
    
    Returns
    ----------
    idx: list
        List of lists. Every item is a list of integers (every integer
        corresponds to a word)
    
    '''
    idx = [[word2idx.get(t, 0) for t in sentence] for sentence in words]
    return idx


def get_char_idx(dataset, char2idx, MAXLENGTH=80, MAXLENCHAR=10):
  X_char = []
  for sentence in dataset['tokens']:
      sent_seq = []
      for i in range(MAXLENGTH):
          word_seq = []
          for j in range(MAXLENCHAR):
              try:
                  if char2idx.get(sentence[i][j]) == None:
                    word_seq.append(char2idx.get("UNK"))
                    continue
                  word_seq.append(char2idx.get(sentence[i][j]))
              except:
                  word_seq.append(char2idx.get("PAD"))
          sent_seq.append(word_seq)
      X_char.append(np.array(sent_seq))
  return np.asarray(X_char, dtype=np.int64)


def label2vec(label,classes=4):
    vec = np.zeros((label.shape[0],label.shape[1],classes))
    for i in range(label.shape[0]):
        for j in range(label.shape[1]):
            t = int(label[i,j])
            vec[i,j,t] = 1
    return vec
