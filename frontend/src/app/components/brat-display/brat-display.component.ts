import { Component, Input, OnInit } from '@angular/core';
declare const Util: any;
import * as $ from 'jquery';
import { ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'app-brat-display',
  templateUrl: './brat-display.component.html',
  styleUrls: ['./brat-display.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class BratDisplayComponent implements OnInit {

  @Input() bratData: any;

  constructor() { }


  bratLocation = 'https://temu.bsc.es/bio-playground';

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
      borderColor: 'darken'
    },
    {
      type: 'PROCEDIMIENTO',
      labels: ['Proce', 'Proc'],
      bgColor: '#7fa32f',
      borderColor: 'darken'
    },
    {
      type: 'FARMACO',
      labels: ['FARMACO', 'FARMACO'],
      bgColor: '#0C25DA',
      borderColor: 'darken'
    },
    {
      type: 'SINTOMA',
      labels: ['SINTOMA', 'SINTOMA'],
      bgColor: '#527259',
      borderColor: 'darken'
    }]
  };

  ngOnInit(): void {

    setTimeout(() => {
      console.log(this.bratData)
      Util.embed('embedding-entity-example', $.extend({}, this.collData),
        $.extend({}, this.bratData), this.webFontURLs);
    }, 500)

  }

}
