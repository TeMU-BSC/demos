import { Component } from '@angular/core'
import { PROJECTS } from 'src/app/shared/projects'

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css'],
})
export class HeaderComponent {
  demos = PROJECTS
}
