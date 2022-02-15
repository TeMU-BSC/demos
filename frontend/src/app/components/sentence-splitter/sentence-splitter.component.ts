import { Component, OnInit } from '@angular/core';
import { Project, PROJECTS } from 'src/app/shared/projects';

@Component({
  selector: 'app-sentence-splitter',
  templateUrl: './sentence-splitter.component.html',
  styleUrls: ['./sentence-splitter.component.css']
})
export class SentenceSplitterComponent implements OnInit {

  project: Project

  constructor() { }

  ngOnInit(): void {
    PROJECTS.forEach((project, index) => {
      if (project.name === 'Sentence Splitter') {
        this.project = PROJECTS[index]
      }
    })

  }
}
