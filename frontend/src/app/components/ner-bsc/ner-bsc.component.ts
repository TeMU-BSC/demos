import { Component, ViewChild, OnInit } from '@angular/core';
import { Annotation, NgxAnnotateTextComponent } from 'ngx-annotate-text';
import { ViewEncapsulation } from '@angular/core';
import { Project, PROJECTS } from 'src/app/shared/projects';
import { FormGroup } from '@angular/forms';
import { NerService } from './ner.service';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { PageEvent } from '@angular/material/paginator';
import { SelectionModel } from '@angular/cdk/collections';


export interface AnnotationMesh {
name: string;
occurrency: number;
code: string;
definition: string;
text: string;
}

@Component({
  selector: 'app-ner-bsc',
  templateUrl: './ner-bsc.component.html',
  styleUrls: ['./ner-bsc.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class NerBscComponent implements OnInit {

  @ViewChild('annotateText') ngxAnnotateText: NgxAnnotateTextComponent;
  displayedColumns: string[] = ['select','name', 'code', 'occurrency', 'text'];
  dataSource: MatTableDataSource<AnnotationMesh>;
  selection = new SelectionModel<AnnotationMesh>(true, []);
  private paginator: MatPaginator;
  private sort: MatSort;
  textInputForm: FormGroup;
  loading = false;
  @ViewChild(MatPaginator) set matPaginator(mp: MatPaginator) {
    this.paginator = mp;
    this.setDataSourceAttributes();
  }
  @ViewChild(MatSort) set matSort(ms: MatSort) {
    this.sort = ms;
    this.setDataSourceAttributes();
  }
  setDataSourceAttributes() {
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
  }

  proccedText = "";
  //This variable stores the input from the user, it should be a clinical story in spanish.
  inputText: string = "";
  //This variables stores the state of the submittion, if the user has not submitted anything, then the annotation component should
  // not be visible.
  textSubmitted: boolean = false;

  constructor(
    private dataSvc: NerService
  ) { this.dataSource = new MatTableDataSource([]); }

  project: Project;
  annotations: Annotation[] = [];

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

  sanitizeString(str) {
    str = str.replace(/[^a-z0-9áéíóúñü \.,_-]/gim, "");
    return str.trim();
  }

  submitText() {
    this.loading = true;
    let dic = {
      INPUTTEXT: this.sanitizeString(this.inputText)
    }
    this.dataSvc.getAnnotations(dic).subscribe(data => {
      this.annotations = []
      data["INPUTTEXT"].split("\n").map(a => {
        let inputtext = a.replaceAll('\t', " ");
        inputtext = inputtext.split(" ", 4);
        console.log(inputtext.length);
        if (inputtext.length > 1) {
          this.annotations = this.annotations.concat(
            new Annotation(
              parseInt(inputtext[2]),
              parseInt(inputtext[3]),
              inputtext[1],
              "#0069d9"
            )
          )
        }
      }
      );
    }, err => { }, () => {

      this.proccedText = this.sanitizeString(this.inputText);
      this.textSubmitted = true;

      this.getMeshFunc();

    })
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
    if (this.dataSource.paginator) {
      this.dataSource.paginator.firstPage();
    }
  }


  getMeshFunc(){

    let annot = []
    this.annotations.map(ann =>{

      annot.push(this.proccedText.substring(ann["startIndex"],ann["endIndex"]))
    })
    let annotation_mesh : AnnotationMesh [] = []
    this.dataSvc.getMesh(annot).subscribe(response =>{
      response.map(an =>{
        const annt : AnnotationMesh = {
          name: an["name"],
          code: an["code"],
          definition: an["description"],
          occurrency: 1,
          text: an["annotation"]
        }
        annotation_mesh.push(annt)
      })
      this.loading = false;
    }, error =>{}, () =>{
      this.dataSource = new MatTableDataSource(annotation_mesh);
      this.dataSource.paginator = this.paginator;
      this.dataSource.sort = this.sort;
    }

    )
  }
  /** Whether the number of selected elements matches the total number of rows. */
  isAllSelected() {
    const numSelected = this.selection.selected.length;
    const numRows = this.dataSource.data.length;
    return numSelected === numRows;
  }

  /** Selects all rows if they are not all selected; otherwise clear selection. */
  masterToggle() {
    if (this.isAllSelected()) {
      this.selection.clear();
      return;
    }

    this.selection.select(...this.dataSource.data);
  }

  /** The label for the checkbox on the passed row */
  checkboxLabel(row?: AnnotationMesh): string {
    if (!row) {
      return `${this.isAllSelected() ? 'deselect' : 'select'} all`;
    }
    return `${this.selection.isSelected(row) ? 'deselect' : 'select'} row ${row.text}`;
  }

  onChange(fileList: FileList): void {
    let file = fileList[0];
    console.log(fileList);

    if(file.type == "text/plain"){
    let fileReader: FileReader = new FileReader();
    let self = this;
    fileReader.onloadend = function(x) {
      self.inputText =  fileReader.result as string
    }
    fileReader.readAsText(file);
    }
    if(file.type == "application/json"){
      this.dataSvc.getAnnotations(file).subscribe(ans => {
        console.log(ans)
      })
    }
  }

}
