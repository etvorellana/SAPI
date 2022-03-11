import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { NgbDropdownModule } from '@ng-bootstrap/ng-bootstrap';
import { StepsDropdownComponent } from './topbar/steps-dropdown/steps-dropdown.component';
import { TopbarComponent } from './topbar/topbar.component';
import { TopbarButtonComponent } from './topbar/topbar-button/topbar-button.component';
import { SpinnerComponent } from './spinner/spinner.component';

@NgModule({
  declarations: [
    TopbarComponent,
    StepsDropdownComponent,
    TopbarButtonComponent,
    SpinnerComponent
  ],
  imports: [
    CommonModule,
    NgbDropdownModule
  ],
  exports: [
    TopbarComponent,
    SpinnerComponent
  ]
})
export class CoreComponentsModule { }
