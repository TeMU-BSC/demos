import { Component, Input, OnInit, OnChanges, SimpleChanges, Renderer2 } from '@angular/core';
declare const Util: any;
import * as $ from 'jquery';
import { ViewEncapsulation } from '@angular/core';

import { ElementRef, ViewChild } from '@angular/core';


@Component({
  selector: 'app-brat-display',
  templateUrl: './brat-display.component.html',
  styleUrls: ['./brat-display.component.css'],
  // encapsulation: ViewEncapsulation.Emulated
})
export class BratDisplayComponent implements OnInit, OnChanges {

  @Input() bratData: any;


  constructor() { }



  bratLocation = 'https://temu.bsc.es/.bio-playground-VIEJO';

  webFontURLs = [
    this.bratLocation + '/static/fonts/Astloch-Bold.ttf',
    this.bratLocation + '/static/fonts/PT_Sans-Caption-Web-Regular.ttf',
    this.bratLocation + '/static/fonts/Liberation_Sans-Regular.ttf'
  ]

  collData = {
    entity_types: [{
      type: 'ENFERMEDAD',
      labels: ['ENFERMEDAD', 'ENFERMEDAD'],
      bgColor: '#7fa2ff',
      borderColor: 'darken',
      fgColor: "white"
    },
    {
      type: 'PROCEDIMIENTO',
      labels: ['PROCEDIMIENTO', 'PROCEDIMIENTO'],
      bgColor: '#7fa32f',
      borderColor: 'darken',
      fgColor: "white"
    },
    {
      type: 'FARMACO',
      labels: ['FARMACO', 'FARMACO'],
      bgColor: '#0C25DA',
      borderColor: 'darken',
      fgColor: "white"
    },
    {
      type: 'SINTOMA',
      labels: ['SINTOMA', 'SINTOMA'],
      bgColor: '#527259',
      borderColor: 'darken',
      fgColor: "white"
    },
    {
      type: 'SYMPTOM',
      labels: ['SYMPTOM', 'SYMPTOM'],
      bgColor: '#6db2e5',
      borderColor: 'darken',
      fgColor: "white"
    }
      ,
    {
      type: 'DISEASE',
      labels: ['DISEASE', 'DISEASE'],
      bgColor: '#e56d88',
      borderColor: 'darken',
      fgColor: "white"
    },
    {
      type: 'PHENOTYPE',
      labels: ['PHENOTYPE', 'PHENOTYPE'],
      bgColor: '#6de5bf',
      borderColor: 'darken',
      fgColor: "black"
    },
    {
      type: 'HPO',
      labels: ['HPO', 'HPO'],
      bgColor: '#b6f7dc',
      borderColor: 'darken',
      fgColor: "black"
    },
    ]
  };


  ngOnInit(): void {
    //this.mydiv.nativeElement.innerHTML = '<div id="embedding-entity-example" style="width: 100rem;"></div>'

    Util.embed('embedding-entity-example', $.extend({}, this.collData),
      $.extend({}, this.bratData), this.webFontURLs);


  }
  @ViewChild('mydiv') mydiv: ElementRef;

  ngOnChanges(changes: SimpleChanges): void {

    setTimeout(() => {
      this.mydiv.nativeElement.innerHTML = '<div id="embedding-entity-example" style="display: block; width: 70vw;margin-left: auto;margin-right: auto;"></div>'
      Util.embed('embedding-entity-example', $.extend({}, this.collData),
        $.extend({}, this.bratData), this.webFontURLs);
    }, 10)


  }


}
