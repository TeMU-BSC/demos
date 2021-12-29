import { Component, ViewChild, OnInit } from '@angular/core';
import { Annotation, NgxAnnotateTextComponent } from 'ngx-annotate-text';
import { ViewEncapsulation } from '@angular/core';
import { Project, PROJECTS } from 'src/app/shared/projects';
import { FormGroup } from '@angular/forms';
import { DrugprotService } from './drugprot.service';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { PageEvent } from '@angular/material/paginator';
import { SelectionModel } from '@angular/cdk/collections';
import { DomSanitizer, SafeUrl } from '@angular/platform-browser'
import { Utils } from 'src/app/shared/utils'
import { TemuResponse } from 'src/app/shared/api.shared'
import { ngxCsv } from 'ngx-csv/ngx-csv';
import { HttpClient } from '@angular/common/http';
import { Renderer2, ElementRef, Inject } from '@angular/core';
import { DOCUMENT } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
declare const Util: any;
import { RouterModule, Routes } from '@angular/router';

import * as $ from 'jquery';
// import { type } from 'os';


export interface AnnotationSnomed {
  type: string
  code: string
  text: string

}


@Component({
  selector: 'app-drugprot',
  templateUrl: './drugprot.component.html',
  styleUrls: ['./drugprot.component.css']
})
export class DrugprotComponent implements OnInit {
  @ViewChild('annotateText') ngxAnnotateText: NgxAnnotateTextComponent;
  displayedColumns: string[] = ['type', 'code', 'text'];
  dataSource: MatTableDataSource<AnnotationSnomed>;
  selection = new SelectionModel<AnnotationSnomed>(true, []);
  private paginator: MatPaginator;
  private sort: MatSort;
  textInputForm: FormGroup;
  loading = false;
  ready = false;
  downloadFilename: string
  annotation_mesh: AnnotationSnomed[] = [];
  ner_type: string = "";
  toggle = {
    'enfermedad': true,
    'sintoma': true,
    'farmaco': true,
    'procedimiento': true
  }
  brat: any
  format_BRAT = []
  downloadLink: SafeUrl
  response: TemuResponse
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
  tutorial = [
    {
      "image": "assets/images/Tutorial/ima1.png",
      "text": "You can find a Text area field that allows you to input a text, or if you prefere to upload a file, you can do it by clicking on the button \"Select file \" it has to be a .txt file",
      "title": "Upload a text file or type a text",
      "alt": "step1"
    },
    {
      "image": "assets/images/Tutorial/ima2.png",
      "text": "After typing your text or upload a file, you can click on the button \"SEND\" to start the analysis of the data.",
      "title": "Send text to the server",
      "alt": "step2"
    },
    {
      "image": "assets/images/Tutorial/ima3.png",
      "text": "Once the data is analized by our the DrugProt deep learning model, you will see the results in a colorful text area, it will be highlighted with the name of the entity that was detected.",
      "title": "Results of the analysis",
      "alt": "step3"
    },
    {
      "image": "assets/images/Tutorial/ima4.png",
      "text": "You could also download the results that we have analyzed in a .json file, you can do it by clicking on the button \"JSON\" or TSV  and CSV if you prefer",
      "title": "Download results",
      "alt": "step4"
    },
    {
      "image": "assets/images/Tutorial/ima6.png",
      "text": "As you can see the JSON result is a very simple format, it contains the text that was analyzed, the entities detected and the type of entity. You can also download the results in TSV and CSV format.",
      "title": "Download JSON",
      "alt": "step5"
    },
    {
      "image": "assets/images/Tutorial/ima7.png",
      "text": "This TSV file is a tab separated values file, We followed BRAT annotation format. It contains the text that was analyzed, the entities detected and the type of entity. You can also download the results in JSON and CSV format.",
      "title": "Download TSV",
      "alt": "step6"
    },
    {
      "image": "assets/images/Tutorial/ima8.png",
      "text": "This CSV file is a comma separated values file, We followed BRAT annotation format. It contains the text that was analyzed, the entities detected and the type of entity. You can also download the results in JSON and TSV format.",
      "title": "Download CSV",
      "alt": "step7"
    },
    {
      "image": "assets/images/Tutorial/ima5.png",
      "text": "Want to try a different text? You can do it by clicking on the button \"BACK\" and start again.",
      "title": "Go Back",
      "alt": "step8"
    },


  ]



  label_colors = {
    'CHEMICAL': "#DA310C",
    'GENE': "#9FDA0C",
    'FARMACO': "#0C25DA",
    'SINTOMA': "#527259"
  }

  proccedText = "";
  //This variable stores the input from the user, it should be a clinical story in spanish.
  inputText: string = "Ovarian Cancer Cells Emerges mTOR and HSP27 as Targets for Sensitization Strategies.  The microenvironment possesses a strong impact on the tumor chemoresistance when cells bind to components of the extracellular matrix. Here we elucidate the signaling pathways of cisplatin resistance in W1 ovarian cancer cells binding to collagen type 1 (COL1) and signaling interference with constitutive cisplatin resistance in W1CR cells to discover the targets for sensitization. Proteome kinase arrays and Western blots were used to identify the signaling components, their impact on cisplatin resistance was evaluated by inhibitory or knockdown approaches. W1 cell binding to COL1 upregulates integrin-associated signals via FAK/PRAS40/mTOR, confirmed by β1-integrin (ITGB1) knockdown. mTOR appears as key for resistance, its blockade reversed COL1 effects on W1 cell resistance completely. W1CR cells compensate ITGB1-knockdown by upregulation of discoidin domain receptor 1 (DDR1) as alternative COL1 sensor. COL1 binding via DDR1 activates the MAPK pathway, of which JNK1/2 appears critical for COL1-mediated resistance. JNK1/2 inhibition inverts COL1 effects in W1CR cells, whereas intrinsic cisplatin resistance remained unaffected. Remarkably, knockdown of HSP27, another downstream MAPK pathway component overcomes intrinsic resistance completely sensitizing W1CR cells to the level of W1 cells for cisplatin cytotoxicity. Our data confirm the independent regulation of matrix-induced and intrinsic chemoresistance in W1 ovarian cancer cells and offer novel targets for sensitization.";
  //This variables stores the state of the submittion, if the user has not submitted anything, then the annotation component should
  // not be visible.
  textSubmitted: boolean = false;

  next_ner = "";


  constructor(
    private sanitizer: DomSanitizer,
    private dataSvc: DrugprotService,
    private http: HttpClient,
    private router: ActivatedRoute,
    private route: Router,

  ) { this.dataSource = new MatTableDataSource([]); }

  project: Project;
  annotations: Annotation[] = [];
  originalAnnotations: Annotation[] = [];
  ngOnInit() {
    this.ner_type = this.router.snapshot.paramMap.get('id')
    this.ner_type == "gene" ? this.next_ner = "Chemical Tagger" : this.next_ner = "Gene Tagger"
    const str = this.ner_type;
    const str2 = str.charAt(0).toUpperCase() + str.slice(1);

    // Set the current project demo
    PROJECTS.forEach((project, index) => {
      if (project.name === 'DrugProt ' + str2 + ' Tagger') {
        this.project = PROJECTS[index]
      }
    })
    this.downloadFilename = "NER_Predictions.json"


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

  reset() {
    this.ready = false;
    this.annotations = [];
    this.annotation_mesh = [];
  }

  sanitizeString(str) {
    str = str.replace(/[^a-z0-9áéíóúñü \.,_-]/gim, "");
    return str.trim();
  }


  submitText() {
    this.loading = true;
    // this.inputText = this.inputText.replace(/\n/g, "\\n")
    let dic = {
      // INPUTTEXT: this.sanitizeString(this.inputText)
      INPUTTEXT: this.inputText,
      MODEL: this.ner_type
    }
    console.log(dic)


    this.dataSvc.getAnnotations(dic).subscribe(data => {

      this.response = data
      this.brat = data
      console.log(this.response)
      let annotaciones: [] = data


      annotaciones.map(d => {
        this.annotations = this.annotations.concat(
          new Annotation(
            parseInt(d["start"]),
            parseInt(d["end"]),
            d["type"],
            this.label_colors[d["type"]],
          ),
        );

        // const annt: AnnotationSnomed = {
        //   type: d["B-TYPE"],
        //   code: d["F-snomed"],
        //   text: d["E-text"],
        // }
        // this.annotation_mesh.push(annt)

      })

      this.originalAnnotations = this.annotations;

    }, err => { }, () => {
      // this.inputText = this.inputText.replace(/\\n/g, " \n")
      this.proccedText = this.inputText;
      this.textSubmitted = true;
      this.ready = true;
      this.loading = false;
      this.dataSource = new MatTableDataSource(this.annotation_mesh);

      this.dataSource.paginator = this.paginator;
      this.dataSource.sort = this.sort;
      // this.getMeshFunc();

      // Generate the download URI

      let t = 0
      this.brat.map(d => {

        this.format_BRAT.push({
          "A-id": "T" + t,
          "B-start": d["start"],
          "C-end": d["end"],
          "D-type": d["type"],
          "F-text": d["text"]
        })
        t = t + 1
      })
      this.downloadLink = Utils.generateDownloadJsonUri(
        this.format_BRAT,
        this.sanitizer
      )

    }
    )
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
    if (this.dataSource.paginator) {
      this.dataSource.paginator.firstPage();
    }
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
  checkboxLabel(row?: AnnotationSnomed): string {
    if (!row) {
      return `${this.isAllSelected() ? 'deselect' : 'select'} all`;
    }
    return `${this.selection.isSelected(row) ? 'deselect' : 'select'} row ${row.text}`;
  }

  onChange(fileList: FileList): void {
    let file = fileList[0];


    if (file.type == "text/plain") {
      let fileReader: FileReader = new FileReader();
      let self = this;
      fileReader.onloadend = function (x) {
        self.inputText = fileReader.result as string
        //self.inputText = self.inputText.replace(/\n/g, "\\n")

      }
      fileReader.readAsText(file);
    }
    if (file.type == "application/json") {
      this.dataSvc.getAnnotations(file).subscribe(ans => {

      })
    }
  }

  downloadTSV() {

    var options = {
      fieldSeparator: '\t',
      quoteStrings: '',
      decimalseparator: '.',
      showLabels: true,
      showTitle: false,
      title: 'NER_Predictions',
      useBom: false,
      noDownload: false,
      headers: ["ID", "START", "END", "TYPE", "TEXT"]
    };
    new ngxCsv(this.format_BRAT, 'NER_Predictions', options);
  }

  downloadCSV() {

    var options = {
      fieldSeparator: ',',
      quoteStrings: '',
      decimalseparator: '.',
      showLabels: true,
      showTitle: false,
      title: 'NER_Predictions',
      useBom: false,
      noDownload: false,
      headers: ["ID", "START", "END", "TYPE", "TEXT"]
    };
    new ngxCsv(this.format_BRAT, 'NER_Predictions', options);
  }



  changeNER(type: string) {
    console.log("click")
    this.dropResults(type)
    this.toggle[type] = !this.toggle[type]


  }

  dropResults(type) {

    this.toggle[type] ? this.annotations = this.annotations.filter(ann => ann["label"] != type.toUpperCase()) : this.annotations = this.annotations.concat(this.originalAnnotations.filter(ann => ann["label"] == type.toUpperCase()))


  }

  getData(code) {

    if (code == "NIL") {
      return "No se encontro termino"
    }
    else {
      code = code.split("+");

      return "None"
    }

  }

  tabchanged(event) {
    console.log(event)
    if (event == 5 && this.ner_type == "gene"){
      console.log("cambia")
      this.route.navigate(['/drugprot/chemical']).then(page => { window.location.reload(); });
    }
    if (event == 5 && this.ner_type == "chemical"){
      console.log("cambia")
      this.route.navigate(['/drugprot/gene']).then(page => { window.location.reload(); });
    }
  }






}
