def split_bio(datapath):
  '''
  Transform dataset from CONLL format (token fileid pos0 pos1 tag\n) into a 
  dictionary with tokens, files, pos0, pos1 and tags as keys.
  Every value of the output dictionary is a list of lists (one per sentence)

  Parameters
  ----------
  datapath : str
   Route to folder with dataset file in BIO format 

  Returns
  ----------
  dataset : dict
    Dictionary with tokens, files, pos0, pos1 and tags. Every entry is a list of
    lists (one per sentence)
    Keys:
      tokens: token
      files: filename to which the token belong
      pos0: starting offset of token
      pos1: ending offset of token
      tags: tag of token (B,I,O,...)
  '''
  # Load BIO file
  _file_ = open(datapath).readlines()

  # Parse BIO file
  tokens = []
  files = []
  pos0 = []
  pos1 = []
  tags = []
  tokens_this_sentence = []
  files_this_sentence = []
  pos0_this_sentence = []
  pos1_this_sentence = []
  tags_this_sentence = []
  for sentence, i in zip(_file_, range(len(_file_))):
    if sentence != '\n':
      splitted = sentence.split(' ')
      tokens_this_sentence.append(' '.join(splitted[:-4]))
      files_this_sentence.append(splitted[-4])
      pos0_this_sentence.append(splitted[-3])
      pos1_this_sentence.append(splitted[-2])
      tags_this_sentence.append(splitted[-1].rstrip('\n'))
    else: 
      # End of sentence
      # Check past sentence is correct
      assert ((len(tokens_this_sentence) == len(files_this_sentence) == 
               len(pos1_this_sentence) == len(pos1_this_sentence) == 
               len(tags_this_sentence))), "ERROR when parsing sentence {} in BIO file".\
              format(_file_[i-1]) 
      tokens.append(tokens_this_sentence)
      files.append(files_this_sentence)
      pos0.append(pos0_this_sentence)
      pos1.append(pos1_this_sentence)
      tags.append(tags_this_sentence)
      tokens_this_sentence = []
      files_this_sentence = []
      pos0_this_sentence = []
      pos1_this_sentence = []
      tags_this_sentence = []

  # Load info into final dictionary
  assert (len(tokens) == len(files) == len(pos0) == len(pos1) == len(tags)), "ERROR when parsing sentences in BIO file"
  assert (sum(map(lambda x: x=='\n', _file_))==len(tokens)), "ERROR when finding line endings in CONLL file"
  dataset = {}
  dataset['tokens'] = tokens
  dataset['files'] = files
  dataset['pos0'] = pos0
  dataset['pos1'] = pos1
  dataset['tags'] = tags
  return dataset
