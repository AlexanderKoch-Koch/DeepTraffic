code = "lanesSide = 0;\n" +
    "patchesAhead = 1;\n" +
    "patchesBehind = 0;\n" +
    "trainIterations = 10000;\n" +
    "\n" +
    "// the number of other autonomous vehicles controlled by your network\n" +
    "otherAgents = 0; // max of 9\n" +
    "\n" +
    "var num_inputs = (lanesSide * 2 + 1) * (patchesAhead + patchesBehind);\n" +
    "var num_actions = 5;\n" +
    "var temporal_window = 1;\n" +
    "var network_size = num_inputs * temporal_window + num_actions * temporal_window + num_inputs;\n" +
    "\n" +
    "var layer_defs = [];\n" +
    "    layer_defs.push({\n" +
    "    type: 'input',\n" +
    "    out_sx: 1,\n" +
    "    out_sy: 1,\n" +
    "    out_depth: network_size\n" +
    "});\n" +
    "layer_defs.push({\n" +
    "    type: 'fc',\n" +
    "    num_neurons: 1,\n" +
    "    activation: 'relu'\n" +
    "});\n" +
    "layer_defs.push({\n" +
    "    type: 'regression',\n" +
    "    num_neurons: num_actions\n" +
    "});\n" +
    "\n" +
    "var tdtrainer_options = {\n" +
    "    learning_rate: 0.001,\n" +
    "    momentum: 0.0,\n" +
    "    batch_size: 64,\n" +
    "    l2_decay: 0.01\n" +
    "};\n" +
    "\n" +
    "var opt = {};\n" +
    "opt.temporal_window = temporal_window;\n" +
    "opt.experience_size = 3000;\n" +
    "opt.start_learn_threshold = 500;\n" +
    "opt.gamma = 0.7;\n" +
    "opt.learning_steps_total = 10000;\n" +
    "opt.learning_steps_burnin = 1000;\n" +
    "opt.epsilon_min = 0.0;\n" +
    "opt.epsilon_test_time = 0.0;\n" +
    "opt.layer_defs = layer_defs;\n" +
    "opt.tdtrainer_options = tdtrainer_options;\n" +
    "console.log('hello world');\n" +
    "brain = new deepqlearn.Brain(num_inputs, num_actions, opt);\n" +
    "\n" +
    "learn = function (state, lastReward) {\n" +
    "brain.backward(lastReward);\n" +
    "var action = brain.forward(state);\n" +
    "\n" +
    //"draw_net();\n" +
    //"draw_stats();\n" +
    "\n" +
    "return action;\n" +
    "}"
 //brain.learning = false;
    //var button = document.getElementById("trainButton");
    //var progress = document.getElementById("trainProgress");
    //button.setAttribute("style", "display: none;");
    //progress.value = 0;
    //progress.setAttribute("style", ";");
    //if (window.Worker) {
if (typeof(Worker) == "undefined") {
    console.log("web worker not supported");
}
var myWorker = new Worker("train_webworker.js");
        /*myWorker.onmessage = function (e) {
            if (typeof e.data.percent != 'undefined') {
                progress.value = e.data.percent;
            }

            if (typeof e.data.net != 'undefined') {
                brain.value_net.fromJSON(e.data.net);
                // jack 2018-01-04
                //transplantBrains(brain, brains);
                for (let i = 0; i < nOtherAgents; i++) {
                   brains[i].value_net = brain.value_net;

                }
                console.log("setting Net");
            }

            if (typeof e.data.done != 'undefined') {
                progress.setAttribute("style", "display: none;");
                button.setAttribute("style", ";");
                swal("Training finished!", "", "success");
            }
        };
        myWorker.postMessage(getData());
    }*/