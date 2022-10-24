import { HttpClient } from '@angular/common/http';
import { Component, ViewChild, AfterViewInit, ViewEncapsulation, ElementRef } from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort, SortDirection } from '@angular/material/sort';
import { merge, Observable, of as observableOf } from 'rxjs';
import { catchError, map, startWith, switchMap } from 'rxjs/operators';
export interface AnnotationSnomed {
  type: string
  code: string
  text: string

}


@Component({
  selector: 'app-neuro-ner',
  templateUrl: './neuro-ner.component.html',
  styleUrls: ['./neuro-ner.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class NeuroNerComponent implements AfterViewInit {
  displayedColumns: string[] = ['created', 'state', 'number', 'title'];
  exampleDatabase: ExampleHttpDatabase | null;
  data: GithubIssue[] = [];

  resultsLength = 0;
  isLoadingResults = true;
  isRateLimitReached = false;

  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;

  constructor(private _httpClient: HttpClient,
    private el: ElementRef<HTMLElement>) { }

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

    merge(this.sort.sortChange, this.paginator.page)
      .pipe(
        startWith({}),
        switchMap(() => {
          this.isLoadingResults = true;
          return this.exampleDatabase!.getRepoIssues(
            this.sort.active,
            this.sort.direction,
            this.paginator.pageIndex,
          ).pipe(catchError(() => observableOf(null)));
        }),
        map(data => {
          // Flip flag to show that loading has finished.
          this.isLoadingResults = false;
          this.isRateLimitReached = data === null;

          if (data === null) {
            return [];
          }

          // Only refresh the result length if there is new data. In case of rate
          // limit errors, we do not want to reset the paginator to zero, as that
          // would prevent users from re-triggering requests.
          this.resultsLength = data.total_count;
          return data.items;
        }),
      )
      .subscribe(data => (this.data = data));
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

