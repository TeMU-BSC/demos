import { Component } from '@angular/core'
import { PROJECTS } from 'src/app/shared/projects'

@Component({
  selector: 'app-projects',
  templateUrl: './projects.component.html',
  styleUrls: ['./projects.component.css']
})
export class ProjectsComponent {

  projects = PROJECTS

}
