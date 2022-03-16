import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subject, takeUntil } from 'rxjs';
import { Message, SoldersClassification } from 'src/app/core/models/message';
import { AnalysisService } from 'src/app/core/services/analysis.service';
import { environment } from 'src/environments/environment';

type AnalysisResult = { label: string, key: keyof SoldersClassification, value?: number, color: string };

@Component({
  selector: 'app-analysis',
  templateUrl: './analysis.component.html',
  styleUrls: ['./analysis.component.scss']
})
export class AnalysisComponent implements OnInit, OnDestroy {

  destroyed$ = new Subject<void>();

  cameraFeed: string = ''
  lastMessage?: Message

  results: AnalysisResult[] = [
    {
      label: 'Ponte',
      key: 'Ponte',
      value: undefined,
      color: 'crimson'
    },
    {
      label: 'Sem solda',
      key: 'Ausente',
      value: undefined,
      color: 'violet'
    },
    {
      label: 'Pouca solda',
      key: 'Pouca',
      value: undefined,
      color: 'blue'
    },
    {
      label: 'Em excesso',
      key: 'Excesso',
      value: undefined,
      color: 'yellow'
    },
    {
      label: 'Boa',
      key: 'Boa',
      value: undefined,
      color: 'green'
    }
  ]

  constructor(private analysisService: AnalysisService) { }

  ngOnInit(): void {
    this.cameraFeed = `${environment.baseURL}/camera/feed`
    this.analysisService.listen((err) => { console.log('trying again') })
      .pipe(takeUntil(this.destroyed$)).subscribe((message) => {
        this.handleReceivedMessage(message)
      });
  }

  handleReceivedMessage(message: Message) {
    this.lastMessage = message
    // States
    switch (message.state) {
      case 1:
        // start of process
        break
      case 2:
        // watching camera
        break
      case 3:
        // processing image start
        break
      case 4:
      // processing image finished
      case 5:
        // showing image and waiting for restart
        this.updateClassification(message.solders_classification.classificacao)
        break
      default:
        throw new Error('Unknown state')
    }
  }

  ngOnDestroy() {
    this.destroyed$.next();
  }

  updateClassification(classification: SoldersClassification) {
    this.results.forEach(result => {
      result.value = classification[result.key]
    })
  }
}
