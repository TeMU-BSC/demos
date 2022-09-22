import { TestBed } from '@angular/core/testing';

import { SpacyVisualizerService } from './spacy-visualizer.service';

describe('SpacyVisualizerService', () => {
  let service: SpacyVisualizerService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SpacyVisualizerService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
