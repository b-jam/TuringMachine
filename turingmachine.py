import csv
from optparse import OptionParser

class TuringState():

    def __init__(self, name):
        self.name = name
        self.actions = {}

    def add_action(self, symbol, action, new_state):
        self.actions[symbol] = (action, new_state)
        
    def process(self, reading):
        try:
            action, new_state = self.actions[reading]
        except KeyError:
            print "State %s has no action %s" % (self.name, reading)
            exit(1)
        return action, new_state


class TuringMachine():
    
    def __init__(self, input_str):
        self.input_str = input_str
        initial_state = TuringState('q0')
        initial_state.add_action('B', 'B', 'H')
        halt_state = TuringState('H')
        self.states = {initial_state.name : initial_state,
                       halt_state.name : halt_state}
        
    def add_state(self, state):
        self.states[state.name] = state

    def run(self):
        current_state = 'q0'
        output_str = list(self.input_str)
        symbol = output_str[0]
        position = 0
        while current_state != 'H':
            print  ''.join(output_str).replace('B','_'), current_state
            print " "*position + "^"
            action, new_state = self.states[current_state].process(symbol)
            if action == 'L':
                position -=1
                if position < 0:
                    position =  0
                    output_str = ["B"] + output_str
            elif action == 'R':
                position +=1
                if position > len(output_str)-1:
                    output_str += "B"
            else:
                output_str[position] = action

            current_state = new_state
            symbol = output_str[position]

        output_str = ''.join(output_str).strip('B')
        return output_str, len(output_str)


def construct_machine(filename, initial_input):
    m = TuringMachine(initial_input)
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        states = {}
        for state, symbol, action, nextstate in reader:
            if state in states:
                s = states[state]
            else:
                s = TuringState(state)
                m.add_state(s)
                states[state] = s
            s.add_action(symbol.strip(), action.strip(), nextstate.strip())
    return m

def parse_args():
    parser = OptionParser()
    _, args = parser.parse_args()
    return args
    
def main():
    args = parse_args()
    m = construct_machine(args[0], args[1])
    output, length =  m.run()
    print "Output: %s \nLength: %d" %(output, length)
    
if __name__ == '__main__':
    main()
