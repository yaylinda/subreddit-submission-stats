import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: [ './dashboard.component.css' ]
})
export class DashboardComponent implements OnInit {

  @ViewChild('meanscores') meanScoresElementRef: ElementRef;
  @ViewChild('meancomments') meanCommentsElementRef: ElementRef;

  baseUrl = 'http://' + environment.serverUrl + ':5000/generate/';

  submitted = false;
  submitAvailable = true;
  buttonText = 'Submit';

  requestFormSubreddit;
  requestFormDays;

  constructor(private http: HttpClient) {}

  ngOnInit() {
    // this.plotChart(this.meanScoresElementRef.nativeElement, [], '<SUBREDDIT>', '<DAYS>', 'Score');
    // this.plotChart(this.meanCommentsElementRef.nativeElement, [], '<SUBREDDIT>', '<DAYS>', 'Comments');
  }

  onSubmit() {
    console.log(this.requestFormSubreddit)
    console.log(this.requestFormDays)

    this.submitted = true;
    this.submitAvailable = false;
    this.buttonText = 'Processing...';
    
    this.http.get(this.baseUrl + this.requestFormSubreddit + '/' + this.requestFormDays)
      .subscribe((result) => {

        this.submitted = false;
        this.submitAvailable = true;
        this.buttonText = 'Submit';

        console.log(result)

        let scores_data = [];
        let comments_data = [];
        if (result['status'] === 'SUCCESS') {
          scores_data = result['scores'];
          comments_data = result['comments']
        }

        this.plotChart(this.meanScoresElementRef.nativeElement, scores_data, result['subreddit'], result['days'], 'Score');
        this.plotChart(this.meanCommentsElementRef.nativeElement, comments_data, result['subreddit'], result['days'], 'Comments');

      })
  }

  plotChart(element, means, subreddit, days, statString) {

    const weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].reverse();
    const hours = Array.from(new Array(24), (val,index) => `${index}`);

    const data = [
      {
        x: hours,
        y: weekdays,
        z: means,
        type: 'heatmap',
        colorscale: 'Viridis'
      }
    ];

    var layout = {
      title: 'Mean ' + statString + ' of /r/' + subreddit + ' Submissions in the Past ' + days + ' Days',
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

    Plotly.newPlot(element, data, layout)
  }
}
