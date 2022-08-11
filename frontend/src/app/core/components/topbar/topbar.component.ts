import {
  animate, state,
  style, transition, trigger
} from '@angular/animations';
import { Component, OnInit } from '@angular/core';
import { environment } from 'src/environments/environment';
import { AnalysisService } from '../../services/analysis.service';
import { UploadService } from '../../services/upload.service';

type TopbarButton = { text: string, icon: string, action: () => void, advancedOnly?: boolean };
type TopbarDropdownButton = {
  id: string,
  text: string,
  type: string,
  advancedOnly?: boolean
};

@Component({
  selector: 'app-topbar',
  templateUrl: './topbar.component.html',
  styleUrls: ['./topbar.component.scss'],
  animations: [
    trigger('toggleAdvanced', [
      state('compact', style({ height: '40px', minHeight: '40px' })),
      state('advanced', style({ height: '70px', minHeight: '70px' })),
      transition('compact <=> advanced', animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')),
    ]),
  ]
})
export class TopbarComponent implements OnInit {

  _advancedMode = true

  buttons: TopbarButton[] = [
    {
      text: 'Modo avançado',
      icon: 'toggle',
      action: () => this.toggleMode(),
      advancedOnly: environment.production
    },
    {
      text: 'Capturar/Limpar',
      icon: 'camera',
      action: () => this.triggerAnalysis(),
      advancedOnly: true
    },
    {
      text: 'Enviar',
      icon: 'upload',
      action: () => this.sendImage(),
      advancedOnly: true
    }
  ]

  buttonsDropdown: TopbarDropdownButton[] = [
    {
      id: 'steps-dropdown',
      text: 'Etapas',
      type: 'steps',
      advancedOnly: true
    },
    {
      id: 'filter-dropdown',
      text: 'Filtro',
      type: 'filter',
      advancedOnly: true
    }
  ]

  constructor(private analysisService: AnalysisService,
    private uploadService: UploadService
  ) { }

  ngOnInit(): void {
    if (environment.production) {
      this._advancedMode = false
    }
  }

  isProductionMode() {
    return environment.production
  }

  toggleMode() {
    this._advancedMode = !this._advancedMode
  }

  triggerAnalysis() {
    this.analysisService.trigger().subscribe()
  }

  sendImage() {
    this.uploadService.upload('.png').then(res => {
      if (res) {
        this.analysisService.sendImage(res[0]).subscribe({
          error: () => {
            alert('Erro ao enviar imagem')
          }
        })
      }
    })
  }
}
