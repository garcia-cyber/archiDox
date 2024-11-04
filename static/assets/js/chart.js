$(document).ready(function() {

	// Bar Chart
	if($('#bar-charts').length > 0) {
		var options = {
			series: [{
				name: 'Project In',
				data: [76, 85, 101, 98, 87]
			}, {
				name: ' Project Taken',
				data: [35, 41, 36, 26, 45]
			}],
				chart: {
				type: 'bar',
				height: 300,
				toolbar: false
			},
			colors: ['#E24F55', '#5F3B7E'],
			plotOptions: {
				bar: {
				horizontal: false,
				columnWidth: '55%',
				},
			},
			dataLabels: {
				enabled: false
			},
			stroke: {
				show: true,
				width: 3,
				colors: ['transparent']
			},
			xaxis: {
				categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
			},
			fill: {
				opacity: 1,
			},
			grid: {
				yaxis: {
					lines: {
					  show: false
					}
				  }
			},
			tooltip: {
				y: {
				formatter: function (val) {
					return "$ " + val + " thousands"
				}
				}
			}
		};
	
		var chart = new ApexCharts(document.querySelector("#bar-charts"), options);
		chart.render();
	}
	
	
	// Evaluation Chart
	
	if($('#evaluation-charts').length > 0) {
		var options = {
			series: [42, 47, 85, 35],
			chart: {
				height: 340,
				type: 'polarArea',				
			},
			labels: ['Design', 'iOS', 'HR', 'DevOps'],
			colors: ['#AA60BB', '#E64B51', '#6B468C', '#734FFE'],
			fill: {
				type: 'normal',
				opacity: 1,
				colors: ['#AA60BB', '#E64B51', '#6B468C', '#734FFE']	
			},
			stroke: {
				width: 0,
				colors: undefined
			},
			yaxis: {
				show: false
			},
			legend: {
				position: 'bottom'
			},
			plotOptions: {
				polarArea: {
				rings: {
					strokeWidth: 0
				},
				spokes: {
					strokeWidth: 0,
				},
				}
			}
		};
	
		var chart = new ApexCharts(document.querySelector("#evaluation-charts"), options);
		chart.render();
	}
	

	// Employee Chart

	if($('#employee-chart').length > 0) {
		var options = {
			series: [85, 44],
			colors : ['#5f3b7e', '#ff943a'],
			chart: {
				type: 'donut',
			},
			fill: {
				type: 'normal'
			},
			legend: {
				formatter: function(val, opts) {
					return val + " - " + opts.w.globals.series[opts.seriesIndex]
				},
				position: 'bottom'
			},
			plotOptions: {
				labels: {
					show: false
				}
			},
			dataLabels: {
				enabled: false
			},
			title: {
				show: true,
			},
			donut: {
				labels: {
					show: false,
					name: {
						show: true,
					}
				}
			},
			
		};

		var chart = new ApexCharts(document.querySelector("#employee-chart"), options);
		chart.render();
	}
		
});