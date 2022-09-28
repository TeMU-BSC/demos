import { TestBed } from '@angular/core/testing';

import { PhenotypeViewService } from './phenotype-view.service';

describe('PhenotypeViewService', () => {
  let service: PhenotypeViewService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PhenotypeViewService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
