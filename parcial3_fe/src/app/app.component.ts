import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { OauthComponent } from './features/oauth/oauth.component';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, OauthComponent, HttpClientModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'parcial3_fe';
  loggedIn : any;
  token = localStorage.getItem("token");

  ngOnInit(): void {

    if(this.token!=null && this.token!=undefined){
      this.loggedIn = true;
    }
  }
}
