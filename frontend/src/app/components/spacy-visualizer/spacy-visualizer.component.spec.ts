import { async, ComponentFixture, TestBed } from '@angular/core/testing'

import SpacyVisualizerComponent from './spacy-visualizer.component'

describe('SpacyVisualizerComponent', () => {
  let component: SpacyVisualizerComponent
  let fixture: ComponentFixture<SpacyVisualizerComponent>

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [SpacyVisualizerComponent],
    }).compileComponents()
  }))

  beforeEach(() => {
    fixture = TestBed.createComponent(SpacyVisualizerComponent)
    component = fixture.componentInstance
    fixture.detectChanges()
  })

  it('should create', () => {
    expect(component).toBeTruthy()
  })
})
