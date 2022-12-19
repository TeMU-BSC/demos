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
export const PROJECTS: any[] = [

  {
    name: 'Anonimizador',
    description: 'Anonimizador para castellano y catalán de contenidos generados por usuarios en sistemas conversacionales',
    repository: 'https://github.com/TeMU-BSC/AnonymizationPipeline',
    routerLink: 'https://anonimizador.plantl.bsc.es/',  // '/pos',
    model: "",
    id: "01",
    short_description: "",
    language: "",
    outputs: [""],
  },
  {
    name: 'Spacy',
    description: 'Demostrador de los diferentes modelos Spacy para castellano, y sus capacidades.',
    repository: '',
    routerLink: 'https://spacy.plantl.bsc.es/',  // '/pos',
    model: "",
    id: "02",
    short_description: "",
    language: "",
    outputs: [""],
  },
  {
    name: 'QA',
    description: 'Sistema de Pregunta/Respuesta en la Wikipedia en Castellano, basado en modelos y datasets generados bajo el PlanTL.',
    repository: '',
    routerLink: 'https://qa.plantl.bsc.es/',  // '/pos',
    model: '',
    id: '03',
    short_description: "",
    language: "",
    outputs: [""],
  },
  {
    name: 'Traductor Automático',
    description: 'Traductores automáticos entre español y catalán y entre español y gallego',
    repository: '',
    routerLink: 'https://traductor.plantl.bsc.es/',  // '/pos',
    model: '',
    id: '04',
    short_description: "",
    language: "",
    outputs: [""],
  },
  {
    name: 'EvalES',
    description: 'Colección de recursos para evaluar sistemas de comprensión del lenguaje natural.',
    repository: 'https://github.com/PlanTL-GOB-ES/spanish-benchmark',
    routerLink: 'https://benchmark.plantl.bsc.es/',  // '/pos',
    model: '',
    id: '05',
    short_description: "",
    language: "",
    outputs: [""],
  },
  // {
  //   name: 'MedLing Tagger',
  //   description: 'Spanish Clinical Case Corpus Part-of-Speech Tagger. Analyze Spanish medical reports to get theirs parts of speech and matching scores.',
  //   repository: 'https://github.com/PlanTL/SPACCC_POS-TAGGER',
  //   routerLink: '/pos',  // '/pos',
  //   model: "",
  //   id: "01",
  //   short_description: "",
  //   language: "",
  //   outputs: [""],
  // },
  // // {
  // //   name: 'Sentence Splitter',
  // //   description: 'This tool separetes long string into sentences, the system can detect when a (.) is used for finishing a sentence or when it used for abreviation. ',
  // //   repository: 'https://github.com/PlanTL-GOB-ES/SPACCC_Sentence-Splitter',
  // //   routerLink: '/sentence-splitter',  // '/pos',
  // //   model: "",
  // //   id: "11",
  // //   short_description: "",
  // //   language: "",
  // //   outputs: [""],
  // // },
  // {
  //   name: 'MedTranslator',
  //   description: 'Translate clinical text using an open-source toolkit for neural machine translation (NMT).',
  //   repository: 'https://github.com/PlanTL-SANIDAD/Medical-Translator-WMT19',
  //   routerLink: '/translator',
  //   model: "",
  //   id: "02",
  //   short_description: "",
  //   language: "",
  //   outputs: [""],
  // },
  // {
  //   name: 'DoctorNLP',
  //   description: 'Reconocimiento de entidades basado en nuestro modelo de deep-learning para la detección de procedimientos, enfermedades, sintomas, farmacos en español.',
  //   repository: '',
  //   routerLink: '/ner/03',
  //   model: "conjunto",
  //   id: "03",
  //   short_description: "",
  //   language: "",
  //   outputs: [""],
  // },
  // {
  //   name: 'DiseaseTagIt',
  //   description: 'Sistema de reconocimiento de menciones de enfermedades/trastornos y mapeo a terminología SNOMED CT',
  //   repository: '',
  //   routerLink: '/ner/04',
  //   model: "enfermedad",
  //   id: "04",
  //   short_description: "",
  //   language: "",
  //   outputs: [""],
  // },
  // {
  //   name: 'SymptomTagIt',
  //   description: 'Sistema de reconocimiento de menciones de síntomas/signos clinicos y mapeo a terminología SNOMED CT ',
  //   repository: '',
  //   routerLink: '/ner/05',
  //   model: "sintoma",
  //   id: "05",
  //   short_description: "",
  //   language: "",
  //   outputs: [""],
  // },
  // {
  //   name: 'DrugTagIt',
  //   description: 'Sistema de reconocimiento de menciones de fármacos/medicamentos y mapeo a terminología SNOMED CT ',
  //   repository: '',
  //   routerLink: '/ner/06',
  //   model: "farmaco",
  //   id: "06",
  //   short_description: "",
  //   language: "",
  //   outputs: [""],
  // },
  // {
  //   name: 'ProcedureTagIt',
  //   description: 'Sistema de reconocimiento de menciones de procedimientos clinicos y mapeo a terminología SNOMED CT.',
  //   repository: '',
  //   routerLink: '/ner/07',
  //   model: "procedimiento",
  //   id: "07",
  //   short_description: "",
  //   language: "",
  //   outputs: [""],
  // },
  // // {
  // //   name: 'NeuroNER Tagger',
  // //   description: 'in progress',
  // //   repository: 'https://github.com/TeMU-BSC/PharmaCoNER-Tagger',
  // //   routerLink: '/neuro-ner', // /'neuroner',
  // // },
  // {
  //   name: 'DrugProt Gene Tagger',
  //   description: "Deep Learning Gene Recognition system for English texts built using cross-sentence information with a transformer model",
  //   repository: 'https://github.com/TeMU-BSC/PharmaCoNER-Tagger',
  //   routerLink: '/drugprot/gene', // /'neuroner',
  //   model: "gene",
  //   id: "08",
  //   short_description: "",
  //   language: "",
  //   outputs: [""],
  // },
  // {
  //   name: 'DrugProt Chemical Tagger',
  //   description: 'Deep Learning Chemical Recognition system for English texts built using cross-sentence information with a transformer model',
  //   repository: 'https://github.com/TeMU-BSC/PharmaCoNER-Tagger',
  //   routerLink: '/drugprot/chemical', // /'neuroner',
  //   model: "chemical",
  //   id: "09",
  //   short_description: "",
  //   language: "",
  //   outputs: [""],
  // },
  // {
  //   name: 'DoctorNLP v2',
  //   description: 'Reconocimiento de entidades basado en nuestro modelo de deep-learning para la detección de procedimientos, enfermedades, sintomas, farmacos en español.',
  //   repository: 'https://github.com/TeMU-BSC/PharmaCoNER-Tagger',
  //   routerLink: '/doctorNLP', // /'neuroner',
  //   model: "doctorNLP",
  //   id: "10",
  //   short_description: "",
  //   language: "es",
  //   outputs: [""],
  // },
  // {
  //   name: 'PhenoTagIt Advanced',
  //   description: 'Place holder for the advanced version of PhenoTagIt',
  //   repository: 'https://github.com/TeMU-BSC/PharmaCoNER-Tagger',
  //   routerLink: '/phenotype_visualizer', // /'neuroner',
  //   model: "phenotype_visualizer",
  //   id: "11",
  //   short_description: "",
  //   language: "es",
  //   outputs: [""],
  // },

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
  // {
  //   name: 'Negation Extraction',
  //   description: 'Work in progress',
  //   repository: '',
  //   routerLink: '/neuro-ner/10', // /'negator',
  //   model: "negation",
  //   id: "10",
  //   short_description: "",
  //   language: "",
  //   outputs: [""],
  // }
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
