window.onload = function() {

var dataWork = [];
var dataFamily = [];
var dataHobby = [];
var dataSleep = [];

var workchart = new CanvasJS.Chart("workchart", {
	animationEnabled: true,
	backgroundColor: "#8DD",
	legendEnabled: false,
	theme: "light2",
	axisY: {
		title: "Units",
		titleFontSize: 24,
		fontFamily: "Roboto"
	},
	data: [{
		type:"line",
		axisYType: "secondary",
		name: "work",
		color: "MediumAquamarine",
		showInLegend: false,
		markerSize: 5,
		yValueFormatString: "",
		dataPoints: dataWork
	}]
});

var familychart = new CanvasJS.Chart("familychart", {
	animationEnabled: true,
	backgroundColor: "#8DD",
	theme: "light2",
	axisY: {
		title: "Units",
		titleFontSize: 24,
		fontFamily: "Roboto"
	},
	data: [{
		type:"line",
		color:"DarkSeaGreen",
		axisYType: "secondary",
		name: "family",
		showInLegend: false,
		markerSize: 5,
		yValueFormatString: "",
		dataPoints: dataFamily
	}]
});

var hobbychart = new CanvasJS.Chart("hobbychart", {
	animationEnabled: false,
	backgroundColor: "#8DD",
	theme: "light2",
	axisY: {
		title: "Units",
		titleFontSize: 24,
		fontFamily: "Roboto"
	},
	data: [{
		type:"line",
		color:"LightSeaGreen",
		axisYType: "secondary",
		name: "hobby",
		showInLegend: false,
		markerSize: 5,
		yValueFormatString: "",
		dataPoints: dataHobby
	}]
});

var sleepchart = new CanvasJS.Chart("sleepchart", {
	animationEnabled: false,
	theme: "light2",
	backgroundColor: "#8DD",
	axisY: {
		title: "Units",
		titleFontSize: 24,
		fontFamily: "Roboto"
	},
	data: [{
		type:"line",
		color:"DarkCyan",
		axisYType: "secondary",
		name: "sleep",
		showInLegend: false,
		markerSize: 5,
		yValueFormatString: "",
		dataPoints: dataSleep
	}]
});


function addData(data) {
	for (var i = 0; i < data.length; i++) {
		dataWork.push({
			x: new Date(data[i].date),
			y: data[i].work
		})}

	for (var i = 0; i < data.length; i++) {
		dataFamily.push({
			x: new Date(data[i].date),
			y: data[i].family
		})}

	for (var i = 0; i < data.length; i++) {
		dataHobby.push({
			x: new Date(data[i].date),
			y: data[i].hobby
		})}

	for (var i = 0; i < data.length; i++) {
		dataSleep.push({
			x: new Date(data[i].date),
			y: data[i].sleep
		})}

	workchart.render();
	familychart.render();
	hobbychart.render();
	sleepchart.render();
}

$.getJSON("static/chart.json", addData);

};