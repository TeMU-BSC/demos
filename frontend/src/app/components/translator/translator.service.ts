import { Injectable } from '@angular/core'
import { HttpClient } from '@angular/common/http'
import { Observable } from 'rxjs'
import { TEMU_API_URLS, TemuResponse } from 'src/app/shared/api.shared'
import { Translation } from 'src/app/components/translator/translator.model'
import { Utils } from 'src/app/shared/utils';


@Injectable({
  providedIn: 'root'
})
export class TranslatorService {
  constructor(private http: HttpClient) { }

  /**
   * Get all the sample texts from the API.
   */
  getSamples(): Observable<TemuResponse> {
    const url = `${TEMU_API_URLS.translator}/samples`;
    const options = Utils.getBasicOptions();
    return this.http.get<TemuResponse>(url, options);
  }

  /**
   * Call the translator API to get the response with the translated
   * sentences, prediction scores and translation time.
   * 
   */
  translate(body: Translation): Observable<TemuResponse> {
    const url = `${TEMU_API_URLS.translator}/translate`;
    const options = Utils.getBasicOptions();
    return this.http.post<TemuResponse>(url, body, options);
  }
}
