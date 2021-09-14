import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { NerBscComponent } from './ner-bsc.component';

describe('NerBscComponent', () => {
  let component: NerBscComponent;
  let fixture: ComponentFixture<NerBscComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ NerBscComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NerBscComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
