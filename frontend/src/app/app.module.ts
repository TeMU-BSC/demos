import { BrowserModule } from '@angular/platform-browser'
import { NgModule } from '@angular/core'
import { AppRoutingModule } from './app-routing.module'
import { AppComponent } from './app.component'
import { FormsModule } from '@angular/forms'
import { ReactiveFormsModule } from '@angular/forms'
import { HttpClientModule } from '@angular/common/http'

// https://material.angular.io/guide/getting-started
import { BrowserAnimationsModule } from '@angular/platform-browser/animations'
import { MaterialModule } from './material.module'

// https://github.com/angular/flex-layout
import { FlexLayoutModule } from '@angular/flex-layout'

// https://www.npmjs.com/package/simplemattable
import { SimplemattableModule } from 'simplemattable'

// https://www.freakyjolly.com/angular-8-7-show-global-progress-bar-loader-on-http-calls-in-3-steps-using-angular-interceptors-in-angular-4-3/
import { LoaderService } from './components/loader/loader.service'
import { HTTP_INTERCEPTORS } from '@angular/common/http'
import { LoaderInterceptor } from './loader.interceptor'

// Own components
import { PosComponent } from './components/pos/pos.component'
import { ComingSoonComponent } from './components/coming-soon/coming-soon.component'
import { FooterComponent } from './components/footer/footer.component'
import { TranslatorComponent } from './components/translator/translator.component'
import { HeaderComponent } from './components/header/header.component'
import { LoaderComponent } from './components/loader/loader.component'
import { ProjectsComponent } from './components/projects/projects.component'

@NgModule({
  declarations: [
    AppComponent,
    PosComponent,
    ComingSoonComponent,
    FooterComponent,
    TranslatorComponent,
    HeaderComponent,
    LoaderComponent,
    ProjectsComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    BrowserAnimationsModule,
    HttpClientModule,
    MaterialModule,
    FlexLayoutModule,
    SimplemattableModule,
  ],
  providers: [
    LoaderService,
    { provide: HTTP_INTERCEPTORS, useClass: LoaderInterceptor, multi: true },
  ],
  bootstrap: [AppComponent],
})
export class AppModule { }
