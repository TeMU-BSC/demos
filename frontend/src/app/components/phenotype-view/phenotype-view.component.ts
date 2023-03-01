import { SelectionModel } from '@angular/cdk/collections';
import { Project, PROJECTS } from 'src/app/shared/projects'
import { Component, OnInit } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { TemuResponse } from 'src/app/shared/api.shared';
import { AnnotationSnomed } from '../ner-bsc/ner-bsc.component';
import { DomSanitizer, SafeUrl } from '@angular/platform-browser'
import { ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { PhenotypeViewService } from './phenotype-view.service'
@Component({
  selector: 'app-phenotype-view',
  templateUrl: './phenotype-view.component.html',
  styleUrls: ['./phenotype-view.component.css']
})
export class PhenotypeViewComponent implements OnInit {
  originalAnnotations: any[];
  originalBRATAnnotations: any[];
  constructor(
    private sanitizer: DomSanitizer,
    private http: HttpClient,
    private router: ActivatedRoute,
    private dataSvc: PhenotypeViewService
  ) {
    this.dataSource = new MatTableDataSource([])
  }

  dataSource: MatTableDataSource<AnnotationSnomed>
  selection = new SelectionModel<AnnotationSnomed>(true, [])
  private paginator: MatPaginator
  private sort: MatSort
  textInputForm: FormGroup
  loading = false
  ready = false
  downloadFilename: string
  annotation_mesh: AnnotationSnomed[] = []
  ner_type: string = ''
  toggle = {
    PHENOTYPE: true,
    HPO: true,
    DISEASE: true,
    SYMPTOM: true,
  }
  docData = {}
  project: Project
  downloadLink: SafeUrl
  response: TemuResponse

  brat_annotations: any[] = []
  originalBRATannotatios: any[] = []
  proccedText = ''
  //This variable stores the input from the user, it should be a clinical story in spanish.
  inputText: string = ""
  //This variables stores the state of the submittion, if the user has not submitted anything, then the annotation component should
  // not be visible.
  textSubmitted: boolean = false




  ngOnInit(): void {
    this.http.get('assets/text/fenotipos.txt', { responseType: 'text' })
      .subscribe(text_file => this.inputText = text_file, error => console.log(error));


    // Set the current project demo
    PROJECTS.forEach((project, index) => {
      if (project.routerLink === "/phenotype_visualizer") {
        this.project = PROJECTS[index]
      }
    })
    this.downloadFilename = 'NER_Predictions.json'
  }

  submitText() {
    this.loading = true
    // this.inputText = this.inputText.replace(/\n/g, "\\n")
    let dic = {
      // INPUTTEXT: this.sanitizeString(this.inputText)
      INPUTTEXT: this.inputText,
      MODELS: ["Phenotypes_1", "Phenotypes_2"],
    }



    this.dataSvc.getPhenotypeAnnotations(dic).subscribe(
      data => {

        this.brat_annotations = []
        this.originalAnnotations = []
        this.response = data
        let annotaciones: [] = data['INPUTTEXT']
        annotaciones.map(d => {
          let newAnnot = []

          newAnnot[0] = d['A-ID']
          newAnnot[1] = d['B-TYPE']
          newAnnot[2] = [[parseInt(d['C-START']), parseInt(d['D-END'])]]
          this.brat_annotations.push(newAnnot)

        })
        this.originalBRATannotatios = this.brat_annotations
        this.docData = {
          text: this.inputText,
          entities: this.brat_annotations,
        }
      },
      error => { },
      () => {

        this.proccedText = this.inputText
        this.textSubmitted = true
        this.ready = true
        this.loading = false

      }
    )
  }

  clearText() {
    this.inputText = ''
  }
  reset() {
    this.ready = false
  }


  changeNER(type: string) {
    this.dropResults(type)
    this.toggle[type] = !this.toggle[type]
    this.docData = {
      text: this.inputText,
      entities: this.brat_annotations,
    }
  }

  dropResults(type) {
    this.toggle[type]
      ? (this.brat_annotations = this.brat_annotations.filter(
        ann => ann[1].toUpperCase() != type.toUpperCase()
      ))
      : (this.brat_annotations = this.brat_annotations.concat(
        this.originalBRATannotatios.filter(
          ann => ann[1].toUpperCase() == type.toUpperCase()
        )
      ))
  }

}
