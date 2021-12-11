'''
Medical Tagger module
'''

import subprocess
import os
from threading import Thread
from time import sleep
from queue import Queue, Empty


class NonBlockingStreamReader:
    '''
    Source: https://gist.github.com/EyalAr/7915597
    '''

    def __init__(self, stream):
        '''
        stream: the stream to read from.
                Usually a process' stdout or stderr.
        '''
        self._s = stream      
        self._q = Queue()

        def _populate_queue(stream, queue):
            '''
            Collect lines from 'stream' and put them in 'queue'.
            '''
            while True:
                line = stream.readline()
                if line:
                    queue.put(line)
                else:
                    raise UnexpectedEndOfStream
        self._t = Thread(target=_populate_queue,
                         args=(self._s, self._q))
        self._t.daemon = True
        self._t.start()  # start collecting lines from the stream

    def readline(self, timeout=None):
        '''
        Readline
        '''
        try:
            return self._q.get(block=timeout is not None,
                               timeout=timeout)
        except Empty:
            return None


class UnexpectedEndOfStream(Exception):
    '''
    Custom exception name used in some cases when general Exception occurs.
    '''
    pass


class MedTagger:
    '''
    Wrapper around the POS tagger based on freeling.

    IMPORTANT: Before calling the wrapper, one must install the dockerized version of the
    software.

    It can be pulled doing:
    docker pull bsctemu/spaccc-pos-tagger-engine:1.0.0
    '''

    def __init__(self):
        '''
        Initialize the subprocess that will receive the inputs from the user
        '''
        # Installed docker runs OK in local but does not run inside a docker container
        self._tagger = subprocess.Popen('docker run -i   bsctemu/med-tagger:1.0.0', shell=True,
                                        stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        # # Singularity runs OK
        # os.system(
        #     'singularity build /tmp/freeling-cnio.sif docker://bsctemu/freeling-cnio:1.0.0')
        # self._tagger = subprocess.Popen('singularity run /tmp/freeling-cnio.simg', shell=True,
        #                                 stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        sleep(2)
        self._nbsr = NonBlockingStreamReader(self._tagger.stdout)
        sleep(1)

    # -------------------------------------------------------------------------

    def get_results(self, text):
        '''
        Function to get results from Freeling
        Input:
            -text: string to be tagged
        Ouput:
            -results: list of tuples
        '''
        print(text)
        results = list()
        try:
            self._tagger.stdin.write((text + '\n').encode('utf-8'))
            self._tagger.stdin.flush()
        except (BrokenPipeError, IOError):
            print('Error in writing to the tagger')
            return results
        print()
        results = []
        stop_it = 0
        while True:
            while True:
                # 0.1 secs to let the shell output the result
                output = self._nbsr.readline(0.1)
                if not output:
                    stop_it = stop_it + 1
                    break
                results.append(tuple(output.decode('utf-8').split(' ')))
            if results or stop_it > 3:
                break
        return results

    # -------------------------------------------------------------------------

    def parse(self, text):
        '''
        Function to parse a single string using the tagger.
        In order to give consistency to the output, this function always
        returns a list of lists of tuples, although the input is made by
        a single list.
        Input:
            -text: string to be tagged
        Ouput:
            -results: List of lists of tuples (original_word, lemma, tag, score)
        '''
        result = self.get_results(text)
        sentences = []
        single_sentence = []
        for item in result:
            if len(item) < 3:
                sentences.append(single_sentence)
                single_sentence = []
            else:
                single_sentence.append(item)
        return sentences

    # -------------------------------------------------------------------------

    def write_brat(self, original, parsed, folder_path):
        '''
        Function to write the parsed string into BRAT originalt file.
        Input:
            - original: the original string
            - parsed: Result from parse method
            - folder_path: Complete path to the file to be saved
        Output:
            - brat file
        :return: None
        '''

        def convert_text(original, parsed, folder_path):
            '''
            Get the different components from the freeling lines
            (original, lemma, tag, percentage(not written into brat)).
            '''
            start, end, tag_id = 0, 0, 0

            if any(isinstance(el, list) for el in parsed):
                f = open(folder_path, "w")
                for item in parsed:
                    for i, s in enumerate(item):
                        item[i] = (item[i][0], item[i][1], item[i][2])
                    for t in item:
                        forma = t[0]
                        lemma = t[1]
                        tag = t[2]
                        simple_tag = tag if (
                            tag[0] == 'F' or tag[0] == 'Z') else tag[:2]
                        start = original.find(forma, end)
                        if start == -1:
                            form_trimmed = forma.split('_')[0]
                            if form_trimmed:
                                start = original.find(form_trimmed, end)
                            else:
                                start = end + 1
                        end = start + len(forma)
                        control = forma.split('_')
                        if len(control) > 1:
                            if control[1] == '.':
                                end = start + len(forma) - 1
                        tag_id += 1
                        f.write(
                            f'T{tag_id}\t{simple_tag} {start} {end}\t{original[start:end]}\n')
                        f.write(f'#{tag_id}\tNorm T{tag_id}\t{lemma} {tag}\n')
                f.close()
            else:
                f = open(folder_path, "w")
                for t in parsed:
                    t = (t[0], t[1], t[2])
                    forma = t[0]
                    lemma = t[1]
                    tag = t[2]
                    simple_tag = tag if (
                        tag[0] == 'F' or tag[0] == 'Z') else tag[:2]
                    start = original.find(forma, end)
                    if start == -1:
                        form_trimmed = forma.split('_')[0]
                        if form_trimmed:
                            start = original.find(form_trimmed, end)
                        else:
                            start = end + 1
                    end = start + len(forma)
                    control = forma.split('_')
                    if len(control) > 1:
                        if control[1] == '.':
                            end = start + len(forma) - 1
                    tag_id += 1
                    f.write(
                        f'T{tag_id}\t{simple_tag} {start} {end}\t{original[start:end]}\n')
                    f.write(f'#{tag_id}\tNorm T{tag_id}\t{lemma} {tag}\n')
                f.close()

    # -------------------------------------------------------------------------

        # Call the previous convert text function.
        convert_text(original, parsed, folder_path)

    def __del__(self):
        '''
        Destroyer that will kill the background docker container.
        Updated on 2019-09-23: Destroyer that stops the singularity instance container.
        '''
        # Docker version
        # self._tagger.kill()

        # Singularity version
        # os.system('singularity instance.stop freeling-cnio')
