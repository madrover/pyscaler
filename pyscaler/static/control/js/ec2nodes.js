
	function executetask(executeurl){
		$.get(executeurl, function(data) {
			$("#output").append("<b>Task ID: " + data.taskid + "</b></br>");
			$("#output").append("<b>Executing</b>");
			var counter = 0;
			var intervalId = setInterval(function(){
					$.ns = {};
					$.ns.taskid = data.taskid;
					var output = "";
				    counter = counter + 1;
				  	if (counter%5==0){
				  		$.get('/actions/ec2node/output/' + $.ns.taskid + "/", function(data) {
				  			$.ns.output = data;
				  			if (data.state != "PENDING" &&  data.state != "STARTED"){
				  				clearInterval(intervalId);
				  				$("#output").append("</br>");
								$("#output").append("<b>Task state = " + $.ns.output.state + "</b></br>");
								$("#output").append("<b>Output = </b></br>");
								$("#output").append("<pre>" + $.ns.output.result + "</pre></br>");
				  				};
				  		});
					  	if (counter==300){
					  		clearInterval(intervalId);
					  		$("#output").append("</br><b>Task timeout</b>");
						};
				  	} ;
					if (counter%2==0){
					  	$("#output").append(".");
					}
				}
				, 1000);
		})
		.fail(function() { $("#output").append("<b>Error creating task</b>"); });
	};



$(document).ready(function(){
    // Populate node div
	$('form').on('click', 'input:radio[name="cluster"]', function(event){
        $.get('/control/cluster/' + $(this).val() + "/nodelist", function(data) {
        	nodes="";
        	for (var i=0; i < data.nodes.length; i++) {
			 nodes = nodes + '<input type="radio" name="node" value="' + data.nodes[i] +'"> ' + data.nodes[i] +'<br>'
			};
			$("#nodes").html(nodes);
       	});	
    });
	// Populate EC2 Profile Info div
	$('form').on('click', 'input:radio[name="ec2profile"]', function(event){
        $.get('/control/ec2profile/detail/' + $(this).val(), function(data) {
        	nodeinfo ="<lu>";
        	
        	for (var key in data) {
 			if (data.hasOwnProperty(key)) {
    			nodeinfo = nodeinfo + "<li> " + key + " = " + data[key] + "</li>";
  				}
			}
			nodeinfo=nodeinfo+"</lu>";
			$("#ec2profileinfo").html(nodeinfo);
       	});	
    });
    // Add node button
    $('form').on('click', '#addnode', function(event){
    	event.preventDefault();
    	//Check if cluster is checked
    	$('#output').html("");
    	var cluster = 	$('input:radio[name=cluster]:checked').val();
    	if (typeof cluster === "undefined") {
    		$('#output').append("<b>Cluster not chosen</b>");
    		return;
    	}
    	//Check if ec2profile is checked
    	var ec2profile = 	$('input:radio[name=ec2profile]:checked').val();
    	if (typeof ec2profile === "undefined") {
    		$('#output').append("<b>Ec2 profile not chosen</b>");
    		return;
    	}
    	
    	var sshprofile = 	$('input:radio[name=sshprofile]:checked').val();
    	if (typeof sshprofile === "undefined") {
    		$('#output').append("<b>Ssh profile not chosen</b>");
    		return;
    	}
    	var jvmprofiles="";

		$(":checked.jvmprofile").each(
			function(index) {
				jvmprofiles += (jvmprofiles == "" ? this.value : "," + this.value);
			}
    	);

    	if (typeof jvmprofiles == "") {
    		$('#output').append("<b>Jvm profiles not chosen</b>");
    		return;
    	};
    	
		var executeurl = "/actions/ec2node/deploy/cluster/" + cluster + "/profile/" + ec2profile + "/sshprofile/" + sshprofile + "/jvmprofiles/" + jvmprofiles;

    	//alert(executeurl);
		$("#output").html("<b>Deploying new node on " + cluster + "</b></br>");
		executetask(executeurl);
    });
    
    $('form').on('click', '#removenode', function(event){
    	   event.preventDefault();
    	//Check if cluster is checked
    	$('#output').html("");
    	var cluster = 	$('input:radio[name=cluster]:checked').val();
    	if (typeof cluster === "undefined") {
    		$('#output').append("<b>Cluster not chosen</b>");
    		return;
    	}
    	//Check if node is checked
    	var node = 	$('input:radio[name=node]:checked').val();
    	if (typeof node === "undefined") {
    		$('#output').append("<b>Nodenot chosen</b>");
    		return;
    	}
		var executeurl = "/actions/ec2node/remove/cluster/" + cluster + "/node/" + node;

    	//alert(executeurl);
		$("#output").html("<b>Removing node " + node + " from " + cluster + "</b></br>");
		executetask(executeurl);

    });
 });
 