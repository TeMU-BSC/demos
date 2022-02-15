import { NgModule } from '@angular/core'
import { Routes, RouterModule } from '@angular/router'

// Projects
import { ComingSoonComponent } from './components/coming-soon/coming-soon.component'
import { PosComponent } from './components/pos/pos.component'
import { TranslatorComponent } from './components/translator/translator.component'
import { ProjectsComponent } from './components/projects/projects.component'
import { NerBscComponent } from './components/ner-bsc/ner-bsc.component'
import { DrugprotComponent } from './components/drugprot/drugprot.component'
import { NeuroNerComponent } from './components/neuro-ner/neuro-ner.component'
const routes: Routes = [
  { path: '', component: ProjectsComponent },
  { path: 'sentence-splitter', component: ComingSoonComponent },
  { path: 'coming-soon', component: ComingSoonComponent },
  { path: 'pos', component: PosComponent },
  { path: 'translator', component: TranslatorComponent },
  { path: 'neuro-ner/:id', component: NeuroNerComponent },
  { path: 'drugprot/:id', component: DrugprotComponent },
  { path: 'ner/:id', component: NerBscComponent },

  // { path: 'pharmaconer', component: TranslatorComponent },
]

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule { }
