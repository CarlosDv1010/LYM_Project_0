import re
import string

global output


def everything():
    positions_used = []
    alphabet = list(string.ascii_lowercase)
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    reserved_words = ['if', 'else', 'while', '[', ']']

    def read_file(ruta: str):
        # Función para leer el archivo y retornar una lista sin espacios innecesarios con las líneas que no son vacías

        with open(ruta) as file:
            lines = file.readlines()

        for i in range(len(lines)):
            lines[i] = lines[i].replace("\n", "")

        list = [i.strip() for i in lines if i.strip()]
        return list

    def index_content(list):
        # Recibe una lista y devuelve una tupla con el valor original y un índice

        dct = dict()

        for i in range(len(list)):
            dct[f'{i}'] = list[i]

        return dct

    def check_if_valid_name(name):
        original_name = name
        name.lower()

        if name[0] in alphabet:
            for i in name:
                if i not in alphabet and i not in digits:
                    print(f'Programa no válido. Declaración de variable errónea. Name: {original_name}')
                    exit()
            return True
        else:
            print(f'Programa no válido. Declaración de variable errónea. Name: {original_name}')
            exit()

    def check_list_by_commas(string):
        try:
            lst = string.split(',')
            lst = [i.strip().lower() for i in lst if i.strip() and check_if_valid_name(i.strip().lower())]

            return lst
        except Exception as e:
            print('Excepción', e)

    def check_vars(string):
        # Recibe un string y revisa si cumple las condiciones para se un statement VARS válido.
        # Si es válido, retorna la lista con las variables definidas en el archivo.

        if str(string[-1] == ";"):
            lst = check_list_by_commas(string[4:-1])
            return lst

        else:
            return "No hay un statement VARS válido"

    def analize_next_procedure(string):
        if '[' in string:
            str_to_analyze = string.split('[')[0].strip()
            if check_if_valid_name(str_to_analyze):
                pass

    def complete_brackets(string, lines, pos):
        count_open_brackets = string.count("[")
        count_closed_brackets = string.count("]")
        positions_used.append(pos)
        if count_open_brackets != count_closed_brackets:

            try:
                current_line = string + lines[pos + 1]
                nw_str = complete_brackets(current_line, lines, pos + 1)

                return nw_str
            except Exception as e:
                print("No hay una cadena posible donde se cierren los brackets correctamente")
                exit()
        else:
            return string

    all_separated_phrases = []

    def check_phrase(phrases: list):
        for i in phrases:
            atpos = i.find(']')

            phrase = i[:atpos]
            all_separated_phrases.append(phrase)

    def form_lines(all_lines, num_read_lines):
        # Si hay procedures, entonces forma las líneas teniendo eso en cuenta.
        # De lo contrario, lo hace solo como bloque de instrucciones.

        lines = all_lines[num_read_lines:]
        phrases = list()

        for i in range(len(lines)):
            if i not in positions_used:
                phrases.append(complete_brackets(lines[i], lines, i))

        return phrases

    def get_proc_name(phrase):
        return str(phrase).split("[")[0].strip().lower(), phrase.find('[')

    def get_proc_parameters(all_proc_content):
        return all_proc_content

    def run_script():
        # Función principal
        all_lines = read_file("programa.txt")
        if all_lines[0].upper() != 'ROBOT_R':
            return 'Programa no válido, no comienza con "ROBOT_R"'

        indexed_lines = index_content(all_lines)

        # Se presupone que hay un renglón entre el último punto y coma de VARS y la siguiente instrucción
        if all_lines[1][:4].upper() == "VARS":
            # Las variables definidas
            defined_vars = check_vars(all_lines[1])
            print(f"Hay VARS: {defined_vars}\n")

            # Caso con VARS y PROCS
            if all_lines[2][:5].upper() == "PROCS":
                # Los procs definidos con sus respectivas instrucciones y parámetros
                defined_procs = dict()
                print("Hay PROCS\n")
                phrases = form_lines(all_lines, 3)

                # Toda esta parte obtiene los PROCS válidos con su contenido
                for phrase in phrases:
                    if str(phrase[0]) in alphabet:
                        proc_name = get_proc_name(phrase)
                        name = proc_name[0]
                        if proc_name[0] not in defined_procs and check_if_valid_name(name):
                            cad = phrase[proc_name[1]:].strip()
                            defined_procs[name] = cad

                for proc_content in defined_procs.values():
                    proc_parameters = get_proc_parameters(proc_content)
                    print(proc_parameters)

    return run_script()


print(everything())
