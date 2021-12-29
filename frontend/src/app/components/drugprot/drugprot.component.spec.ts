import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DrugprotComponent } from './drugprot.component';

describe('DrugprotComponent', () => {
  let component: DrugprotComponent;
  let fixture: ComponentFixture<DrugprotComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DrugprotComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DrugprotComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
