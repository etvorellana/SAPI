import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-topbar-button',
  styleUrls: ['./topbar-button.component.scss'],
  template: `
    <button
      class="topbar-action-btn btn"
    >
      <img
        class="topbar-btn-icon"
        src="assets/image/icon/{{ icon }}.svg"
        alt="{{ icon }} icon"
      />
      <span class="topbar-btn-label">{{ text }}</span>
    </button>
  `
})
export class TopbarButtonComponent implements OnInit {

  @Input() text: string = '';
  @Input() icon: string = '';

  constructor() { }

  ngOnInit(): void {
  }

}
