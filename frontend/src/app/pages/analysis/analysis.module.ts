import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { CoreComponentsModule } from 'src/app/core/components/core-components.module';
import { AnalysisRoutingModule } from './analysis-routing.module';
import { AnalysisComponent } from './analysis.component';

@NgModule({
  declarations: [
    AnalysisComponent
  ],
  imports: [
    CommonModule,
    AnalysisRoutingModule,
    CoreComponentsModule
  ],
  exports: [
  ]
})
export class AnalysisModule { }
