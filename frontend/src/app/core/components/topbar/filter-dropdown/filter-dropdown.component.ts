import { Component, OnInit } from '@angular/core';
import { Filters } from 'src/app/core/models/filter';
import { AnalysisService } from 'src/app/core/services/analysis.service';

@Component({
  selector: 'app-filter-dropdown',
  templateUrl: './filter-dropdown.component.html',
  styleUrls: ['./filter-dropdown.component.scss']
})
export class FilterDropdownComponent implements OnInit {

  _filters?: { label: string, value: number }[] = undefined
  selected?: number

  constructor(private service: AnalysisService) { }

  ngOnInit(): void {
    this._filters = Object.entries(Filters)
      .map((entry) => ({ label: entry[1], value: Number(entry[0]) }))

    this.service.getFilter().subscribe((response) => {
      this.selected = response.current_filter;
    })
  }

  changeFilter(filter: number, event: MouseEvent) {
    if (this.selected !== filter) {
      this.selected = filter
      this.service.setFilter(filter).subscribe();
    } else {
      event.preventDefault()
    }
  }

}
