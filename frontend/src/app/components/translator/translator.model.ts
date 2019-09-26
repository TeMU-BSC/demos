export interface Language {
  label: string
  name: string
  flagIconImgSrc: string
}

export const LANGUAGES = [
  {
    label: 'en',
    name: 'English',
    flagIconImgSrc: 'assets/images/flags/united-kingdom.svg',
  },
  {
    label: 'es',
    name: 'Spanish',
    flagIconImgSrc: 'assets/images/flags/spain.svg',
  },
  {
    label: 'pt',
    name: 'Portuguese',
    flagIconImgSrc: 'assets/images/flags/portugal.svg',
  }
]

export interface Sample {
  language: string
  filename: string
  content: string
}

export interface SampleGroup {
  language: Language
  samples: Sample[]
}

export interface Translation {
  predictionScore: number
  translatedSentences: string[]
  translationTime: number
}