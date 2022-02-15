import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SentenceSplitterComponent } from './sentence-splitter.component';

describe('SentenceSplitterComponent', () => {
  let component: SentenceSplitterComponent;
  let fixture: ComponentFixture<SentenceSplitterComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SentenceSplitterComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SentenceSplitterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
