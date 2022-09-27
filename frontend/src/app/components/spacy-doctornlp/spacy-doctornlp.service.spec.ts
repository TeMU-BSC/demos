import { TestBed } from '@angular/core/testing';

import { SpacyDoctornlpService } from './spacy-doctornlp.service';

describe('SpacyDoctornlpService', () => {
  let service: SpacyDoctornlpService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SpacyDoctornlpService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
