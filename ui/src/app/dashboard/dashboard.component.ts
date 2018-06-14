import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import * as _ from 'lodash'

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: [ './dashboard.component.css' ]
})
export class DashboardComponent implements OnInit {

  @ViewChild('meanchart') meanElementRef: ElementRef;

  baseUrl = 'http://localhost:5000/generate/';
  submitted = false;
  showPlots = false;
  requestFormSubreddit;
  requestFormDays;
  requestFormStat;

  constructor(private http: HttpClient) { }

  ngOnInit() {
    this.plotChart([]);
  }

  onSubmit() {
    console.log(this.requestFormSubreddit)
    console.log(this.requestFormDays)
    console.log(this.requestFormStat);

    this.submitted = true;
    this.showPlots = false;
    this.meanElementRef.nativeElement.remove()
    
    this.http.get(this.baseUrl + this.requestFormSubreddit + '/' + this.requestFormDays + '/' + this.requestFormStat)
      .subscribe((result) => {
        this.submitted = false;
        this.showPlots = true;
        if (result['status'] === 'SUCCESS') {
          console.log(result)
          console.log(result['means'])
          this.plotChart(result['means']);
        } else {
          console.error('ERROR');
        }
      })
  }

  plotChart(means) {

    if (this.showPlots) {

      const weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].reverse();
      const hours = Array.from(new Array(24), (val,index) => `${index}`);

      const mean_element = this.meanElementRef.nativeElement;

      const mean_data = [
        {
          x: hours,
          y: weekdays,
          z: means,
          type: 'heatmap'
        }
      ];

      var mean_layout = {
        title: 'Mean ' + this.requestFormStat + ' of /r/' + this.requestFormSubreddit + ' in the past ' + this.requestFormDays + ' days',
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

      Plotly.plot(mean_element, mean_data, mean_layout)
    }
  }
}
