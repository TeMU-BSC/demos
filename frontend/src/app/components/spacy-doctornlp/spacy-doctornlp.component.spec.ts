import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SpacyDoctornlpComponent } from './spacy-doctornlp.component';

describe('SpacyDoctornlpComponent', () => {
  let component: SpacyDoctornlpComponent;
  let fixture: ComponentFixture<SpacyDoctornlpComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SpacyDoctornlpComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SpacyDoctornlpComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
