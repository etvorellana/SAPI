import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  {
    path: 'analysis',
    loadChildren: () => import('./pages/analysis/analysis.module').then(m => m.AnalysisModule),
  },
  {
    path: '**',
    redirectTo: 'analysis',
    pathMatch: 'full'
  }
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes)
  ],
  exports: [
    RouterModule
  ]
})
export class AppRoutingModule { }
