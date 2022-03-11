import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subject, takeUntil } from 'rxjs';
import { Message } from 'src/app/core/models/message';
import { AnalysisService } from 'src/app/core/services/analysis.service';
import { environment } from 'src/environments/environment';

type AnalysisResult = { label: string, key: string, value: number, color: string };

@Component({
  selector: 'app-analysis',
  templateUrl: './analysis.component.html',
  styleUrls: ['./analysis.component.scss']
})
export class AnalysisComponent implements OnInit, OnDestroy{
  
  destroyed$ = new Subject<void>();
  
  cameraFeed: string = ''
  lastMessage?: Message
  
  results: AnalysisResult[] = [
    {
      label: 'Ponte',
      key: 'bridge',
      value: 1,
      color: 'danger'
    },
    {
      label: 'Sem solda',
      key: 'missing',
      value: 0,
      color: 'danger'
    },
    {
      label: 'Pouca solda',
      key: 'too-little',
      value: 1,
      color: 'warning'
    },
    {
      label: 'Em excesso',
      key: 'too-much',
      value: 1,
      color: 'warning'
    },
    {
      label: 'Boa',
      key: 'good',
      value: 1,
      color: 'success'
    }
  ]

  // States
  // 1 - start of process
  // 2 - watching camera
  // 3 - processing image start
  // 4 - processing image finished
  // 5 - showing image and waiting for restart

  constructor(private analysisService: AnalysisService) { }

  ngOnInit(): void {
    this.cameraFeed = `${environment.baseURL}/camera/feed`
    this.analysisService.listen((err) => { console.log('trying again') })
    .pipe(takeUntil(this.destroyed$)).subscribe((message) => {
      this.lastMessage = message
    });
  }

  ngOnDestroy() {
    this.destroyed$.next();
  }

}
