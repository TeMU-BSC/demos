import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ProjectsService {

  constructor(private http: HttpClient) {

  }

  getSnomedTemrs(code: any): Observable<any> {
    return this.http.get<any>(`https://browser.ihtsdotools.org/snowstorm/snomed-ct/browser/MAIN/SNOMEDCT-ES/2021-10-31/concepts/${code}?descendantCountForm=stated`)
  }
}
