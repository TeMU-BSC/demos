import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { NeuroNerComponent } from './neuro-ner.component';

describe('NeuroNerComponent', () => {
  let component: NeuroNerComponent;
  let fixture: ComponentFixture<NeuroNerComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ NeuroNerComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NeuroNerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
