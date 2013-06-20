$(document).ready(function(){
    // Populate node div
	$('form').on('click', 'input:radio[name="cluster"]', function(event){
        $.get('/control/cluster/' + $(this).val() + "/triggerlist", function(data) {
        	triggers="";
        	for (var i=0; i < data.triggers.length; i++) {
			 triggers = triggers + '<input type="radio" name="trigger" value="' + data.triggers[i] +'">' + data.triggers[i] +'<br>'
			};
			$("#triggers").html(triggers);
       	});	
    });
	$('form').on('click', 'input:radio[name="trigger"]', function(event){
        $.get('/control/trigger/' + $(this).val() + "/actionlist/", function(data) {
        	actions="";
        	for (var i=0; i < data.actions.length; i++) {
			 actions = actions + "<b>" + data.actions[i][0] +' - </b>' + data.actions[i][1] +'<br>';
			};
			$("#actions").html(actions);
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
    	var trigger = 	$('input:radio[name=trigger]:checked').val();
    	// Checking if script is marked
    	if (typeof trigger === "undefined") {
    		$('#output').append("<b>Trigger not chosen</b>");
    		return;
    	}
    	var ac = 	$('input:radio[name=trigger]:checked').val();
    	// Checking if script is marked
    	if (typeof trigger === "undefined") {
    		$('#output').append("<b>Trigger not chosen</b>");
    		return;
    	}

		var executeurl = "/control/trigger/" + trigger + "/execute/";

    	
    	 //alert(executeurl);
		$.ns = {};
		$("#output").html("<b>Executing " + trigger + "</b></br></br>");
		$.get(executeurl, function(data) {
			for (var i=0;i<data.length;i++){ 
				taskid = data[i].taskid;
				action = data[i].action;
				order = data[i].order;
				$("#output").append('<div id="' +taskid + '"></div>');
				$("#output").append('<div id="' +taskid + 'out"></div>');
				$("#" + taskid).append("<b>" +  data[i].order + " - " + action + " Destination: " + data[i].destination + "</b></br>");
				$("#" + taskid).append("<b>Task ID: " + taskid + "</b></br>");
				$("#" + taskid).append("<b>Executing</b>");
			}
			;
			window.currenttask = 0
			window.intervalId = setInterval( function(){checktaskoutput(data)}, 1000);
		})
		.fail(function() { $("#output").append("<b>Error creating task</b>"); });
    });
    
    
    function checktaskoutput(data) {
    	if (window.currenttask == data.length){
    		clearInterval(window.intervalId);
    	}
    	else{
    		window.seconds = window.seconds + 1;
    		if (window.seconds %5==0){
			$.get('/control/trigger/output/' + data[window.currenttask].taskid + "/", function(data) {
	 			if (data.state != "PENDING" &&  data.state != "STARTED"){
						//clearInterval(intervalId);
						tx = $("#" + data.taskid + "out").text()
						if ($("#" + data.taskid + "out").text() == "") {
		 					$("#" + data.taskid + "out").append("</br>");
							$("#" + data.taskid + "out").append("<b>Task state = " + data.state + "</b></br>");
							$("#" + data.taskid + "out").append("<b>Output = </b></br>");
							$("#" + data.taskid + "out").append("<pre>" + data.result + "</pre></br>");
							window.currenttask = window.currenttask + 1
							window.seconds=0
							}
		 				};
		 		});
		 	
		 		if (window.seconds >=300){
					if ($("#" + data.taskid + "out").text() == "") {
						$("#" + data.taskid + "out").append("</br><b>Task timeout</b>");
						window.currenttask = window.currenttask + 1
						window.seconds=0
					};
				};
			}
		if (($("#" + data[window.currenttask].taskid + "out").text() == "") && (window.seconds%2==0)){
				$("#" + data[window.currenttask].taskid).append(".");
		};
			
		};
		
	};
 });