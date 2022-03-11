import { Component, OnInit } from '@angular/core';
import { AnalysisStep } from 'src/app/core/models/analysis-step.enum';
import { LabelValue } from 'src/app/core/models/label-value';

@Component({
  selector: 'app-steps-dropdown',
  templateUrl: './steps-dropdown.component.html',
  styleUrls: ['./steps-dropdown.component.scss']
})
export class StepsDropdownComponent implements OnInit {

  _steps?: LabelValue[] = undefined

  constructor() { }

  ngOnInit(): void {
    this._steps = Object.entries(AnalysisStep)
      .map((entry) => ({ label: entry[1] as string, value: entry[0] }))
  }

}
