import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { DomSanitizer, SafeUrl } from '@angular/platform-browser';
import { ActivatedRoute } from '@angular/router';
import { TemuResponse } from 'src/app/shared/api.shared';
import { PROJECTS } from 'src/app/shared/projects';
import { SpacyDoctornlpService } from './spacy-doctornlp.service'
import {
  FormBuilder,
  FormGroup,
  FormArray,
  FormControl,
  ValidatorFn
} from '@angular/forms';
@Component({
  selector: 'app-spacy-doctornlp',
  templateUrl: './spacy-doctornlp.component.html',
  styleUrls: ['./spacy-doctornlp.component.css']
})
export class SpacyDoctornlpComponent implements OnInit {

  checked = false;
  indeterminate = false;
  labelPosition: 'before' | 'after' = 'after';
  disabled = false;
  inputText: string = ""
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
  ner_list = []
  form: FormGroup;
  selectedOrderIds = []

  constructor(private sanitizer: DomSanitizer,
    private dataSvc: SpacyDoctornlpService,
    private http: HttpClient,
    private router: ActivatedRoute,
    private formBuilder: FormBuilder) {
    this.form = this.formBuilder.group({ orders: new FormArray([]) });
  }

  get ordersFormArray() {
    return this.form.controls.orders as FormArray;
  }

  ngOnInit(): void {

    this.dataSvc.getModelsInfo().subscribe(
      data => {

        let modelds = data

        modelds.map(d => {
          let mod = {}
          mod["name"] = d["name"]
          mod['model'] = d['route']
          this.ner_list.push(mod)
        })
        this.projects = this.projects.concat(modelds)
      },
      error => { },
      () => {
        // Set the current project demo
        this.projects.forEach((project, index) => {
          if (project.model === "doctorNLP") {
            this.project = this.projects[index]
          }
        })
        this.ner_list.forEach(() => this.ordersFormArray.push(new FormControl(false)));


      }
    )
  }

  submit() {


    console.log(this.selectedOrderIds);
  }

  submitText() {
    this.selectedOrderIds = this.form.value.orders
      .map((checked, i) => checked ? this.ner_list[i].model : null)
      .filter(v => v !== null);
    console.log(this.selectedOrderIds)
    this.loading = true
    let dic = {
      // INPUTTEXT: this.sanitizeString(this.inputText)
      INPUTTEXT: this.inputText,
      MODEL: this.selectedOrderIds,
    }

    this.dataSvc.getSpacyAllNERsAnnotations(dic).subscribe(
      data => {
        console.log(data)
      },
      error => { },
      () => {
      }
    )
  }

}
