import { Component, OnInit } from '@angular/core'
import { PROJECTS } from 'src/app/shared/projects'

@Component({
  selector: 'app-projects',
  templateUrl: './projects.component.html',
  styleUrls: ['./projects.component.css']
})
export class ProjectsComponent implements OnInit {

  projects = PROJECTS

  constructor() { }

  ngOnInit() {
  }

}
