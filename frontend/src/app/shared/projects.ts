export interface Project {
    name: string
    routerLink: string
    materialIcon: string // TODO remove when all the projects are finished
    description: string
    github: string
}

/**
 * Text Mining Unit projects' information used across the entire app.
 */
export const PROJECTS: Project[] = [
    // Projects done; materialIcon: 'check'
    {
        name: 'SPACCC POS Tagger',
        routerLink: '/spaccc-pos-tagger',
        materialIcon: 'check',
        description: 'Spanish Clinical Case Corpus Part-of-Speech Tagger. Analyze Spanish medical reports to get theirs parts of speech and matching scores.',
        github: 'https://github.com/PlanTL/SPACCC_POS-TAGGER'
    },
    {
        name: 'Translator',
        routerLink: '/translator',
        materialIcon: 'check',
        description: 'Translate text using an open-source toolkit for neural machine translation (NMT).',
        github: 'https://github.com/PlanTL-SANIDAD/Medical-Translator-WMT19'
    },

    // Coming soon... materialIcon: 'warning'; TODO: CHANGE routerLink WHEN DONE
    {
        name: 'NeuroNER Tagger',
        routerLink: '/coming-soon', // /neuroner
        materialIcon: 'warning',
        description: 'Coming soon!',
        github: ''
    },
    {
        name: 'Spell Checker',
        routerLink: '/coming-soon', // /speller
        materialIcon: 'warning',
        description: 'Coming soon!',
        github: ''
    },
    {
        name: 'Word Embedding',
        routerLink: '/coming-soon', // /embedder
        materialIcon: 'warning',
        description: 'Coming soon!',
        github: ''
    },
    {
        name: 'Negation Extraction',
        routerLink: '/coming-soon', // /negator
        materialIcon: 'warning',
        description: 'Coming soon!',
        github: ''
    },
    {
        name: 'Search in Spanish',
        routerLink: '/coming-soon', // /searcher
        materialIcon: 'warning',
        description: 'Coming soon!',
        github: ''
    },
    {
        name: 'CUTEXT',
        routerLink: '/coming-soon', // /cutext
        materialIcon: 'warning',
        description: 'Coming soon!',
        github: ''
    },
    {
        name: 'Abre - Abbreviations',
        routerLink: '/coming-soon', // /abre
        materialIcon: 'warning',
        description: 'Coming soon!',
        github: ''
    },
    {
        name: 'TENTE',
        routerLink: '/coming-soon', // /tente
        materialIcon: 'warning',
        description: 'Coming soon!',
        github: ''
    },
    {
        name: 'EHR Normalizer',
        routerLink: '/coming-soon', // /ehrnormalizer
        materialIcon: 'warning',
        description: 'Coming soon!',
        github: ''
    },
];