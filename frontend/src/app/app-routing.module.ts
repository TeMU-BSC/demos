import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

// Projects
import { ComingSoonComponent } from './components/coming-soon/coming-soon.component';
import { SpacccPosTaggerComponent } from './components/spaccc-pos-tagger/spaccc-pos-tagger.component';
import { TranslatorComponent } from './components/translator/translator.component';
import { ProjectsComponent } from './components/projects/projects.component';


const routes: Routes = [
  { path: '', component: ProjectsComponent },
  { path: 'coming-soon', component: ComingSoonComponent },
  { path: 'spaccc-pos-tagger', component: SpacccPosTaggerComponent },
  { path: 'translator', component: TranslatorComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
