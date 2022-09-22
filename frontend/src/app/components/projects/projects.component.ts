import { Component, OnInit } from '@angular/core'
import { PROJECTS } from 'src/app/shared/projects'
import { TemuResponse } from 'src/app/shared/api.shared'
import { HttpClient } from '@angular/common/http'
import { ProjectsService } from './projects.service'
import { ActivatedRoute, Router } from '@angular/router'
import { MatTableDataSource } from '@angular/material/table'

@Component({
  selector: 'app-projects',
  templateUrl: './projects.component.html',
  styleUrls: ['./projects.component.css']
})
export class ProjectsComponent implements OnInit {

  constructor(

    private dataSvc: ProjectsService,
    private http: HttpClient,
    private router: ActivatedRoute,
    private route: Router
  ) {

  }

  projects = PROJECTS

  ngOnInit(): void {
    this.dataSvc.getModelsInfo().subscribe(
      data => {
        let modelds = data
        modelds.map(d => {
          if (d["model_type"] == "spacy") {
            d["routerLink"] = "ner_v2/" + d["route"]
          }
        }
        )
        this.projects = this.projects.concat(modelds)
        console.log(this.projects)
      },
      error => { },
      () => { }
    )
  }










}
