import re
import nltk
import string

global output


def everything():
    all_parameters = list()
    alphabet = list(string.ascii_lowercase)
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    control_structure = ['if', 'then', 'else', 'while', 'do', 'repeat']
    reserved_words = ['if', 'else', 'while', '[', ']', '|', 'PROCS', 'ROBOT_R', 'VARS', 'then', 'do', 'repeat',
                      'assignTo',
                      'goto', 'move', 'turn', 'face', 'put', 'pick', 'movetothe', 'moveindir', 'jumptothe', 'jumpindir',
                      'nop', 'facing', 'canput', 'canpick', 'canmoveindir', 'canjumpindir', 'canmovetothe',
                      'canjumptothe', 'not']

    def run_script():
        # Función principal
        all_lines = read_file("programa.txt")
        lines_concat = str()

        for line in all_lines:
            lines_concat += line

        if lines_concat[:7].upper() != 'ROBOT_R':
            print('Programa no válido, no comienza con "ROBOT_R"')
            exit()

        nw_lines = lines_concat[7:]
        words = nltk.tokenize.word_tokenize(nw_lines)
        vars_bool = False
        vars_procs = False

        # Chequea si hay VARS
        if 'VARS' in words:
            vars_bool = True
            index = words.index('VARS')
            string = get_until_semicolon(words, index + 3)
            variables = [i for i in string.split(',') if check_if_valid_name(i)]
            reserved_words.extend(variables)

        # Chequea si hay PROCS
        for i in range(len(words)):
            if 'PROCS' in words[i]:
                vars_procs = True
                index_1 = words[i].index('PROCS')
                words[i] = words[i][index_1 + 5:]

        phrases = get_phrases(words)
        for key in phrases.keys():
            check_if_valid_phrase(phrases[key], key)

        return None

    def read_file(ruta: str):
        # Función para leer el archivo y retornar una lista sin espacios innecesarios con las líneas que no son vacías

        with open(ruta) as file:
            lines = file.readlines()

        for i in range(len(lines)):
            lines[i] = lines[i].replace("\n", "")

        list = [i.strip() for i in lines if i.strip()]
        return list

    def check_if_valid_name(name):
        name = name.lower().strip()

        if name[0] in alphabet:
            for i in name:
                if i not in alphabet and i not in digits:
                    return False
            return True
        else:
            return False

    def get_phrases(words):
        phrases = {}
        phrases['instructions'] = []
        phrases['procs'] = []
        last_index = len(words) - 1
        index_1 = last_index
        all_passed = False
        current_last_index = last_index
        # Recorrido de adelante hacia atrás
        while not all_passed:
            words[index_1] = words[index_1].strip()
            if words[index_1] == ']':
                count_closed_brackets = 1
                count_open_brackets = 0
                while count_closed_brackets != count_open_brackets:
                    token = get_previous_token(words, index_1)
                    index_1 -= 1
                    if token == ']':
                        count_closed_brackets += 1
                    elif token == '[':
                        count_open_brackets += 1

                lst = words[index_1:current_last_index + 1]
                phrase = "".join(words[index_1:current_last_index + 1])
                if not check_if_valid_name(words[index_1 - 1]):
                    phrases['instructions'].append(lst)
                elif check_if_valid_name(words[index_1 - 1]):
                    lst.insert(0, words[index_1 - 1])
                    phrases['procs'].append(lst)

                index_1 -= 1
                current_last_index = index_1

            elif index_1 == 0:
                all_passed = True
            else:
                index_1 -= 1
                current_last_index = index_1

        return phrases

    def check_if_valid_phrase(phrases, type):
        if type == 'procs':
            for phrase in phrases:
                # parameters guarda en [0] los params de una frase y en [1] el bloque a procesar
                parameters = check_parameters(phrase)
                if parameters:
                    check_if_valid_block(parameters[1])
                else:
                    check_if_valid_block(phrase[1:-1])

        elif type == 'instructions':
            for phrase in phrases:
                if phrase[1] == '[' and phrase[-1] == ']':
                    phrase = phrase[1:-1]
                else:
                    print('Sintaxis para bloque de instrucciones inválida')
                check_if_valid_block(phrase)

    def check_parameters(proc_statement):
        if proc_statement[1] == '[' and proc_statement[-1] == ']':
            proc_statement = proc_statement[2:-1]
            if not '|' in proc_statement[0] or (proc_statement[0]).find("|") != 0:
                print('Definición de función sin definir parámetros apropiadamente')
            else:
                sentence = str(proc_statement[0]).removeprefix("|")
                if sentence:
                    try:
                        all_phrase = "".join(proc_statement).removeprefix("|")
                        nxt_index = all_phrase.find("|")
                        all_parameters = all_phrase[:nxt_index].split(",")
                        proc_statement[nxt_index] = proc_statement[nxt_index].removeprefix("|")
                        if not proc_statement[nxt_index]:
                            del proc_statement[nxt_index]
                        params = []
                        for i in all_parameters:
                            if i not in reserved_words and check_if_valid_name(i):
                                params.append(i)
                            else:
                                print('No se pueden usar palabras reservadas para definir parámetros')
                        return params, proc_statement[nxt_index:]

                    except Exception as e:
                        print('No hay delimitadores suficientes para los parametros de la función')
                else:
                    return [], proc_statement[2:]

    def check_if_valid_block(string):
        print(string)

    def get_previous_token(lst, index):
        return lst[index - 1]

    def get_until_semicolon(lista, pos):
        cad = ''
        semicolon_found = False
        i = pos
        while not semicolon_found and i < len(lista):
            if lista[i] != ';':
                cad += lista[i]
            else:
                semicolon_found = True
            i += 1
        return cad

    return run_script()


print(everything())
