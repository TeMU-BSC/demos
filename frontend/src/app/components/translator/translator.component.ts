import { Component, OnInit } from '@angular/core'
import { FormBuilder, FormGroup, Validators } from '@angular/forms'
import { MatSnackBar } from '@angular/material/snack-bar';
import { DomSanitizer, SafeUrl } from '@angular/platform-browser'
import { TemuResponse } from 'src/app/shared/api.shared'
import { Project, PROJECTS } from 'src/app/shared/projects'
import {
  Language,
  LANGUAGES,
  Sample,
  SampleGroup,
} from 'src/app/components/translator/translator.model'
import { TranslatorService } from 'src/app/components/translator/translator.service'
import { Utils } from 'src/app/shared/utils'

@Component({
  selector: 'app-translator',
  templateUrl: './translator.component.html',
  styleUrls: ['./translator.component.css'],
})
export class TranslatorComponent implements OnInit {
  project: Project
  languages: Language[]
  translatorForm: FormGroup
  sampleGroups: SampleGroup[]
  MAX_CHARACTERS = 10000
  response: TemuResponse
  sourceText: string
  translatedText: string
  averageScore: number
  translationTime: number
  downloadFilename: string
  downloadLink: SafeUrl

  // -------------------------------------------------------------------------

  constructor(
    private translatorService: TranslatorService,
    private sanitizer: DomSanitizer,
    private snackBar: MatSnackBar,
    private formBuilder: FormBuilder
  ) {}

  ngOnInit() {
    // Set the current project demo
    PROJECTS.forEach((project, index) => {
      if (project.name === 'Translator') {
        this.project = PROJECTS[index]
      }
    })

    // Set the available languages
    this.languages = LANGUAGES

    // Prepare the samples group select
    this.getSamplesGroup()

    // Define the form fields and its validators
    this.translatorForm = this.formBuilder.group({
      sourceLanguageCode: ['es', Validators.required],
      targetLanguageCode: ['en', Validators.required],
      sample: [''],
      text: [
        '',
        [Validators.required, Validators.maxLength(this.MAX_CHARACTERS)],
      ],
    })

    // Init some string atributes
    this.sourceText = ''
    this.translatedText = ''
    this.downloadFilename = 'temu_translator.json'
  }

  // -------------------------------------------------------------------------

  /**
   * Convenience getter for easy access to form fields from HTML template.
   */
  get f() {
    return this.translatorForm.controls
  }

  /**
   * Get the sample texts to easily test the app
   */
  getSamplesGroup() {
    this.sampleGroups = []
    this.languages.forEach(lang =>
      this.sampleGroups.push({ language: lang, samples: [] })
    )

    this.translatorService.getSamples().subscribe(response => {
      // this.samples = response.data
      this.sampleGroups.forEach(group => {
        group.samples = []
        response.data.forEach((sample: Sample) => {
          if (group.language.label === sample.language) {
            group.samples.push(sample)
          }
        })
      })
    })
  }

  /**
   * Select the corresponding language to be the source or target.
   *
   * @param langType 'sourceLanguageCode'|'targetLanguageCode'
   * @param langLabel 'en'|'es'|'pt'
   */
  onLanguageClick(langType: string, langLabel: string) {
    this.translatorForm.controls[`${langType}`].setValue(langLabel)
  }

  /**
   * Toggle between source and target languages.
   */
  toggleSourceTargetLanguage() {
    const tmpSrc = this.translatorForm.controls.sourceLanguageCode.value
    const tmpTgt = this.translatorForm.controls.targetLanguageCode.value
    this.translatorForm.controls.sourceLanguageCode.setValue(tmpTgt)
    this.translatorForm.controls.targetLanguageCode.setValue(tmpSrc)
  }

  /**
   * Load a sample text to quickly test the web app.
   */
  loadSampleText(sample: Sample) {
    this.translatorForm.get('text').setValue(sample.content)
  }

  /**
   * Get the response from the translator service.
   */
  translate() {
    // Reset the translated text before the next translation
    this.translatedText = ''
    this.response = null

    // Call the service
    this.translatorService.translate(this.translatorForm.value).subscribe(
      response => (this.response = response),
      error => alert(error),
      () => {

        this.translatedText = this.response['data']['translation']


        // Round down to 4 digits the average pred score and translation time.
        this.averageScore = Utils.round(this.response.data.predictionScore, 4)
        this.translationTime = Utils.round(
          this.response.data.translationTime,
          4
        )

        // Inform the user when data has been retrieved.
        this.snackBar.open(this.response.message, 'OK', {
          duration: 4000,
        })

        // Generate the download URI.
        this.downloadLink = Utils.generateDownloadJsonUri(
          this.response,
          this.sanitizer
        )
      }
    )
  }
}
