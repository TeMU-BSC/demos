import { Component, ViewChild, OnInit } from '@angular/core';
import { Annotation, NgxAnnotateTextComponent } from 'ngx-annotate-text';
import { ViewEncapsulation } from '@angular/core';
import { Project, PROJECTS } from 'src/app/shared/projects';
import { FormGroup } from '@angular/forms';
import { NerService } from './ner.service';

@Component({
  selector: 'app-ner-bsc',
  templateUrl: './ner-bsc.component.html',
  styleUrls: ['./ner-bsc.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class NerBscComponent implements OnInit {

  @ViewChild('annotateText') ngxAnnotateText: NgxAnnotateTextComponent;
  textInputForm: FormGroup;
  //This variable stores the input from the user, it should be a clinical story in spanish.
  inputText: string;
  //This variables stores the state of the submittion, if the user has not submitted anything, then the annotation component should
  // not be visible.
  textSubmitted: boolean = false;

  constructor(
    private dataSvc: NerService
  ) { }

  project: Project;
  annotations: Annotation[] = [
    new Annotation(577, 595, 'PROCEDIMIENTO', '#0069d9'),
    new Annotation(644, 669, 'PROCEDIMIENTO', '#0069d9'),
    new Annotation(844, 862, 'PROCEDIMIENTO', '#0069d9'),
    new Annotation(948, 968, 'PROCEDIMIENTO', '#0069d9'),
    new Annotation(1100, 1119, 'PROCEDIMIENTO', '#0069d9'),
    new Annotation(1542, 1557, 'PROCEDIMIENTO', '#0069d9'),
    new Annotation(2036, 2051, 'PROCEDIMIENTO', '#0069d9'),
    new Annotation(2151, 2177, 'PROCEDIMIENTO', '#0069d9'),
    new Annotation(577, 595, 'PROCEDIMIENTO', '#0069d9'),
    new Annotation(2285, 2311, 'PROCEDIMIENTO', '#0069d9'),
    new Annotation(2313, 2341, 'PROCEDIMIENTO', '#0069d9'),
    new Annotation(2343, 2361, 'PROCEDIMIENTO', '#0069d9'),
    new Annotation(2384, 2399, 'PROCEDIMIENTO', '#0069d9'),
    new Annotation(2466, 2480, 'PROCEDIMIENTO', '#0069d9'),
    new Annotation(2610, 2673, 'PROCEDIMIENTO', '#0069d9'),
    new Annotation(2675, 2701, 'PROCEDIMIENTO', '#0069d9'),
  ];

  ngOnInit() {
    // Set the current project demo
    PROJECTS.forEach((project, index) => {
      if (project.name === 'NER') {
        this.project = PROJECTS[index]
      }
    })

  }
  addAnnotation(label: string, color: string) {
    if (this.ngxAnnotateText) {
      const selection = this.ngxAnnotateText.getCurrentTextSelection();
      if (selection) {
        this.annotations = this.annotations.concat(
          new Annotation(
            selection.startIndex,
            selection.endIndex,
            label,
            color,
          ),
        );
      }
    }
  }

  submitText() {
    this.textSubmitted = true;

    let dic = {
      INPUTTEXT: this.inputText
    }
    this.dataSvc.getAll(dic).subscribe(data => {
      console.log(data)
    })
  }
}
