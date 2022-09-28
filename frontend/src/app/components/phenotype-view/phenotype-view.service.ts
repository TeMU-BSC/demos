import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment'


@Injectable({
  providedIn: 'root'
})
export class PhenotypeViewService {

  constructor(private http: HttpClient) { }

  getPhenotypeAnnotations(text: any): Observable<any> {
    return this.http.post<any>(`${environment.spacyServerUrl}/get_phenotype_annotations`, text)
  }
}
