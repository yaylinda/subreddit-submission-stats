import { Component, OnInit, ViewChild, ElementRef, Renderer } from '@angular/core';
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

  buttonText = 'Submit';
  submitAvailable = true;

  requestFormSubreddit;
  requestFormDays;

  constructor(private http: HttpClient, private _renderer: Renderer) {}

  ngOnInit() {
    // this.plotChart(this.meanScoresElementRef.nativeElement, [], '<SUBREDDIT>', '<DAYS>', 'Score');
    // this.plotChart(this.meanCommentsElementRef.nativeElement, [], '<SUBREDDIT>', '<DAYS>', 'Comments');
  }

  onSubmit() {
    console.log(this.requestFormSubreddit)
    console.log(this.requestFormDays)

    this.buttonText = 'Processing...';
    this.submitAvailable = false;

    let loader = '<div class="loader" style="border:16px solid #f3f3f3; border-top:16px solid #3498db; border-radius: 50%; width:60px; height:60px; animation: spin 4s linear infinite; margin: auto auto;"></div>';
    this._renderer.setElementProperty(this.meanScoresElementRef.nativeElement, 'innerHTML', loader);
    this._renderer.setElementProperty(this.meanCommentsElementRef.nativeElement, 'innerHTML', loader);

    const requestFormSubredditCleaned = this.requestFormSubreddit.replace('/r/', '').replace('r/', '').replace('/', '')
    this.http.get(this.baseUrl + requestFormSubredditCleaned + '/' + this.requestFormDays)
      .subscribe((result) => {

        this.buttonText = 'Submit';
        this.submitAvailable = true;

        this._renderer.setElementProperty(this.meanScoresElementRef.nativeElement, 'innerHTML', '');
        this._renderer.setElementProperty(this.meanCommentsElementRef.nativeElement, 'innerHTML', '');

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
