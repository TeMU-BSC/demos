export interface SampleText {
  filename: string
  content: string
}

export interface Word {
  sentenceId: number
  id: number
  forma: string
  lemma: string
  tag: string
  pos: string
  category: string
  score: number
}

export interface Sentence {
  id: number
  words: Word[]
}