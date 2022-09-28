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
import { SentenceSplitterComponent } from './components/sentence-splitter/sentence-splitter.component'
import { FooterComponent } from './components/footer/footer.component'
import { SpacyDoctornlpComponent } from './components/spacy-doctornlp/spacy-doctornlp.component'
import SpacyVisualizerComponent from './components/spacy-visualizer/spacy-visualizer.component'
import { PhenotypeViewComponent } from './components/phenotype-view/phenotype-view.component'
const routes: Routes = [
  { path: '', component: ProjectsComponent },
  { path: 'sentence-splitter', component: SentenceSplitterComponent },
  { path: 'coming-soon', component: ComingSoonComponent },
  { path: 'pos', component: PosComponent },
  { path: 'translator', component: TranslatorComponent },
  { path: 'neuro-ner/:id', component: NeuroNerComponent },
  { path: 'doctorNLP', component: SpacyDoctornlpComponent },
  { path: 'phenotype_visualizer', component: PhenotypeViewComponent },
  {
    path: 'drugprot/:id',
    component: DrugprotComponent,
    children: [{ path: '', component: FooterComponent }],
  },
  { path: 'ner/:id', component: NerBscComponent },
  { path: 'ner_v2/:id', component: SpacyVisualizerComponent },

  // { path: 'pharmaconer', component: TranslatorComponent },
]

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule { }
