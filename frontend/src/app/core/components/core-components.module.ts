import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { NgbDropdownModule } from '@ng-bootstrap/ng-bootstrap';
import { StepsDropdownComponent } from './topbar/steps-dropdown/steps-dropdown.component';
import { TopbarComponent } from './topbar/topbar.component';
import { TopbarButtonComponent } from './topbar/topbar-button/topbar-button.component';
import { SpinnerComponent } from './spinner/spinner.component';
import { FilterDropdownComponent } from './topbar/filter-dropdown/filter-dropdown.component';
import { FormsModule } from '@angular/forms';

@NgModule({
  declarations: [
    TopbarComponent,
    StepsDropdownComponent,
    TopbarButtonComponent,
    SpinnerComponent,
    FilterDropdownComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    NgbDropdownModule
  ],
  exports: [
    TopbarComponent,
    SpinnerComponent
  ]
})
export class CoreComponentsModule { }
