import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment'

@Injectable({
  providedIn: 'root'
})
export class ProjectsService {

  constructor(private http: HttpClient) {

  }
  getModelsInfo(): Observable<any> {
    return this.http.get<any>(`${environment.spacyServerUrl}/get_model_info`)
  }
  getAnnotations(text: any): Observable<any> {
    return this.http.post<any>(`${environment.drugProtApiUrl}/get_annotations`, text)
  }
  getMesh(Annotations: any): Observable<any> {
    return this.http.post<any>(`${environment.drugProtApiUrl}/get_mesh`, Annotations)
  }

  getSnomedTemrs(code: any): Observable<any> {
    return this.http.get<any>(`https://browser.ihtsdotools.org/snowstorm/snomed-ct/browser/MAIN/SNOMEDCT-ES/2021-10-31/concepts/${code}?descendantCountForm=stated`)
  }
}
