import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { NerTableComponent } from './ner-table';

describe('NerTableComponent', () => {
  let component: NerTableComponent;
  let fixture: ComponentFixture<NerTableComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [NerTableComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NerTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
