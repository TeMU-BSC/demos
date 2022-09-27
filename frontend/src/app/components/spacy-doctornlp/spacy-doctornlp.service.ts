import { HttpClient } from '@angular/common/http'
import { Injectable } from '@angular/core'
import { Observable } from 'rxjs'
import { environment } from 'src/environments/environment'

@Injectable({
  providedIn: 'root'
})
export class SpacyDoctornlpService {

  constructor(private http: HttpClient) { }
  getModelsInfo(): Observable<any> {
    return this.http.get<any>(`${environment.spacyServerUrl}/get_model_info`)
  }
  getSpacyAllNERsAnnotations(data): Observable<any> {
    return this.http.post<any>(
      `${environment.spacyServerUrl}/get_all_ner_annotations`,
      data
    )
  }
}
