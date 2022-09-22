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
  inputText: string =
    'Mujer de 59 años cuyos antecedentes personales incluyen hipertensión arterial, artropatía degenerativa cervical, lumbociática crónica, tuberculosis ganglionar diagnosticada por cuadro de eritema nudoso y migraña. En su tratamiento habitual, destaca el candesartán 32 mg/día.﻿Acudió en marzo de 2020 al servicio de urgencias por sensación distérmica de 5 días de evolución, acompañada de dolor torácico de características opresivas en ausencia de síntomas respiratorios. A su llegada presentaba SatO2 del 96% con gafas nasales a 2 l/min y presión arterial de 75/53 mmHg. En la exploración física destacan signos de hipoperfusión periférica con auscultación respiratoria normal. A pesar de la sobrecarga hídrica y la noradrenalina, persistía hipotensa con signos de hipoperfusión (frialdad cutánea y ácidos lácticos elevados: 3,9 mmol/l). En el electrocardiograma destacaba elevación cóncava del ST y descenso del PR, así como bajos voltajes. En la radiografía de tórax se observaron ligeros signos de redistribución vascular sin infiltrados. La reacción en cadena de la polimerasa (PCR) de virus del frotis nasofaríngeo resultó positiva para SARS-CoV-2 y negativo para adenovirus y virus Influenza A y B, con un ambiente epidemiológico positivo (familiares con fiebre y cuadro respiratorio días previos). Entre los datos del laboratorio, destacaba la elevación de troponinas (TnT, 220-1.100 ng/dl) y NT-proBNP (4.421 ng/l), ligera leucocitosis (14,17 × 109/l), linfocitos (2,59 × 109/l), PCR 10 mg/l y dímero D a las 24 h (23.242 ng/ml). Una ecocardiografía mostró hipertrofia concéntrica moderada, volúmenes intraventriculares disminuidos con fracción de eyección del ventrículo izquierdo conservada sin segmentarismos y derrame pericárdico moderado sin claros signos de deterioro hemodinámico. Debido al cuadro tan indicativo de miocarditis (elevación concaviforme y difusa del ST, fiebre, derrame pericárdico y engrosamiento miocárdico) y la fracción de eyección del ventrículo izquierdo conservada sin segmentarismos, no se realizó coronariografía por baja sospecha clínica de síndrome coronario agudo. En la unidad coronaria, durante el implante de un catéter de Swan-Ganz, se produjo un rápido deterioro hemodinámico hasta llegar a una actividad eléctrica sin pulso que requirió reanimación cardiopulmonar, pericardiocentesis emergente (drenaje de líquido seroso) y altas dosis de vasopresores para la recuperación hemodinámica de la paciente. Se realizó otro ecocardiograma (a las 2 h del ingreso), que mostró disfunción biventricular grave y edema miocárdico difuso, por lo que se decidió implantar un balón de contrapulsación y oxigenador extracorpóreo de membrana (ECMO) venoarterial femoral.'
  inputText1 = ""
  inputText2 = ""
  texto_recibido = ""
  ngOnInit(): void {
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
