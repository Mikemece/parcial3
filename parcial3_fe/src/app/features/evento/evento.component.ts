import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Component } from '@angular/core';
import { PruebaService } from '../../services/prueba-serv/prueba.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-evento',
  standalone: true,
  imports: [CommonModule, HttpClientModule],
  templateUrl: './evento.component.html',
  styleUrl: './evento.component.css',
  providers: [PruebaService]
})

export class EventoComponent {

  idEvento ='';
  evento : any;

  constructor(private http: HttpClient, private route: ActivatedRoute, private pruebaService: PruebaService){}
  ngOnInit(){
    this.route.params.subscribe(params => {
      this.idEvento = params['id'];
    });

    this.pruebaService.getInfo(this.idEvento).subscribe(data =>{
      this.evento = data;
    })



  }



}
