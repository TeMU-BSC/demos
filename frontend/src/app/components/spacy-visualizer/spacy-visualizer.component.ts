import { Component, ViewChild, OnInit, Pipe } from '@angular/core'
import { Project, PROJECTS } from 'src/app/shared/projects'
import { TemuResponse } from 'src/app/shared/api.shared'
import { ngxCsv } from 'ngx-csv/ngx-csv'
import { HttpClient } from '@angular/common/http'
import { Renderer2, ElementRef, Inject } from '@angular/core'
import { ActivatedRoute } from '@angular/router'
import { Utils } from 'src/app/shared/utils'
import { DomSanitizer, SafeUrl } from '@angular/platform-browser'
import { SelectionModel } from '@angular/cdk/collections'
import { MatPaginator } from '@angular/material/paginator'
import { MatSort } from '@angular/material/sort'
import { MatTableDataSource } from '@angular/material/table'
import { FormGroup } from '@angular/forms'
import { SpacyVisualizerService } from './spacy-visualizer.service'

@Component({
  selector: 'app-spacy-visualizer',
  templateUrl: './spacy-visualizer.component.html',
  styleUrls: ['./spacy-visualizer.component.css'],
})
export default class SpacyVisualizerComponent implements OnInit {
  loading = false
  ready = false
  downloadFilename: string
  ner_type: string = ''
  docData = {}
  projects = PROJECTS
  downloadLink: SafeUrl
  response: TemuResponse
  project = PROJECTS[0]
  inputHTML = ''
  constructor(
    private sanitizer: DomSanitizer,
    private dataSvc: SpacyVisualizerService,
    private http: HttpClient,
    private router: ActivatedRoute,
  ) { }
  inputText: string = "hola"
  inputText1 = ""
  inputText2 = ""
  texto_recibido = ""
  ngOnInit(): void {
    this.http.get('assets/text/fenotipos.txt', { responseType: 'text' })
      .subscribe(text_file => console.log(text_file), error => console.log(error), () => console.log('completed'));
    this.ner_type = this.router.snapshot.paramMap.get('id')
    console.log(this.ner_type)
    this.dataSvc.getModelsInfo().subscribe(
      data => {
        let modelds = data
        modelds.map(d => {
          if (d['model_type'] == 'spacy') {
            d['routerLink'] = 'ner_v2/' + d['route']
          }
        })
        this.projects = this.projects.concat(modelds)
      },
      error => { },
      () => {
        // Set the current project demo
        this.projects.forEach((project, index) => {
          if (project.route === this.ner_type) {
            this.project = this.projects[index]
          }
        })
      }
    )
    this.downloadFilename = 'NER_Predictions.json'
  }

  clearText() {
    this.inputText = ''
  }
  reset() {
    this.ready = false
  }

  submitText() {
    this.loading = true
    let dic = {
      // INPUTTEXT: this.sanitizeString(this.inputText)
      INPUTTEXT: this.inputText,
      MODEL: this.project.route,
    }
    this.dataSvc.getSpacyNERAnnotations(dic).subscribe(
      data => {
        console.log(data)
        this.inputHTML = data['html']
      },
      error => { },
      () => {
        this.loading = false
        this.ready = true
      }
    )
  }

  submitText2() {
    console.log(this.inputText2)
  }
}
