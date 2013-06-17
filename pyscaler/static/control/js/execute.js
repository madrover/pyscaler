$(document).ready(function(){
    // Populate node div
	$('form').on('click', 'input:radio[name="cluster"]', function(event){
        $.get('/control/cluster/' + $(this).val() + "/nodelist", function(data) {
        	nodes="";
        	for (var i=0; i < data.nodes.length; i++) {
			 nodes = nodes + '<input type="radio" name="node" value="' + data.nodes[i] +'">' + data.nodes[i] +'<br>'
			};
			$("#nodes").html(nodes);
       	});	
    });
    $('form').on('click', '#executescript', function(event){
    	//Preventing button default action to be executed
    	event.preventDefault();
    	//Erasing output div counter
    	$('#output').html("");
		//Getting cluster value
    	var cluster = 	$('input:radio[name=cluster]:checked').val();
    	// Checking if cluster is marked
    	if (typeof cluster === "undefined") {
    		$('#output').append("<b>Cluster not chosen</b>");
    		return;
    	}	
    	//Getting script value
    	var script = 	$('input:radio[name=script]:checked').val();
    	// Checking if script is marked
    	if (typeof script === "undefined") {
    		$('#output').append("<b>Script not chosen</b>");
    		return;
    	}
    	
    	//Getting node value, may be undefined
    	var node = 	$('input:radio[name=node]:checked').val();
		if (typeof node === "undefined") {
			var executeurl = "/actions/executescript/" + script + "/cluster/" + cluster;
		}else{
			var executeurl = "/actions/executescript/" + script + "/cluster/" + cluster + "/node/" + node;
		}
    	//alert(executeurl);
		$.ns = {};
		$("#output").html("<b>Executing " + script + "</b></br>");
		$.get(executeurl, function(data) {
			$("#output").append("<b>Task ID: " + data.taskid + "</b></br>");
			$("#output").append("<b>Executing</b>");
			$.ns.taskid = data.taskid;
			var a =0;
			var output = "";
			var intervalId = setInterval( function() 
			    {
			        a = a + 1;
			      	if (a%5==0){
			      		$.get('/actions/executescript/output/' + $.ns.taskid + "/", function(data) {
			      			$.ns.output = data;
			      			if (data.state != "PENDING" &&  data.state != "STARTED"){
			      				clearInterval(intervalId);
			      				$("#output").append("</br>");
								$("#output").append("<b>Task state = " + $.ns.output.state + "</b></br>");
								$("#output").append("<b>Output = </b></br>");
								$("#output").append("<pre>" + $.ns.output.result + "</pre></br>");
			      				};
			      		});
			      	if (a==60){
			      		clearInterval(intervalId);
			      		$("#output").append("</br><b>Task timeout</b>");
			      		}
			      	};

			      	$("#output").append(".");
			    }, 1000);
		})
		.fail(function() { $("#output").append("<b>Error creating task</b>"); });
    });
 });