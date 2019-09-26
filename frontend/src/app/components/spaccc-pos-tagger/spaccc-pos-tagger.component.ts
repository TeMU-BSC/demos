/**
 * Customized version of the Freeling tool:
 * http://nlp.lsi.upc.edu/freeling/demo/demo.php
 * 
 * Adapted to Spanish Medical text. This component calls the Freeling service
 * component, which requests the obtained data from our RESTful API. 
 * 
 * @author Alejandro Asensio <https://github.com/aasensios>
 */

import { Component, OnInit } from '@angular/core'
import { FormBuilder, FormGroup, Validators } from '@angular/forms'
import { MatSnackBar } from '@angular/material'
import { DomSanitizer, SafeUrl } from '@angular/platform-browser'
import { TableColumn, Width, ButtonType } from 'simplemattable'
import { TemuResponse } from 'src/app/shared/api.shared'
import { Utils } from 'src/app/shared/utils'
import { SpacccPosTaggerService, CATEGORIES, FREELING_USER_MANUAL_SPANISH_TAGSET_URL, TAG_ANCHOR_BASE } from 'src/app/components/spaccc-pos-tagger/spaccc-pos-tagger.service'
import { SampleText, Word, Sentence } from 'src/app/components/spaccc-pos-tagger/spaccc-pos-tagger.model'
import { PROJECTS, Project } from 'src/app/shared/projects'

@Component({
  selector: 'app-spaccc-pos-tagger',
  templateUrl: './spaccc-pos-tagger.component.html',
  styleUrls: ['./spaccc-pos-tagger.component.scss']
})
export class SpacccPosTaggerComponent implements OnInit {

  project: Project
  freelingForm: FormGroup
  samples: SampleText[]
  MAX_CHARACTERS = 1000000
  response: TemuResponse
  sentences: Sentence[]
  words: Word[]
  scores: number[]
  averageScore: number
  downloadFilename: string
  downloadLink: SafeUrl

  // Table columns can be filtered. The two first columns hide when screen is extra-small (xs).
  columns = [
    new TableColumn<Word, 'sentenceId'>('Sentence #', 'sentenceId').withColFilter().withWidth(Width.pct(10)).isHiddenXs(true),
    new TableColumn<Word, 'id'>('Word #', 'id').withColFilter().withWidth(Width.pct(10)).isHiddenXs(true),
    new TableColumn<Word, 'forma'>('Forma (Original Word)', 'forma').withColFilter(),
    new TableColumn<Word, 'lemma'>('Lemma', 'lemma').withColFilter().withNgClass(() => 'font-italic'),
    new TableColumn<Word, 'tag'>('Tag', 'tag').withColFilter().withButton(ButtonType.RAISED).withButtonColor('accent')
      // .withNgClass((data, parentData) => `tooltip ${parentData.pos}`)
      .withOnClick(
        (tag, word) => {
          // const firstLetter = tag.charAt(0)
          // const anchor = `${TAG_ANCHOR_BASE}${POS[firstLetter]}`
          const anchor = `${TAG_ANCHOR_BASE}${word.pos}`
          window.open(`${FREELING_USER_MANUAL_SPANISH_TAGSET_URL}${anchor}`)
        }
      ),
    new TableColumn<Word, 'pos'>('POS Category', 'pos').withColFilter().withButton(ButtonType.BASIC).withButtonColor('primary')
    // .withNgClass((data, parentData) => `tooltip ${parentData.pos}`)
    .withOnClick(
      (pos, word) => {
        const anchor = `${TAG_ANCHOR_BASE}${pos}`
        window.open(`${FREELING_USER_MANUAL_SPANISH_TAGSET_URL}${anchor}`)
      }
    ),
    new TableColumn<Word, 'score'>('Score', 'score').withColFilter().withWidth(Width.pct(10)),
  ]

  // --------------------------------------------------------------------------

  constructor(
    private freelingService: SpacccPosTaggerService,
    private sanitizer: DomSanitizer,
    private snackBar: MatSnackBar,
    private formBuilder: FormBuilder,
  ) { }

  ngOnInit() {
    // Set the current project demo
    PROJECTS.forEach(
      (project, index) => {
        if (project.name === 'SPACCC POS Tagger') {
          this.project = PROJECTS[index]
        }
      })

    // Get the sample texts to test the app
    this.freelingService.getSampleTexts()
      .subscribe(
        response => this.samples = response.data
      )

    // Define the form fields and its validators
    this.freelingForm = this.formBuilder.group({
      medicalReport: ['', [Validators.required, Validators.maxLength(this.MAX_CHARACTERS)]],
    })

    // Init some atributes
    this.words = []
    this.downloadFilename = 'temu_pos_medical_tagger.json'
  }

  // -------------------------------------------------------------------------

  /**
   * Convenience getter for easy access to form fields from HTML template.
   */
  get f() { return this.freelingForm.controls }

  /**
   * Load a sample text to quickly test the web app.
   */
  loadSampleText(content: string) {
    this.freelingForm.get('medicalReport').setValue(content)
  }

  /**
   * Get the resulting POS tags from our REST API through the Freeling service.
   */
  getPosTags() {
    this.freelingService.getPosTags(this.freelingForm.value)
      .subscribe(
        // 1. API response
        response => {
          this.response = response

          // Prepare the words array to display.
          this.words = []
          this.scores = []
          response.data.sentences.forEach((sentence: Sentence) => {
            sentence.words.forEach((word: Word) => {
              // Add an extra column for sentenceId to each word.
              word.sentenceId = sentence.id
              this.words.push(word)
              this.scores.push(word.score)
            })
          })
        },

        // 2. Error handling
        error => alert(error),

        // 3. Complete
        () => {
          // Calculate the average score
          this.averageScore = Utils.round(Utils.getAverage(this.scores), 6)

          // Inform the user when data has been retrieved
          this.snackBar.open(this.response.message, 'OK', {
            duration: 4000
          })

          // Generate the download URI
          this.downloadLink = Utils.generateDownloadJsonUri(this.response, this.sanitizer)
        }
      )
  }

}
