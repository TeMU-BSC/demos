import { NgModule } from '@angular/core'
import { Routes, RouterModule } from '@angular/router'

// Projects

import { ProjectsComponent } from './components/projects/projects.component'

const routes: Routes = [
  { path: '', component: ProjectsComponent },
  // { path: 'sentence-splitter', component: SentenceSplitterComponent },
  // { path: 'coming-soon', component: ComingSoonComponent },
  // { path: 'pos', component: PosComponent },
  // { path: 'translator', component: TranslatorComponent },
  // { path: 'neuro-ner/:id', component: NeuroNerComponent },
  // { path: 'doctorNLP', component: SpacyDoctornlpComponent },
  // { path: 'phenotype_visualizer', component: PhenotypeViewComponent },
  // {
  //   path: 'drugprot/:id',
  //   component: DrugprotComponent,
  //   children: [{ path: '', component: FooterComponent }],
  // },
  // { path: 'ner/:id', component: NerBscComponent },
  // { path: 'ner_v2/:id', component: SpacyVisualizerComponent },

  // { path: 'pharmaconer', component: TranslatorComponent },
]

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule { }
