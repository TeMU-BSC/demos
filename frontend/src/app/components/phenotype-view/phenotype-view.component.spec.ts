import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PhenotypeViewComponent } from './phenotype-view.component';

describe('PhenotypeViewComponent', () => {
  let component: PhenotypeViewComponent;
  let fixture: ComponentFixture<PhenotypeViewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PhenotypeViewComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PhenotypeViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
