		function counterGraph(url,placeholder,placeholderrst,options){
			var data ="";
			$.ajax({
				url: url,
				method: 'GET',
				dataType: 'json',
				success: function(datasets){
					var plot = $.plot(placeholder, datasets, options);
					data = datasets;
					}
				}); 
			placeholder.bind("plotselected", function (event, ranges) {
				var plot = $.plot(placeholder, data, $.extend(true, {}, options, {
								xaxis: {
									min: ranges.xaxis.from,
									max: ranges.xaxis.to
								},
								yaxis: {
									min: ranges.yaxis.from,
									max: ranges.yaxis.to
								},
				}));
			});
				
		
		
			var plot = $.plot(placeholder, data, options);
			$(placeholderrst).click(function(event){
				event.preventDefault();
				var plot_xaxis = plot.getAxes().xaxis;
				plot = $.plot(placeholder, data,
					$.extend(true, {}, options, {
						xaxis: {mode: "time" ,min:plot_xaxis.datamin , max: plot_xaxis.datamax }
					}));
			});

		};