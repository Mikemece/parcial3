import { Component, OnInit } from '@angular/core';
import { OauthComponent } from '../oauth/oauth.component';
import { Router } from '@angular/router';
import { PruebaService } from '../../services/prueba-serv/prueba.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Timestamp } from 'rxjs';

interface Evento{
    nombre : string;
    timestamp : Date;
    lugar : string;
    lat :   number;
    long :   number;
    organizador :   string;
    imagen : string;
}

@Component({
  selector: 'app-inicio',
  standalone: true,
  imports: [OauthComponent, CommonModule, FormsModule],
  templateUrl: './inicio.component.html',
  styleUrl: './inicio.component.css',
  providers: [PruebaService]
})
export class InicioComponent implements OnInit{
  token = localStorage.getItem("token");

  constructor(private router: Router, private pruebaService: PruebaService){}

  texto : string = '';
  postal : string = '';
  eventos : any[] = [];
  eventosC : any[] = [];
  evento : any ;
  
  ngOnInit(): void {
    // console.log("token: ", this.token);
    // if (this.token == undefined || this.token == null) {
    //   this.router.navigate(['/login']);
    // }
    this.pruebaService.getAll().subscribe((data)=>{
      this.eventos = data;
    })
  }

  busca(busqueda: { b: string }){
    if (busqueda.b === '') {
      this.texto = "Ningún evento encontrado";
    } else{
      this.postal= busqueda.b;
      this.pruebaService.getPostal(this.postal).subscribe((data) =>{
      this.evento = data;
      console.log(this.evento);
      if (this.evento!==null){
        for (let i = 0; i < this.eventos.length; i++) {
          let dist = this.eventos[i].lat - this.evento.lat;
          let dist2 = this.eventos[i].long - this.evento.long;
          if((dist < 0.2) && (dist> -0.2) && (dist2 < 0.2) && (dist2> -0.2)){
            this.eventosC.push(this.eventos[i]);
          }
        } 
      }
    });    
    }
  }

redEvento(id: any){
  this.router.navigate(['/evento', id])
}
}