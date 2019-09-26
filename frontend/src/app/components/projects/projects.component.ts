import { Component, OnInit } from '@angular/core'
import { PROJECTS } from 'src/app/shared/projects'
import { Router } from '@angular/router'

@Component({
  selector: 'app-projects',
  templateUrl: './projects.component.html',
  styleUrls: ['./projects.component.css']
})
export class ProjectsComponent implements OnInit {

  projects = PROJECTS

  constructor(private router: Router) { }

  ngOnInit() {
  }

}
