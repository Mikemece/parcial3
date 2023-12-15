import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PruebaService {

  constructor(private http:HttpClient) { }

  getAll() : Observable<any> {
    //const url = 'http://localhost:8000/api/eventos/';
    const url = 'http://13.36.188.166:8000/api/eventos/';
    return this.http.get<any>(url);
  }
  getPostal(postal: string) : Observable<any> {
    //const url = 'http://localhost:8000/api/eventoPostal/'+postal+'/';
    const url = 'http://13.36.188.166:8000/api/eventoPostal/'+postal+'/';;
    return this.http.get<any>(url);
  }
  getInfo(id: string) : Observable<any> {
    //const url = 'http://localhost:8000/api/eventos/'+id+'/';
    const url = 'http://13.36.188.166:8000/api/eventos/'+id+'/';
    return this.http.get<any>(url);
  }

}
