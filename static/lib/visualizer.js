var inputNodes = 2;
var hiddenLayers = 0;
var hiddenNodes = [];
var outputNodes = 2;

var learningRate = 0.01;
var activation = 'Tanh';
var problemType = 'Classification';

var epochs = 2;

$(document).ready(function() {
    
    // Resize stats chart
    var $canvas = $('#stats-chart');
    var $parent = $canvas.parent();
    $canvas.width($parent.width());
    $canvas.height($canvas.width());
    
    var processedChartData = [];
    var chartColors = [];

    for(var i = 0; i < chartData.length; i++) {
        processedChartData.push({
            x: parseFloat(chartData[i].split(',')[0]),
            y: parseFloat(chartData[i].split(',')[1])
        });
        
        label = parseInt(chartData[i].split(',')[2]);
        if(label == -1) {
            chartColors.push('#29B6F6');
        } else {
            chartColors.push('#FFA726');
        }
    }
    
    var ctx = document.getElementById('stats-chart').getContext('2d');
    var statsChart = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Training Dataset',
                data: processedChartData,
                pointBackgroundColor: chartColors
            }]
        },
        options: {
            scales: {
                xAxes: [{
                    type: 'linear',
                    position: 'bottom',
                    ticks: {
                        min: -6,
                        max: 6
                    }
                }],
                yAxes: [{
                    ticks: {
                        min: -6,
                        max: 6
                    }
                }]
            }
        }
    });
});

function hiddenLayersNodes() {
    hiddenLayers = $('#n-hidden-layers').val();
    
    $('#hidden-nodes').empty();
    for(var i = 1; i <= hiddenLayers; i++) {
        var layerId = 'L' + i;
        $('#hidden-nodes').append('<div class="input-group"><div class="input-group-prepend"><span class="input-group-text">' + layerId + ' Nodes</span></div><input class="form-control" type="number" value="4" id="' + layerId + '"></div>');
    }
}

// GENERATE MODEL
function generateModel() {
    // Reset parameters
    $('#epoch').text('Epoch: 0');
    $('#total-loss').text('0');
    $('#accuracy').text('0');
    
    // Set variables
    inputNodes = $('#input-layer').val();
    
    hiddenNodes = [];
    for(var i = 1; i <= hiddenLayers; i++) {
        var layerId = 'L' + i;
        var n_nodes = $('#' + layerId).val();
        hiddenNodes.push(n_nodes);
    }
    
    outputNodes = $('#output-layer').val();
    
    learningRate = $('#learning-rate').val();
    activation = $('#activation').val();
    problemType = $('#problem-type').val();
    
    // Send variables to server
    $.ajax({
        type: 'POST',
        url: '/generate_model',
        contentType: 'application/json',
        data: JSON.stringify({
            input_layer: inputNodes,
            hidden_layers: hiddenNodes,
            output_layer: outputNodes,
            activation: activation,
            learning_rate: learningRate,
            problem_type: problemType
        }),
        dataType: 'json',
        success: function(response) {
            console.log(response);
        },
        error: function(error) {
            console.log(error);
        }
    });
    
    // Draw network
    redraw();
}

var $lossChart;
$scope.$on("create", function (event, chart) {
    if (typeof $lossChart !== "undefined") {
        $lossChart.destroy();
    }

    $lossChart = lossChart;
});

function epochTrain() {
    $('#trainingModal').modal();
    
    $('#epoch-play .fa').toggleClass('fa-pause');
    $('#epoch-play .fa').toggleClass('fa-play');
    
    epochs = $('#epochs').val();
    
    $.ajax({
        type: 'POST',
        url: '/train',
        contentType: 'application/json',
        data: JSON.stringify({
            n_epochs: epochs
        }),
        dataType: 'json',
        success: function(response){
            $('#total-loss').text(response['loss']);
            $('#accuracy').text(response['acc']);
            
            setTimeout(function(){$('#trainingModal').modal('hide')}, 900)
            
            // Resize loss chart
            var $canvas = $('#loss-chart');
            var $parent = $canvas.parent();
            $canvas.width($parent.width());
            $canvas.height($canvas.width());
            
            total_loss = response['total_loss'];
            var lossData = [];
            console.log(total_loss);
            for(var i = 1; i <= total_loss.length; i++) {
                lossData.push({
                    x: i,
                    y: total_loss[i]
                });
            }
            
            var ctx = document.getElementById('loss-chart').getContext('2d');
            var lossChart = new Chart(ctx, {
                type: 'line',
                data: {
                    datasets: [{
                        label: 'Loss',
                        data: lossData
                    }]
                },
                options: {
                    scales: {
                        xAxes: [{
                            type: 'linear',
                            position: 'bottom'
                        }],
                    },
                    elements: {
                        point: {
                            radius: 0
                        }
                    }
                }
            });
        },
        error: function(error){
            console.log(error);
        }
    });
}

function redraw() {
    var cy = cytoscape({
        container: $('#cy'),
        elements: createNetwork(),
        userZoomingEnabled: false,
        userPanningEnabled: false,
        autoungrabify: true,
        boxSelectionEnabled: false
    });
    
    cy.layout({
        name: 'breadthfirst',
        directed: true,
        spacingFactor: 1.5,
    }).run();
    
    for(var i = 0; i < cy.nodes().length; i++) {
        cy.nodes()[i].position({
            x: cy.nodes()[i].position('y'),
            y: cy.nodes()[i].position('x')
        })
    }
}

function createNetwork() {
    var graph = [];
    
    // INPUT LAYER
    for(var i = 0; i < inputNodes; i++) {
        graph.push({
            data: {id: 'i' + i}
        });
    }
    
    // HIDDEN LAYERS
    for(var i = 0; i < hiddenLayers; i++) {
        for(var j = 0; j < hiddenNodes[i]; j++) {
            graph.push({
                data: {id: 'h' + i + 'n' + j}
            });
            
            if(i == 0) {
                for(var k = 0; k < inputNodes; k++) {
                    nSource = 'i' + k;
                    nTarget = 'h' + i + 'n' + j;
                    graph.push({
                        data: {id: 'i' + k + '-h' + i + 'n' + j, source: nSource, target: nTarget}
                    });
                }
            } else {
                for(var k = 0; k < hiddenNodes[i-1]; k++) {
                    nSource = 'h' + eval(i-1) + 'n' + k;
                    nTarget = 'h' + i + 'n' + j;
                    graph.push({
                        data: {id: nSource + '-' + nTarget, source: nSource, target: nTarget}
                    });
                }
            }
        }
    }
    
    // OUTPUT LAYER
    for(var i = 0; i < outputNodes; i++) {
        graph.push({
            data: {id: 'o' + i}
        });
   
        if(hiddenLayers > 0) {
            for(var j = 0; j < hiddenNodes[hiddenLayers - 1]; j++) {
                nSource = 'h' + eval(hiddenLayers-1) + 'n' + j;
                nTarget = 'o' + i;
                graph.push({
                    data: {id: nSource + '-' + nTarget, source: nSource, target: nTarget}
                });
            }
        } else {
            for(var j = 0; j < inputNodes; j++) {
                nSource = 'i' + j;
                nTarget = 'o' + i;
                graph.push({
                    data: {id: nSource + '-' + nTarget, source: nSource, target: nTarget}
                });
            }
        }
    }
    
    return graph
}
