import { Injectable, OnDestroy } from "@angular/core";
import { delay, filter, map, of, retryWhen, switchMap, tap } from "rxjs";
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import { environment } from "src/environments/environment";

@Injectable({
  providedIn: 'root'
})
export class WebSocketService<Message> implements OnDestroy {

  connection$: WebSocketSubject<Message> | null = null;
  RETRY_SECONDS = 3;

  constructor() { }

  ngOnDestroy() {
    this.closeConnection();
  }

  connect(endpoint: string = '', onError?: (error: any) => void) {
    return of(environment.baseURL).pipe(
      filter(apiUrl => !!apiUrl),
      // https becomes wws, http becomes ws
      map(apiUrl => `${apiUrl.replace(/^http/, 'ws')}/${environment.production ? endpoint : 'ws/' + endpoint}`),
      switchMap(wsUrl => {
        if (this.connection$) {
          return this.connection$;
        } else {
          this.connection$ = webSocket<Message>(wsUrl);
          return this.connection$;
        }
      }),
      retryWhen((errors) => errors.pipe(
        tap(error => onError ? onError(error) : undefined),
        delay(this.RETRY_SECONDS * 1000)
      ))
    );
  }

  closeConnection() {
    if (this.connection$) {
      this.connection$.complete();
      this.connection$ = null;
    }
  }

  send(data: any) {
    if (this.connection$) {
      this.connection$.next(data);
    } else {
      console.error('Did not send data, open a connection first');
    }
  }
}