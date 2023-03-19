#Implementación de sDES en Python.
import fileinput as fp

def initial_permutation(plain_text):
    # Con base en una tabla de permutaciones, cambia de posición los bits en la cadena de entrada.
    permuted_text = ""
    permutation_table = [1, 5, 2, 0, 3, 7, 4, 6]
    #P[1] = P'[0], P[5] = P'[1], P[2] = P'[2], P[0] = P'[3], P[3] = P'[4],  P[7] = P'[5], P[4] = P'[6], P[6] = P'[7]
    for i in permutation_table:
        permuted_text += plain_text[i]
    return permuted_text

def shift_left(binary_str):
    return binary_str[1:] + binary_str[0]

def shift_left2(binary_str):
    return binary_str[1:] + binary_str[0]

def shift_left3(binary_str):
    return binary_str[2:] + binary_str[:2]

def shift_left4(binary_str):
    return binary_str[2:] + binary_str[:2]

def subkeys(key):
    #Obtiene las 2 subclaves a usar en el cifrado sDES.
    perm_table = [2, 4, 1, 6, 3, 9, 0, 8, 7, 5] #Tabla de permutaciones. 
    perm_10keys = ""

    # Permuta los primeros 10 bits de la clave.
    for i in perm_table:
        perm_10keys += key[i]

    #print("Bits permutados de la clave:", perm_10keys)

    #Divide en 2 mitades de 5 bits cada una. 
    left_half = perm_10keys[:5]
    right_half = perm_10keys[5:10]

    #print("Mitades obtenidas:", left_half, right_half)

    #Round 1: mueve 1 bit a la izquierda.
    left_half = shift_left(left_half)
    right_half = shift_left2(right_half)

    #print("Mitades recorridas 1 posición a la izquierda: ", left_half, right_half)

    #Obteniendo la primera subkey.
    key1_table = [5, 2, 6, 3, 7, 4, 9, 8]
    subkey1 = ""

    keystep = left_half + right_half

    for i in key1_table:
        subkey1 += keystep[i]
    
    #print(subkey1)

    #Round 2: mueve 2 bit a la izquierda lo obtenido en el paso 3. 
    left_half = shift_left3(left_half)
    right_half = shift_left4(right_half)

    #print("Mitades recorridas 2 posiciones a la izquierda: ", left_half, right_half)

    #Obteniendo la segunda subkey.
    keystep = left_half + right_half
    subkey2 = ""

    for i in key1_table:
        subkey2 += keystep[i]

    return subkey1, subkey2

def xor(x, y):
    return '{1:0{0}b}'.format(len(x), int(x, 2) ^ int(y, 2))

def mix(subkey, left, right):
      #Implementa la función de mezcla simplificada de sDES.
      
      expansion_table = [3, 0, 1, 2, 1, 2, 3, 0] #Tabla de permutaciones. 
      expanded_block = ""

      # Expande el bloque a 8 bits con un ciclo for que asigna los bits de acuerdo al arreglo de permutaciones.
      for i in expansion_table:
            expanded_block += right[i]

      #print("Bloque expandido a 8 bits:", expanded_block)

      # XOR subclave con el bloque expandido.
      xored = xor(expanded_block, subkey)
      #print("XOR entre la subclave y el bloque:", xored)

      # Divide en 2 mitades de 4 bits.
      left_half = xored[:4]
      right_half = xored[4:]

      #print("Mitades izquierda y derecha:", left_half, right_half)

      # Definición de S-Boxes.      

      sbox_0 = {
      "00": "01",
      "01": "00",
      "02": "11",
      "03": "10",
      "10": "11",
      "11": "10",
      "12": "01",
      "13": "00",
      "20": "00",
      "21": "10",
      "22": "01",
      "23": "11",
      "30": "11",
      "31": "01",
      "32": "11",
      "33": "10"
      }

      sbox_1 = {
      "00": "00",
      "01": "01",
      "02": "10",
      "03": "11",
      "10": "10",
      "11": "00",
      "12": "01",
      "13": "11",
      "20": "11",
      "21": "00",
      "22": "01",
      "23": "00",
      "30": "10",
      "31": "01",
      "32": "00",
      "33": "11"
      }

      #Calculamos la salida con base en las S-Box en forma de diccionarios. Ej: 1011: Fila 11-3 y columna 01: 1.

      rowleft = str(int(left_half[0] + left_half[3], 2))
      columnleft = str(int(left_half[1] + left_half[2], 2))

      #print("Parámetros a la primera S-box:", rowleft+columnleft)
      
      #Obtenemos la salida consultando a los diccionarios.
      output1 = sbox_0[rowleft+columnleft]
      #print("Salida S0:", output1)

      rowright = str(int(right_half[0] + right_half[3], 2))
      columnright = str(int(right_half[1] + right_half[2], 2))

      #print("Parámetros a la segunda S-box:", rowright+columnright)

      output2 = sbox_1[rowright+columnright]
      #print("Salida S1:", output2)

      #Concatenamos los outputs y permutamos.
      output = output1+output2
      #print("Concatenación:", output)

      perm_table = [1, 3, 2, 0] #Tabla de permutaciones. 
      perm_output = ""

      # Expande el bloque a 8 bits con un ciclo for que asigna los bits de acuerdo al arreglo de permutaciones.
      for i in perm_table:
            perm_output += output[i]
      #print("Permutado:", perm_output)
      
      #print("Al XOR", perm_output, left)
      #Aplicamos XOR con la mitad izquierda:
      xorleft = xor(perm_output, left)
      #print("XOR con la izquierda:", xorleft)

      #Concatenamos con la derecha para producir el output final
      #print(right)

      return xorleft+right

def last_permutation(plain_text):
    # Con base en una tabla de permutaciones, cambia de posición los bits en la cadena de entrada.
    permuted_text = ""
    permutation_table = [3, 0, 2, 4, 6, 1, 7, 5]

    for i in permutation_table:
        permuted_text += plain_text[i]
    return permuted_text

def encrypt(key, plaintext):
    #print("Clave:", key)
    #print("Texto plano:", plaintext)

    #Paso 1
    perm_text = initial_permutation(plaintext)
    #print("Permutación del paso 1:", perm_text)
    subkey1, subkey2 = subkeys(key)
    #print("Subclaves generadas:", subkey1, subkey2)

    #Paso 2
    left_block = perm_text[:4]
    right_block = perm_text[4:8]
    step2 = mix(subkey1, left_block, right_block)
    #print("Salida del paso 2:", step2)

    #Paso 3
    lswap= step2[:4]
    rswap = step2[4:]

    swap = rswap + lswap
    #print("Salida del paso 3:", swap)

    #Paso 4
    left_block = swap[:4]
    right_block = swap[4:8]
    #print("Nuevos bloques izquierdo y derecho para el paso 4", left_block, right_block)
    step4= mix(subkey2 ,left_block, right_block)
    #print("Salida del paso 4:", step4)

    #Paso 5
    ciphered_output = last_permutation(step4)

    return ciphered_output


def decrypt(key, plaintext):
    #print("Clave:", key)
    #print("Texto plano:", plaintext)

    #Paso 1
    perm_text = initial_permutation(plaintext)
    #print("Permutación del paso 1:", perm_text)
    subkey1, subkey2 = subkeys(key)
    #print("Subclaves generadas:", subkey1, subkey2)

    #Paso 2
    left_block = perm_text[:4]
    right_block = perm_text[4:8]
    step2 = mix(subkey2, left_block, right_block)
    #print("Salida del paso 2:", step2)

    #Paso 3
    lswap= step2[:4]
    rswap = step2[4:]

    swap = rswap + lswap
    #print("Salida del paso 3:", swap)

    #Paso 4
    left_block = swap[:4]
    right_block = swap[4:8]
    #print("Nuevos bloques izquierdo y derecho para el paso 4", left_block, right_block)
    step4= mix(subkey1 ,left_block, right_block)
    #print("Salida del paso 4:", step4)

    #Paso 5
    unciphered_output = last_permutation(step4)
    #print(unciphered_output)
    return unciphered_output



#Recuperando las entradas en una lista.
inputs = []

for entrada in fp.input():
    inputs.append(entrada.strip())

mode = inputs[0]
key = inputs[1]
plaintext = inputs[2]

if (mode == 'E'):
    ciphered_output = encrypt(key, plaintext)
    print(ciphered_output)
else:
    unciphered_output = decrypt(key, plaintext)
    print(unciphered_output)