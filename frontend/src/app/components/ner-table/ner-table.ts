import { SelectionModel } from '@angular/cdk/collections';
import { HttpClient } from '@angular/common/http';
import { Component, ViewChild, AfterViewInit, ViewEncapsulation, ElementRef } from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort, SortDirection } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { merge, Observable, of as observableOf } from 'rxjs';
import { catchError, map, startWith, switchMap } from 'rxjs/operators';
export interface AnnotationSnomed {
  type: string
  code: string
  text: string

}


@Component({
  selector: 'app-ner-table',
  templateUrl: './ner-table.component.html',
  styleUrls: ['./ner-table.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class NerTableComponent implements AfterViewInit {
  displayedColumns: string[] = ['type', 'code', 'text']
  exampleDatabase: ExampleHttpDatabase | null;

  dataSource: MatTableDataSource<AnnotationSnomed>
  selection = new SelectionModel<AnnotationSnomed>(true, [])
  private paginator: MatPaginator
  private sort: MatSort



  @ViewChild(MatPaginator) set matPaginator(mp: MatPaginator) {
    this.paginator = mp
    this.setDataSourceAttributes()
  }
  @ViewChild(MatSort) set matSort(ms: MatSort) {
    this.sort = ms
    this.setDataSourceAttributes()
  }

  setDataSourceAttributes() {
    this.dataSource.paginator = this.paginator
    this.dataSource.sort = this.sort
  }


  textSubmitted: any;

  constructor(private _httpClient: HttpClient,
    private el: ElementRef<HTMLElement>) {

    this.dataSource = new MatTableDataSource([])
  }

  ngAfterViewInit() {
    const lastBtn = this.el.nativeElement.querySelector(
      '.mat-paginator-navigation-previous'
    );
    if (lastBtn) {
      lastBtn.innerHTML = '<span class="material-symbols-outlined">arrow_back_ios</span>';
    }
    const firstBtn = this.el.nativeElement.querySelector(
      '.mat-paginator-navigation-next'
    );
    if (firstBtn) {
      firstBtn.innerHTML = '<span class="material-symbols-outlined">arrow_forward_ios</span>';
    }


    this.exampleDatabase = new ExampleHttpDatabase(this._httpClient);

    // If the user changes the sort order, reset back to the first page.
    this.sort.sortChange.subscribe(() => (this.paginator.pageIndex = 0));

  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value
    this.dataSource.filter = filterValue.trim().toLowerCase()
    if (this.dataSource.paginator) {
      this.dataSource.paginator.firstPage()
    }
  }

  /** Whether the number of selected elements matches the total number of rows. */
  isAllSelected() {
    const numSelected = this.selection.selected.length
    const numRows = this.dataSource.data.length
    return numSelected === numRows
  }

  /** Selects all rows if they are not all selected; otherwise clear selection. */
  masterToggle() {
    if (this.isAllSelected()) {
      this.selection.clear()
      return
    }

    this.selection.select(...this.dataSource.data)
  }

  /** The label for the checkbox on the passed row */
  checkboxLabel(row?: AnnotationSnomed): string {
    if (!row) {
      return `${this.isAllSelected() ? 'deselect' : 'select'} all`
    }
    return `${this.selection.isSelected(row) ? 'deselect' : 'select'} row ${row.text
      }`
  }

}

export interface GithubApi {
  items: GithubIssue[];
  total_count: number;
}

export interface GithubIssue {
  created_at: string;
  number: string;
  state: string;
  title: string;
}

/** An example database that the data source uses to retrieve data for the table. */
export class ExampleHttpDatabase {
  constructor(private _httpClient: HttpClient) { }

  getRepoIssues(sort: string, order: SortDirection, page: number): Observable<GithubApi> {
    const href = 'https://api.github.com/search/issues';
    const requestUrl = `${href}?q=repo:angular/components&sort=${sort}&order=${order}&page=${page + 1
      }`;

    return this._httpClient.get<GithubApi>(requestUrl);
  }
}

