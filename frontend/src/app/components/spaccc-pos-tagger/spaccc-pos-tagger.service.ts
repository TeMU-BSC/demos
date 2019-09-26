import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { TEMU_API_URLS, TemuResponse } from 'src/app/shared/api.shared'
import { Utils } from 'src/app/shared/utils';

// ----------------------------------------------------------------------------

/**
 * Web page of FreeLing manual explaining Spanish tagsets.
 */
export const FREELING_USER_MANUAL_SPANISH_TAGSET_URL = 'https://freeling-user-manual.readthedocs.io/en/latest/tagsets/tagset-es/'
export const TAG_ANCHOR_BASE = '#part-of-speech-'

/**
 * Part of Speech (POS) correlations between the first letter of the tag and
 * its meaning.
 */
export const CATEGORIES = {
  A: 'adjective',
  C: 'conjunction',
  D: 'determiner',
  N: 'noun',
  P: 'pronoun',
  R: 'adverb',
  S: 'adposition',
  V: 'verb',
  Z: 'number',
  W: 'date',
  I: 'interjection',
  F: 'punctuation'
}

// ----------------------------------------------------------------------------

@Injectable({
  providedIn: 'root'
})
export class SpacccPosTaggerService {

  constructor(private http: HttpClient) { }

  /**
   * Get all the sample texts from the API.
   */
  getSampleTexts(): Observable<TemuResponse> {
    const url = `${TEMU_API_URLS.freeling}/samples`;
    const options = Utils.getBasicOptions();
    return this.http.get<any>(url, options);
  }


  /**
   * Get some Part of Speech (POS) Spanish Medical Tags
   * from the API.
   * 
   * @returns the API response as an Observable object 
   */
  getPosTags(body: any): Observable<TemuResponse> {
    const url = `${TEMU_API_URLS.freeling}/analyze`;
    const options = Utils.getBasicOptions();
    return this.http.post<any>(url, body, options);
  }

}
