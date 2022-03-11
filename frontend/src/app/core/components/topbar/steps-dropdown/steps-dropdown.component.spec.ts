import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StepsDropdownComponent } from './steps-dropdown.component';

describe('StepsDropdownComponent', () => {
  let component: StepsDropdownComponent;
  let fixture: ComponentFixture<StepsDropdownComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ StepsDropdownComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(StepsDropdownComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
