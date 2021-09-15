import { TestBed } from '@angular/core/testing';

import { NerService } from './ner.service';

describe('NerService', () => {
  let service: NerService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(NerService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
