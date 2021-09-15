import numpy as np

def getEmbeddingMatrix(words2idx, emb_dim, model):
  # From https://github.com/ssantamaria94/CANTEMIST-Participation/blob/master/final-model.ipynb
  embedding_matrix = np.zeros((len(words2idx), emb_dim))
  for word, i in words2idx.items():
    embedding_matrix[i] = model[word]

  return embedding_matrix


def add_bpe_emb(dataset, bpe_object, MAXLENGTH, BPEDIM):
  dataset_bpe = []
  for sentence in dataset['tokens']:
    dataset_bpe_this = []
    for token, idx in zip(sentence, range(len(sentence))):
      if idx >= MAXLENGTH:
        break
      dataset_bpe_this.append(bpe_object.embed(token))
    try:
      dataset_bpe_this_max = list(map(lambda x: np.max(x, axis=0), dataset_bpe_this))
    except Exception as e:
      print(e)
      print(sentence)
      print(repr(token))
      print(dataset_bpe_this)
      #input('HEHE')
    # Add padding
    if len(sentence)<MAXLENGTH:
      for i in range(MAXLENGTH-len(sentence)):
        dataset_bpe_this_max.append(np.zeros((50,), dtype=np.float32))
    # Max pooling to have 1 vector per word
    dataset_bpe.append(dataset_bpe_this_max)
  return np.array(dataset_bpe)
