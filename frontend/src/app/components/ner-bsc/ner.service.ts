import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment'

@Injectable({
  providedIn: 'root',
})
export class NerService {

  constructor(private http: HttpClient) {

  }
  getAll(text: any): Observable<any> {
    return this.http.post<any>(`${environment.nerApiUrl}/hello`, text)
  }
  getAnnotations(text: any): Observable<any> {
    return this.http.post<any>(`${environment.nerApiUrl}/get_annotations`, text)
  }
  getMesh(Annotations: any): Observable<any>{
    return this.http.post<any>(`${environment.nerApiUrl}/get_mesh`, Annotations)
  }
}
