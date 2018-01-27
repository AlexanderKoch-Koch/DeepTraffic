from Naked.toolshed import shell
import numpy as np


class Agent:

    def __init__(self, params):
        self.params = params

    def run(self, queue):
        #print(self.generate_code(self.params))
        js = shell.muterun_js("javascript/train_webworker.js", arguments=self.generate_arguments())
        #print(js.stdout)
        result = float(js.stdout[-6:])
        #print(result)
        queue.put(result)

    def generate_arguments(self):
        arguments = ""
        for i in range(len(self.params)):
            if self.params[i] % 1 == 0:
                arguments += str(int(self.params[i]))
            else:
                arguments += str(self.params[i])
            arguments += " "
        return arguments

    #@staticmethod
    def generate_code(self, params):
        #print(int(params[0]))
        code =  'lanesSide = ' + str(int(params[0])) + ';\\n' + \
                'patchesAhead = ' + str(int(params[1])) + ';\\n' + \
                'patchesBehind = ' + str(int(params[2])) + ';\\n' + \
                'trainIterations = ' + str(int(params[3])) + ';\\n' + \
                'otherAgents = 0;\\n' + \
                'var num_inputs = (lanesSide * 2 + 1) * (patchesAhead + patchesBehind);\\n' + \
                'var num_actions = 5;\\n' + \
                'var temporal_window = ' + str(int(params[12])) + ';\\n' + \
                'var network_size = num_inputs * temporal_window + num_actions * temporal_window + num_inputs;\\n' + \
                'var layer_defs = [];\\n' + \
                'layer_defs.push({\\n' + \
                '    type: \'input\',\\n' + \
                '    out_sx: 1,\\n' + \
                '    out_sy: 1,\\n' + \
                '    out_depth: network_size\\n' + \
                ' });\\n' + \
                'layer_defs.push({\\n' + \
                '    type: \'fc\',\\n' + \
                '    num_neurons: ' + str(int(params[4])) + ',\\n' + \
                '    activation: \'relu\'\\n' + \
                '});\\n'
        if(params[5] > 0):
            code += 'layer_defs.push({\\n' + \
                    '    type: \'fc\',\\n' + \
                    '    num_neurons: ' + str(int(params[5])) + ',\\n' + \
                    '    activation: \'relu\'\\n' + \
                    '});\\n'
            if params[6] > 0:
                code += 'layer_defs.push({\\n' + \
                        '    type: \'fc\',\\n' + \
                        '    num_neurons: ' + str(int(params[6])) + ',\\n' + \
                        '    activation: \'relu\'\\n' + \
                        '});\\n'

        code += 'layer_defs.push({\\n' + \
                '    type: \'regression\',\\n' + \
                '    num_neurons: num_actions\\n' + \
                '});\\n' + \
                'var tdtrainer_options = {\\n' + \
                '    learning_rate: ' + str(params[7]) + ',\\n' + \
                '    momentum: ' + str(params[8]) + ',\\n' + \
                '    batch_size: ' + str(int(params[9])) + ',\\n' + \
                '    l2_decay: ' + str(params[10]) + '\\n' + \
                '};\\n' + \
                'var opt = {};\\n' + \
                '    opt.temporal_window = temporal_window;\\n' + \
                '    opt.experience_size = 3000;\\n' + \
                '    opt.start_learn_threshold = 500;\\n' + \
                '    opt.gamma = ' + str(params[11]) + ';\\n' + \
                '    opt.learning_steps_total = 10000;\\n' + \
                '    opt.learning_steps_burnin = 1000;\\n' + \
                '    opt.epsilon_min = 0.0;\\n' + \
                '    opt.epsilon_test_time = 0.0;\\n' + \
                '    opt.layer_defs = layer_defs;\\n' + \
                '    opt.tdtrainer_options = tdtrainer_options;\\n' + \
                '    brain = new deepqlearn.Brain(num_inputs, num_actions, opt);\\n' + \
                '    learn = function (state, lastReward) {\\n' + \
                '        brain.backward(lastReward);\\n' + \
                '        var action = brain.forward(state);\\n' + \
                '        draw_net();\\n' + \
                '        draw_stats();\\n' + \
                '        return action;\\n' + \
                '    }\\n'

        return code
