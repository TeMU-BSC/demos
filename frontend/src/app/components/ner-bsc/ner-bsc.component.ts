import { Component, ViewChild } from '@angular/core';
import { Annotation, NgxAnnotateTextComponent } from 'ngx-annotate-text';
import { ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'app-ner-bsc',
  templateUrl: './ner-bsc.component.html',
  styleUrls: ['./ner-bsc.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class NerBscComponent {

  @ViewChild('annotateText') ngxAnnotateText: NgxAnnotateTextComponent;

  text: string = ' Mujer de 59 años cuyos antecedentes personales incluyen hipertensión arterial, artropatía degenerativa cervical, lumbociática crónica, tuberculosis ganglionar diagnosticada por cuadro de eritema nudoso y migraña. En su tratamiento habitual, destaca el candesartán 32 mg/día.﻿Acudió en marzo de 2020 al servicio de urgencias por sensación distérmica de 5 días de evolución, acompañada de dolor torácico de características opresivas en ausencia de síntomas respiratorios. A su llegada presentaba SatO2 del 96% con gafas nasales a 2 l/min y presión arterial de 75/53 mmHg. En la exploración física destacan signos de hipoperfusión periférica con auscultación respiratoria normal. A pesar de la sobrecarga hídrica y la noradrenalina, persistía hipotensa con signos de hipoperfusión (frialdad cutánea y ácidos lácticos elevados: 3,9 mmol/l). En el electrocardiograma destacaba elevación cóncava del ST y descenso del PR, así como bajos voltajes. En la radiografía de tórax se observaron ligeros signos de redistribución vascular sin infiltrados. La reacción en cadena de la polimerasa (PCR) de virus del frotis nasofaríngeo resultó positiva para SARS-CoV-2 y negativo para adenovirus y virus Influenza A y B, con un ambiente epidemiológico positivo (familiares con fiebre y cuadro respiratorio días previos). Entre los datos del laboratorio, destacaba la elevación de troponinas (TnT, 220-1.100 ng/dl) y NT-proBNP (4.421 ng/l), ligera leucocitosis (14,17 × 109/l), linfocitos (2,59 × 109/l), PCR 10 mg/l y dímero D a las 24 h (23.242 ng/ml). Una ecocardiografía mostró hipertrofia concéntrica moderada, volúmenes intraventriculares disminuidos con fracción de eyección del ventrículo izquierdo conservada sin segmentarismos y derrame pericárdico moderado sin claros signos de deterioro hemodinámico. Debido al cuadro tan indicativo de miocarditis (elevación concaviforme y difusa del ST, fiebre, derrame pericárdico y engrosamiento miocárdico) y la fracción de eyección del ventrículo izquierdo conservada sin segmentarismos, no se realizó coronariografía por baja sospecha clínica de síndrome coronario agudo. En la unidad coronaria, durante el implante de un catéter de Swan-Ganz, se produjo un rápido deterioro hemodinámico hasta llegar a una actividad eléctrica sin pulso que requirió reanimación cardiopulmonar, pericardiocentesis emergente (drenaje de líquido seroso) y altas dosis de vasopresores para la recuperación hemodinámica de la paciente. Se realizó otro ecocardiograma (a las 2 h del ingreso), que mostró disfunción biventricular grave y edema miocárdico difuso, por lo que se decidió implantar un balón de contrapulsación y oxigenador extracorpóreo de membrana (ECMO) venoarterial femoral. Se inició el tratamiento de la miocarditis con inmunoglubulinas (80 mg/día) durante 4 días y metilprenisolona (500 mg/día) en pauta descendente durante 14 días y tratamiento antiviral: IFN B (0,25 mg/48 h) y (ritonavir 400 mg/lopinavir 100 mg/12 h). Al quinto día de ingreso, se constató la normalización de la función biventricular, pero se mantuvo el dispositivo ECMO por la disnea, con hipoxemia refractaria, actualmente pendiente de progreso respiratorio. ';

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

}
