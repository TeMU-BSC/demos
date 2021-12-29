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
    description: 'Spanish Clinical Case Corpus Part-of-Speech Tagger. Analyze Spanish medical reports to get theirs parts of speech and matching scores.',
    repository: 'https://github.com/PlanTL/SPACCC_POS-TAGGER',
    routerLink: '/pos',  // '/pos',
  },
  {
    name: 'Translator',
    description: 'Translate clinical text using an open-source toolkit for neural machine translation (NMT).',
    repository: 'https://github.com/PlanTL-SANIDAD/Medical-Translator-WMT19',
    routerLink: '/translator',
  },
  {
    name: 'NER All',
    description: 'Reconocimiento de entidades nombradas utilizando  deep-learning para la detección de procedimientos en español.',
    repository: '',
    routerLink: '/ner/All',
  },
  {
    name: 'NER enfermedad',
    description: 'Reconocimiento de entidades nombradas utilizando  deep-learning para la detección de procedimientos en español.',
    repository: '',
    routerLink: '/ner/enfermedad',
  },
  {
    name: 'NER sintoma',
    description: 'Reconocimiento de entidades nombradas utilizando  deep-learning para la detección de procedimientos en español.',
    repository: '',
    routerLink: '/ner/sintoma',
  },
  {
    name: 'NER farmaco',
    description: 'Reconocimiento de entidades nombradas utilizando  deep-learning para la detección de procedimientos en español.',
    repository: '',
    routerLink: '/ner/farmaco',
  },
  {
    name: 'NER procedimiento',
    description: 'Reconocimiento de entidades nombradas utilizando  deep-learning para la detección de procedimientos en español.',
    repository: '',
    routerLink: '/ner/procedimiento',
  },
  {
    name: 'NeuroNER Tagger',
    description: 'in progress',
    repository: 'https://github.com/TeMU-BSC/PharmaCoNER-Tagger',
    routerLink: '/coming-soon', // /'neuroner',
  },
  {
    name: 'DrugProt Gene Tagger',
    description: " A system used to create a baseline Named entity and entity relation predictions for BioCreative VII, Track 1 - Text mining drug \n and chemical-protein interactions  as well as to automatically annotate named entities on large scale biomedical background data set for Large scale Text Mining.",
    repository: 'https://github.com/TeMU-BSC/PharmaCoNER-Tagger',
    routerLink: '/drugprot/gene', // /'neuroner',
  },
  {
    name: 'DrugProt Chemical Tagger',
    description: 'A system used to create a baseline Named entity and entity relation predictions for BioCreative VII, Track 1 - Text mining drug \n and chemical-protein interactions  as well as to automatically annotate named entities on large scale biomedical background data set for Large scale Text Mining.',
    repository: 'https://github.com/TeMU-BSC/PharmaCoNER-Tagger',
    routerLink: '/drugprot/chemical', // /'neuroner',
  },

  {
    name: 'Spell Checker',
    description: 'Coming soon!',
    repository: '',
    routerLink: '/coming-soon', // /'speller',
  },
  {
    name: 'Word Embedding',
    description: 'Coming soon!',
    repository: '',
    routerLink: '/coming-soon', // /'embedder',
  },
  {
    name: 'Negation Extraction',
    description: 'Coming soon!',
    repository: '',
    routerLink: '/coming-soon', // /'negator',
  },
  {
    name: 'Search in Spanish',
    description: 'Coming soon!',
    repository: '',
    routerLink: '/coming-soon', // /'searcher',
  },
  {
    name: 'CUTEXT',
    description: 'Coming soon!',
    repository: '',
    routerLink: '/coming-soon', // /'cutext',
  },
  {
    name: 'Abre - Abbreviations',
    description: 'Coming soon!',
    repository: '',
    routerLink: '/coming-soon', // /'abre',
  },
  {
    name: 'TENTE',
    description: 'Coming soon!',
    repository: '',
    routerLink: '/coming-soon', // /'tente',
  },
  {
    name: 'EHR Normalizer',
    description: 'Coming soon!',
    repository: '',
    routerLink: '/coming-soon', // /'ehrnormalizer',
  },
]
