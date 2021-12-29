import { TestBed } from '@angular/core/testing';

import { DrugprotService } from './drugprot.service';

describe('DrugprotService', () => {
  let service: DrugprotService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(DrugprotService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
