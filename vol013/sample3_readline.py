import readline
import logging
import os

LOG_FILENAME = 'sample3.log'
HISTORY_FILENAME = 'sample3.history'

logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.DEBUG,
                    )

def get_history_items():
    return [ readline.get_history_item(i)
             for i in range(1, readline.get_current_history_length() + 1)
             ]

class HistoryCompleter(object):
    
    def __init__(self):
        self.matches = []
        return

    def complete(self, text, state):
        response = None
        if state == 0:
            history_values = get_history_items()
            logging.debug('history: %s', history_values)
            if text:
                self.matches = sorted(h 
                                      for h in history_values 
                                      if h and h.startswith(text))
            else:
                self.matches = []
            logging.debug('matches: %s', self.matches)
        try:
            response = self.matches[state]
        except IndexError:
            response = None
        logging.debug('complete(%s, %s) => %s', 
                      repr(text), state, repr(response))
        return response

def input_loop():
    if os.path.exists(HISTORY_FILENAME):
        readline.read_history_file(HISTORY_FILENAME)
    print(f'Max history file length: {readline.get_history_length()}')
    print(f'Startup history: {get_history_items()}')
    try:
        while True:
            line = input('Prompt ("stop" to quit): ')
            if line == 'stop':
                break
            if line:
                print(f'Adding "{line}" to the history')
    finally:
        print(f'Final history: {get_history_items()}')
        readline.write_history_file(HISTORY_FILENAME)

# 補完関数を登録する
readline.set_completer(HistoryCompleter().complete)

# 補完に tab キーを使用する
readline.parse_and_bind('tab: complete')

# ユーザへテキストを表示する
input_loop()