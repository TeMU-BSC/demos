import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BratDisplayComponent } from './brat-display.component';

describe('BratDisplayComponent', () => {
  let component: BratDisplayComponent;
  let fixture: ComponentFixture<BratDisplayComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BratDisplayComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BratDisplayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
