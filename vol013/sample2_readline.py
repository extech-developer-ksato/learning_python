import readline
import logging

LOG_FILENAME = 'sample2.log'
logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.DEBUG,
                    )

class BufferAwareCompleter(object):
    
    def __init__(self, options):
        self.options = options
        self.current_candidates = []
        return

    def complete(self, text, state):
        response = None
        if state == 0:
            # このテキストは初めてなのでマッチリストを作成する
            
            origline = readline.get_line_buffer()
            begin = readline.get_begidx()
            end = readline.get_endidx()
            being_completed = origline[begin:end]
            words = origline.split()

            logging.debug('origline=%s', repr(origline))
            logging.debug('begin=%s', begin)
            logging.debug('end=%s', end)
            logging.debug('being_completed=%s', being_completed)
            logging.debug('words=%s', words)
            
            if not words:
                self.current_candidates = sorted(self.options.keys())
            else:
                try:
                    if begin == 0:
                        # 最初の単語
                        candidates = self.options.keys()
                    else:
                        # 後続の単語
                        first = words[0]
                        candidates = self.options[first]
                    
                    if being_completed:
                        # 補完される入力部をもつオプションにマッチする
                        self.current_candidates = [ w for w in candidates
                                                    if w.startswith(being_completed) ]
                    else:
                        # 空の文字列がマッチしたので全ての候補を使用する
                        self.current_candidates = candidates

                    logging.debug('candidates=%s', self.current_candidates)
                    
                except (KeyError, IndexError) as err:
                    logging.error('completion error: %s', err)
                    self.current_candidates = []
        
        try:
            response = self.current_candidates[state]
        except IndexError:
            response = None
        logging.debug('complete(%s, %s) => %s', repr(text), state, response)
        return response
            

def input_loop():
    line = ''
    while line != 'stop':
        line = input('Prompt ("stop" to quit): ')
        print(f'Dispatch {line}')

# 補完関数を登録する
readline.set_completer(BufferAwareCompleter(
    {'list':['files', 'directories'],
     'print':['byname', 'bysize'],
     'stop':[],
    }).complete)

# 補完に tab キーを使用する
readline.parse_and_bind('tab: complete')

# ユーザへテキストを表示する
input_loop()