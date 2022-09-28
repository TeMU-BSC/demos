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

@Component({
  selector: 'app-phenotype-view',
  templateUrl: './phenotype-view.component.html',
  styleUrls: ['./phenotype-view.component.css']
})
export class PhenotypeViewComponent implements OnInit {
  constructor(
    private sanitizer: DomSanitizer,
    private http: HttpClient,
    private router: ActivatedRoute
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
    enfermedad: true,
    sintoma: true,
    farmaco: true,
    procedimiento: true,
  }
  docData = {}
  project: Project
  downloadLink: SafeUrl
  response: TemuResponse

  brat_annotations: any[] = []

  proccedText = ''
  //This variable stores the input from the user, it should be a clinical story in spanish.
  inputText: string =
    'Mujer de 59 años cuyos antecedentes personales incluyen hipertensión arterial, artropatía degenerativa cervical, lumbociática crónica, tuberculosis ganglionar diagnosticada por cuadro de eritema nudoso y migraña. En su tratamiento habitual, destaca el candesartán 32 mg/día.﻿Acudió en marzo de 2020 al servicio de urgencias por sensación distérmica de 5 días de evolución, acompañada de dolor torácico de características opresivas en ausencia de síntomas respiratorios. A su llegada presentaba SatO2 del 96% con gafas nasales a 2 l/min y presión arterial de 75/53 mmHg. En la exploración física destacan signos de hipoperfusión periférica con auscultación respiratoria normal. A pesar de la sobrecarga hídrica y la noradrenalina, persistía hipotensa con signos de hipoperfusión (frialdad cutánea y ácidos lácticos elevados: 3,9 mmol/l). En el electrocardiograma destacaba elevación cóncava del ST y descenso del PR, así como bajos voltajes. En la radiografía de tórax se observaron ligeros signos de redistribución vascular sin infiltrados. La reacción en cadena de la polimerasa (PCR) de virus del frotis nasofaríngeo resultó positiva para SARS-CoV-2 y negativo para adenovirus y virus Influenza A y B, con un ambiente epidemiológico positivo (familiares con fiebre y cuadro respiratorio días previos). Entre los datos del laboratorio, destacaba la elevación de troponinas (TnT, 220-1.100 ng/dl) y NT-proBNP (4.421 ng/l), ligera leucocitosis (14,17 × 109/l), linfocitos (2,59 × 109/l), PCR 10 mg/l y dímero D a las 24 h (23.242 ng/ml). Una ecocardiografía mostró hipertrofia concéntrica moderada, volúmenes intraventriculares disminuidos con fracción de eyección del ventrículo izquierdo conservada sin segmentarismos y derrame pericárdico moderado sin claros signos de deterioro hemodinámico. Debido al cuadro tan indicativo de miocarditis (elevación concaviforme y difusa del ST, fiebre, derrame pericárdico y engrosamiento miocárdico) y la fracción de eyección del ventrículo izquierdo conservada sin segmentarismos, no se realizó coronariografía por baja sospecha clínica de síndrome coronario agudo. En la unidad coronaria, durante el implante de un catéter de Swan-Ganz, se produjo un rápido deterioro hemodinámico hasta llegar a una actividad eléctrica sin pulso que requirió reanimación cardiopulmonar, pericardiocentesis emergente (drenaje de líquido seroso) y altas dosis de vasopresores para la recuperación hemodinámica de la paciente. Se realizó otro ecocardiograma (a las 2 h del ingreso), que mostró disfunción biventricular grave y edema miocárdico difuso, por lo que se decidió implantar un balón de contrapulsación y oxigenador extracorpóreo de membrana (ECMO) venoarterial femoral. Se inició el tratamiento de la miocarditis con inmunoglubulinas (80 mg/día) durante 4 días y metilprenisolona (500 mg/día) en pauta descendente durante 14 días y tratamiento antiviral: IFN B (0,25 mg/48 h) y (ritonavir 400 mg/lopinavir 100 mg/12 h). Al quinto día de ingreso, se constató la normalización de la función biventricular, pero se mantuvo el dispositivo ECMO por la disnea, con hipoxemia refractaria, actualmente pendiente de progreso respiratorio.'
  //This variables stores the state of the submittion, if the user has not submitted anything, then the annotation component should
  // not be visible.
  textSubmitted: boolean = false




  ngOnInit(): void {


    // Set the current project demo
    PROJECTS.forEach((project, index) => {
      if (project.routerLink === "/phenotype_visualizer") {
        this.project = PROJECTS[index]
      }
    })
    this.downloadFilename = 'NER_Predictions.json'
  }

}
