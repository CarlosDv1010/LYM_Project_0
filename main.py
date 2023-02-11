import re
import nltk
import string

global output


def everything():
    all_parameters = list()
    alphabet = list(string.ascii_lowercase)
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    control_structure = 'if then else while do repeat'
    reserved_words = ['if', 'else', 'while', '[', ']', '|', 'PROCS', 'ROBOT_R', 'VARS', 'then', 'do', 'repeat',
                      'assignTo',
                      'goto', 'move', 'turn', 'face', 'put', 'pick', 'movetothe', 'moveindir', 'jumptothe', 'jumpindir',
                      'nop', 'facing', 'canput', 'canpick', 'canmoveindir', 'canjumpindir', 'canmovetothe',
                      'canjumptothe', 'not']

    commands_dct = {'assignto': ['num', 'var'], 'goto': ['num_var', 'num_var'], 'move': ['num_var'],
                    'turn': ['left right around'],
                    'face': ['north south east west'], 'put': ['num_var', 'chips balloons'],
                    'pick': ['num_var', 'chips balloons'],
                    'movetothe': ['num_var', 'front right left back'],
                    'jumptothe': ['num_var', 'front right left back'],
                    'jumpindir': ['num_var', 'north south east west'], 'nop': [],
                    'moveindir': ['num_var', 'north south east west']}

    conditions_dct = {'facing': ['north south east west'],
                      'canput': ['num_var', 'chips balloons'],
                      'canpick': ['num_var', 'chips balloons'],
                      'canjumpindir': ['num_var', 'north south east west'],
                      'canmovetothe': ['num_var', 'front right left back'],
                      'canjumptothe': ['num_var', 'front right left back'],
                      'canmoveindir': ['num_var', 'north south east west'],
                      'not': ['num_var']}

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
        recorrido = False
        i = 0
        length = len(words)
        while not recorrido and i < length:
            if '||' in words[i]:
                words.insert(i, "|")
                words[i + 1] = words[i + 1][1:]
            if ',' in words[i] and len(words[i]) > 1:
                lst = words[i].split(",")
                num = len(lst)
                index = i
                words.remove(words[i])
                for j in range(num):
                    words.insert(index, lst[j])
                    if j != num - 1:
                        words.insert(index + 1, ",")
                        index += 2
            length = len(words)
            i += 1
        vars_bool = False
        vars_procs = False

        # Chequea si hay VARS
        if 'VARS' in words:
            vars_bool = True
            index = words.index('VARS')
            string = get_until_semicolon(words, index + 3)
            variables = [i for i in string.split(',') if check_if_valid_name(i)]  # ERROR
            reserved_words.extend(variables)

        # Chequea si hay PROCS
        for i in range(len(words)):
            if 'PROCS' in words[i]:
                vars_procs = True
                index_1 = words[i].index('PROCS')
                words[i] = words[i][index_1 + 5:]

        phrases = get_phrases(words)
        check_if_valid_phrase(phrases['procs'], 'procs')
        check_if_valid_phrase(phrases['instructions'], 'instructions')

        print('Programa válido')

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
                c_open = phrase.count("[")
                c_close = phrase.count("]")
                if not c_close == c_open:
                    print('Error99')
                    exit()
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
        print(type)
        if type == 'procs':

            for phrase in phrases:
                print('AAAAAAAAAAAAAAAAAAAA', phrase)
                # parameters guarda en [0] los params de una frase y en [1] el bloque a procesar
                parameters = check_parameters(phrase)
                if parameters[0]:
                    check_if_valid_block(parameters[1])
                else:
                    frase = phrase[3:-1]
                    frase[0] = str(frase[0]).strip("|").strip('[').strip(';')
                    check_if_valid_block(frase)

        elif type == 'instructions':
            print('EEEEEEEEEEEEEEEEEEEEEEE')
            for phrase in phrases:
                if phrase[0] == '[' and phrase[-1] == ']':
                    phrase = phrase[1:-1]
                else:
                    print('Sintaxis para bloque de instrucciones inválida')
                check_if_valid_block(phrase)

    def check_parameters(proc_statement):
        name = proc_statement[0]
        commands_dct[name.lower()] = []
        if proc_statement[1] == '[' and proc_statement[-1] == ']':
            proc_statement = proc_statement[2:-1]
            if not '|' in proc_statement[0] or (proc_statement[0]).find("|") != 0:
                print('Definición de función sin definir parámetros apropiadamente')
            else:
                sentence = str(proc_statement[0])
                if sentence:
                    try:
                        all_phrase = "".join(proc_statement).removeprefix("|")
                        nxt_index = all_phrase.find("|")
                        all_parameters = all_phrase[:nxt_index].split(",")
                        commands_dct[name.lower()].extend(all_parameters)
                        proc_statement[nxt_index] = proc_statement[nxt_index].removeprefix("|")
                        if not proc_statement[nxt_index]:
                            del proc_statement[nxt_index]
                        params = []

                        if not all_parameters[0]:
                            proc_statement[0] = str(proc_statement[0]).strip('|')
                            return [], proc_statement[0:]

                        for i in all_parameters:
                            if i not in reserved_words and check_if_valid_name(i):
                                params.append(i)
                            else:
                                print('No se pueden usar palabras reservadas para definir parámetros')
                                exit()
                        if not '|' in proc_statement[nxt_index - 1]:
                            return params, proc_statement[nxt_index:]
                        else:
                            proc_statement[nxt_index - 1] = proc_statement[nxt_index - 1][
                                                            str(proc_statement[nxt_index - 1]).find('|') + 1:]

                            return params, proc_statement[1:]

                    except Exception as e:
                        print('No hay delimitadores suficientes para los parametros de la función')
                else:
                    return [], proc_statement[1:]

    def check_if_num_var(string, num_var_or_num_or_var):
        # Si no es num_var exit(), no es de retornar
        return False

    def check_parameters_coincide(parameters, condition_or_command_name, condit_or_command):
        if condit_or_command == 'condition':
            real_params = conditions_dct[condition_or_command_name]

            try:
                for i in range(len(real_params)):
                    if real_params[i] == 'num_var':
                        check_if_num_var(parameters[i], 'num_var')
                    elif real_params[i] == 'condition':
                        if not parameters[i] in conditions_dct.keys():
                            print('Error5')
                            exit()

                    else:
                        if not parameters[i] in conditions_dct[condition_or_command_name][i]:
                            print('Error66')
                            exit()
                return True

            except Exception as e:
                print('Error33')
                exit()
        else:
            real_params = commands_dct[condition_or_command_name]
            try:
                for i in range(len(real_params)):
                    if real_params[i] == 'num_var':
                        check_if_num_var(parameters[i], 'num_var')
                    elif real_params[i] == 'num':
                        check_if_num_var(parameters[i], 'num')
                    elif real_params[i] == 'var':
                        check_if_num_var(parameters[i], 'var')
                    elif not i:
                        return True
                    else:
                        if not parameters[i].lower() in commands_dct[condition_or_command_name][i]:
                            print('Error6')
                            exit()
                return True

            except Exception as e:
                print('Error33')
                exit()

    def check_command(string):
        # Se le pasa el string desde el comando
        one_value = False
        string_ = string[0].lower()
        if string_ in commands_dct.keys() and string[1] == ':':
            num_valores = len(commands_dct[string_])
            if num_valores == 1:
                one_value = True
                condits = string[2:3]
            else:
                condits = string[2:3 + num_valores]
            for i in range(len(condits)):
                if i % 2 == 1 and condits[i] != ',':
                    print('Faltan comas')
                    exit()

            cad = "".join(condits)
            parameters = cad.split(",")
            if not check_parameters_coincide(parameters, string_.lower(), 'command'):
                print("Los tipos de los argumentos no coinciden con los especificados")
            if not one_value:
                return string[3 + num_valores:]
            else:
                return string[3:]
        else:
            print(string)
            print('Error 65')
            exit()

    def check_condition(string):
        # Se le pasa el string desde la condición
        one_value = False
        string_ = string[0].lower()
        if string_ in conditions_dct.keys() and ":" in string:
            num_valores = len(conditions_dct[string_])
            if num_valores == 1:
                one_value = True
                condits = string[2:3]
            else:
                condits = string[2:3 + num_valores]
            for i in range(len(condits)):
                if i % 2 == 1 and condits[i] != ',':
                    print('Faltan comas')
                    exit()

            cad = "".join(condits)
            parameters = cad.split(",")
            if not check_parameters_coincide(parameters, string_.lower(), 'condition'):
                print("Los tipos de los argumentos no coinciden con los especificados")
        if not one_value:
            return string[3 + num_valores:]
        else:
            return string[3:]

    def delimit_command(string):
        index = list(string).index("[")
        lst = string[index:]
        open_bracks = 0
        closed_bracks = 0

        for i in range(len(lst)):

            if lst[i] == '[':
                open_bracks += 1
            elif lst[i] == ']':
                closed_bracks += 1

            elif open_bracks == closed_bracks:
                return (string[index:i], string[i:])

    def check_if_valid_block(string):
        if string:
            try:
                if string[0] == "," or string[0] == ";" or not string[0]:
                    if string[0] == ";" and string[1] != 'while' and string[1] != 'repeat' and string[1] != 'nop' and string[1] != 'if':
                        print('POSIBLE ERROR')
                    string.pop(0)

                    if string[1] == "," or string[1] == ";" or not string[1]:
                        string.pop(1)

            except Exception as e:
                pass

            cad_ = next(s.strip().lower() for s in string if s)
            print(string)

            if cad_ in commands_dct.keys():
                nw = check_command(string)
                check_if_valid_block(nw[1:])

            elif cad_ in control_structure:
                if cad_ == 'if':
                    if not (string[1] == ':'):
                        print('Error1')
                        exit()
                    else:
                        nw_cad = check_condition(string[2:])
                    if not (nw_cad[0] == 'then' and nw_cad[1] == ':' and nw_cad[2] == '['):
                        print('Error21')
                        exit()
                    else:
                        check_if_valid_block(nw_cad)
                elif cad_ == 'then':
                    commands_to_analyze = delimit_command(string[2:])
                    check_if_valid_block(commands_to_analyze[0][1:-1])
                    check_if_valid_block(commands_to_analyze[1])
                elif cad_ == 'else':
                    if not (string[1] == ':'):
                        print('Error1')
                        exit()
                    else:
                        commands_to_analyze = delimit_command(string[2:])
                        check_if_valid_block(commands_to_analyze[0][1:-1])
                        check_if_valid_block(commands_to_analyze[1][1:])

                elif cad_ == 'while':
                    if not (string[1] == ':'):
                        print('Error1')
                        exit()
                    else:
                        nw_cad = check_condition(string[2:])

                    if not (nw_cad[0] == 'do' and nw_cad[1] == ':' and nw_cad[2] == '['):
                        print('Error21')
                        exit()
                    else:
                        commands_to_analyze = delimit_command(string[2:])
                        check_if_valid_block(commands_to_analyze[0][1:-1])
                        check_if_valid_block(commands_to_analyze[1][1:])

                elif cad_ == 'do':
                    if not (string[1] == ':' and string[2] == '['):
                        print('Error1')
                        exit()
                    else:
                        commands_to_analyze = delimit_command(string[2:])
                        check_if_valid_block(commands_to_analyze[0][1:-1])
                        check_if_valid_block(commands_to_analyze[1][1:])
                elif cad_ == 'repeat':
                    if not (string[1] == ':'):
                        print('Error1')
                        exit()
                    else:
                        commands_to_analyze = delimit_command(string[2:])
                        check_if_valid_block(commands_to_analyze[0][1:-1])
                        check_if_valid_block(commands_to_analyze[1][1:])

    def get_previous_token(lst, index):
        try:
            return lst[index - 1]
        except Exception as e:
            print('Error57')
            exit()

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

    run_script()


everything()
