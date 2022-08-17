import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { AnalysisStep } from '../models/analysis-step.enum';
import { WebSocketService } from './websocket.service';
import { Message } from '../models/message';

type CurrentFilter = { current_filter: number }

@Injectable({
  providedIn: 'root'
})
export class AnalysisService {

  constructor(private http: HttpClient, private webSocket: WebSocketService<Message>) { }

  trigger() {
    return this.http.post(`${environment.baseURL}/button/press`, undefined);
  }

  listen(errorCallback?: (error: any) => void) {
    return this.webSocket.connect('analysis',  errorCallback)
  }

  sendImage(payload: string) {
    return this.http.post<void>(`${environment.baseURL}/analysis/simulation`, 
      { image: payload }
    );
  }

  setSteps(payload: AnalysisStep[]) {
    return this.http.put(`${environment.baseURL}/analysis/steps`, payload);
  }

  clear() {
    return this.http.post(`${environment.baseURL}/analysis/clear`, undefined);
  }

  setFilter(filter: number) {
    return this.http.post(`${environment.baseURL}/filter`, { filter });
  }

  getFilter() {
    return this.http.get<CurrentFilter>(`${environment.baseURL}/filter`);
  }
}
