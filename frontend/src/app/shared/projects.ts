export interface Project {
  name: string
  description: string
  repository: string
  routerLink: string
  model: string
  id: string
  short_description: string
  language: string
  outputs: string[]

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
    model: "",
    id: "01",
    short_description: "",
    language: "",
    outputs: [""],
  },
  {
    name: 'Sentence Splitter',
    description: 'This tool separetes long string into sentences, the system can detect when a (.) is used for finishing a sentence or when it used for abreviation. ',
    repository: 'https://github.com/PlanTL-GOB-ES/SPACCC_Sentence-Splitter',
    routerLink: '/sentence-splitter',  // '/pos',
    model: "",
    id: "11",
    short_description: "",
    language: "",
    outputs: [""],
  },
  {
    name: 'Translator',
    description: 'Translate clinical text using an open-source toolkit for neural machine translation (NMT).',
    repository: 'https://github.com/PlanTL-SANIDAD/Medical-Translator-WMT19',
    routerLink: '/translator',
    model: "",
    id: "02",
    short_description: "",
    language: "",
    outputs: [""],
  },
  {
    name: 'Doctor NLP',
    description: 'Reconocimiento de entidades basado en nuestro modelo de deep-learning para la detección de procedimientos, enfermedades, sintomas, farmacos en español.',
    repository: '',
    routerLink: '/ner/03',
    model: "conjunto",
    id: "03",
    short_description: "",
    language: "",
    outputs: [""],
  },
  {
    name: 'NER enfermedad',
    description: 'Reconocimiento de entidades basado en nuestro modelo de deep-learning para la detección de enfermedades en español.',
    repository: '',
    routerLink: '/ner/04',
    model: "enfermedad",
    id: "04",
    short_description: "",
    language: "",
    outputs: [""],
  },
  {
    name: 'NER sintoma',
    description: 'Reconocimiento de entidades basado en nuestro modelo de deep-learning para la detección de sintomas en español.',
    repository: '',
    routerLink: '/ner/05',
    model: "sintoma",
    id: "05",
    short_description: "",
    language: "",
    outputs: [""],
  },
  {
    name: 'NER farmaco',
    description: 'Reconocimiento de entidades basado en nuestro modelo de deep-learning para la detección de farmacos en español.',
    repository: '',
    routerLink: '/ner/06',
    model: "farmaco",
    id: "06",
    short_description: "",
    language: "",
    outputs: [""],
  },
  {
    name: 'NER procedimiento',
    description: 'Reconocimiento de entidades basado en nuestro modelo de deep-learning para la detección de procedimientos en español.',
    repository: '',
    routerLink: '/ner/07',
    model: "procedimiento",
    id: "07",
    short_description: "",
    language: "",
    outputs: [""],
  },
  // {
  //   name: 'NeuroNER Tagger',
  //   description: 'in progress',
  //   repository: 'https://github.com/TeMU-BSC/PharmaCoNER-Tagger',
  //   routerLink: '/neuro-ner', // /'neuroner',
  // },
  {
    name: 'DrugProt Gene Tagger',
    description: "Deep Learning Gene Recognition system for English texts built using cross-sentence information with a transformer model",
    repository: 'https://github.com/TeMU-BSC/PharmaCoNER-Tagger',
    routerLink: '/drugprot/gene', // /'neuroner',
    model: "gene",
    id: "08",
    short_description: "",
    language: "",
    outputs: [""],
  },
  {
    name: 'DrugProt Chemical Tagger',
    description: 'Deep Learning Chemical Recognition system for English texts built using cross-sentence information with a transformer model',
    repository: 'https://github.com/TeMU-BSC/PharmaCoNER-Tagger',
    routerLink: '/drugprot/chemical', // /'neuroner',
    model: "chemical",
    id: "09",
    short_description: "",
    language: "",
    outputs: [""],
  },

  // {
  //   name: 'Spell Checker',
  //   description: 'Coming soon!',
  //   repository: '',
  //   routerLink: '/coming-soon', // /'speller',
  // },
  // {
  //   name: 'Word Embedding',
  //   description: 'Coming soon!',
  //   repository: '',
  //   routerLink: '/coming-soon', // /'embedder',
  // },
  {
    name: 'Negation Extraction',
    description: 'Work in progress',
    repository: '',
    routerLink: '/neuro-ner/10', // /'negator',
    model: "negation",
    id: "10",
    short_description: "",
    language: "",
    outputs: [""],
  }
  //,
  // {
  //   name: 'Search in Spanish',
  //   description: 'Coming soon!',
  //   repository: '',
  //   routerLink: '/coming-soon', // /'searcher',
  // },
  // {
  //   name: 'CUTEXT',
  //   description: 'Coming soon!',
  //   repository: '',
  //   routerLink: '/coming-soon', // /'cutext',
  // },
  // {
  //   name: 'Abre - Abbreviations',
  //   description: 'Coming soon!',
  //   repository: '',
  //   routerLink: '/coming-soon', // /'abre',
  // },
  // {
  //   name: 'TENTE',
  //   description: 'Coming soon!',
  //   repository: '',
  //   routerLink: '/coming-soon', // /'tente',
  // },
  // {
  //   name: 'EHR Normalizer',
  //   description: 'Coming soon!',
  //   repository: '',
  //   routerLink: '/coming-soon', // /'ehrnormalizer',
  // },
]
