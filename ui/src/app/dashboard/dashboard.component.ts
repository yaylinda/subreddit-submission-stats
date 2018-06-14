import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: [ './dashboard.component.css' ]
})
export class DashboardComponent implements OnInit {

  @ViewChild('meanscores') meanScoresElementRef: ElementRef;
  @ViewChild('meancomments') meanCommentsElementRef: ElementRef;

  baseUrl = 'http://localhost:5000/generate/';
  submitted = false;
  requestFormSubreddit;
  requestFormDays;

  constructor(private http: HttpClient) { }

  ngOnInit() {
    this.plotChart(this.meanScoresElementRef.nativeElement, [], 'N/A');
    this.plotChart(this.meanCommentsElementRef.nativeElement, [], 'N/A');
  }

  onSubmit() {
    console.log(this.requestFormSubreddit)
    console.log(this.requestFormDays)

    this.submitted = true;
    
    this.http.get(this.baseUrl + this.requestFormSubreddit + '/' + this.requestFormDays)
      .subscribe((result) => {
        this.submitted = false;
        if (result['status'] === 'SUCCESS') {
          console.log(result)
          this.plotChart(this.meanScoresElementRef.nativeElement, result['means'], 'Score');
          this.plotChart(this.meanCommentsElementRef.nativeElement, result['comments'], 'Number of Comments');
        } else {
          console.error('ERROR');
        }
      })
  }

  plotChart(element, means, statString) {

    const weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].reverse();
    const hours = Array.from(new Array(24), (val,index) => `${index}`);

    const data = [
      {
        x: hours,
        y: weekdays,
        z: means,
        type: 'heatmap'
      }
    ];

    var layout = {
      title: 'Mean ' + statString + ' of /r/' + this.requestFormSubreddit + ' Submissions in the Past ' + this.requestFormDays + ' Days',
      xaxis: {
        title: 'Hour of Submission',
        ticks: ' ',
        nticks: 24
      },
      yaxis: {
        title: 'Day of the Week',
        ticks: ' ',
      }
    };

    Plotly.plot(element, data, layout)
  }
}
