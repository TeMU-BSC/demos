import { Component, OnInit } from '@angular/core';
import { PROJECTS } from 'src/app/shared/projects';

@Component({
  selector: 'app-sidenav',
  templateUrl: './sidenav.component.html',
  styleUrls: ['./sidenav.component.css']
})
export class SidenavComponent implements OnInit {

  projects = PROJECTS

  constructor() { }

  ngOnInit() {
  }

}
