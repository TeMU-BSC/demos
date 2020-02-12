export interface Project {
  name: string
  description: string
  repository: string
  routerLink: string
}

/**
 * Text Mining Unit projects' information used across the entire app.
 */
export const PROJECTS: Project[] = [
  {
    name: 'SPACCC POS Tagger',
    description:
      'Spanish Clinical Case Corpus Part-of-Speech Tagger. Analyze Spanish medical reports to get theirs parts of speech and matching scores.',
    repository: 'https://github.com/PlanTL/SPACCC_POS-TAGGER',
    routerLink: '/pos',
  },
  {
    name: 'Translator',
    routerLink: '/translator',
    description:
      'Translate clinical text using an open-source toolkit for neural machine translation (NMT).',
    repository: 'https://github.com/PlanTL-SANIDAD/Medical-Translator-WMT19',
  },
  {
    name: 'NeuroNER Tagger',
    routerLink: '/coming-soon', // /neuroner
    description: 'Coming soon!',
    repository: 'https://github.com/TeMU-BSC/PharmaCoNER-Tagger',
  },
  {
    name: 'Spell Checker',
    routerLink: '/coming-soon', // /speller
    description: 'Coming soon!',
    repository: '',
  },
  {
    name: 'Word Embedding',
    routerLink: '/coming-soon', // /embedder
    description: 'Coming soon!',
    repository: '',
  },
  {
    name: 'Negation Extraction',
    routerLink: '/coming-soon', // /negator
    description: 'Coming soon!',
    repository: '',
  },
  {
    name: 'Search in Spanish',
    routerLink: '/coming-soon', // /searcher
    description: 'Coming soon!',
    repository: '',
  },
  {
    name: 'CUTEXT',
    routerLink: '/coming-soon', // /cutext
    description: 'Coming soon!',
    repository: '',
  },
  {
    name: 'Abre - Abbreviations',
    routerLink: '/coming-soon', // /abre
    description: 'Coming soon!',
    repository: '',
  },
  {
    name: 'TENTE',
    routerLink: '/coming-soon', // /tente
    description: 'Coming soon!',
    repository: '',
  },
  {
    name: 'EHR Normalizer',
    routerLink: '/coming-soon', // /ehrnormalizer
    description: 'Coming soon!',
    repository: '',
  },
]
