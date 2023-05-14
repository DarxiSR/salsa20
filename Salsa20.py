class Salsa20:
    @staticmethod
    def call_rotate(input_first_rotate_number, input_second_rotate_number):
        try:
            return ((input_first_rotate_number << input_second_rotate_number) & 0xFFFFFFFF) | (input_first_rotate_number >> (int(32) - input_second_rotate_number))
        except Exception:
            raise BufferError('[-] Ошибка ротирования в call_rotate()!\n')

    def __init__(self, get_input_encryption_key, get_input_cryptographic_nonce, get_input_cryptographic_thread_position, get_input_nothing_up_my_sleeve_number):
        try:
            if len(get_input_encryption_key) != int(64):
                raise ValueError('[-] Ошибка! Ключ должен быть ровно 64 байта в кодировке UTF-8!\n')
            else:
                self.encryption_key = get_input_encryption_key # Ключ шифрование
            if len(get_input_cryptographic_nonce) != int(16):
                raise ValueError('[-] Ошибка! Одноразовое произвольное число (Nonce) должен быть ровно 16 байт в кодировке UTF-8!\n')
            else:
                self.cryptographic_nonce = get_input_cryptographic_nonce # Одноразовое произвольное число
            if len(get_input_cryptographic_thread_position) != int(16):
                raise ValueError('[-] Ошибка! Значения чисел позиции потока должны быть ровно 16 байт в кодировке UTF-8!\n')
            else:
                self.cryptographic_thread_position = get_input_cryptographic_thread_position
            if len(get_input_nothing_up_my_sleeve_number) != int(32):
                raise ValueError('[-] Ошибка! Значения чисел типа "Козырь в рукаве" должны быть ровно 32 байта в кодировке UTF-8!\n')
            else:
                self.nothing_up_my_sleeve_number = get_input_nothing_up_my_sleeve_number
        except Exception:
            raise BufferError('[-] Ошибка буффера памяти при инициализации переменных "encryption_key" и "cryptographic_nonce" в __init__!\n')
        try:
            self.salsa_20_result = []
            self.state_matrix = [] # Матрица 4x4
            self.save_state_matrix = [] # Будет использовано для реплики state_matrix
            self.cryptographic_rounds = int(20) # Раунды

            self.initial_state_matrix() # Заполняем начальное состояние матрицы

            self.cryptographic_rounds_actions()
        except Exception:
            raise BufferError('[-] Ошибка буффера памяти при инициализации переменных  в __init__!\n')

    def initial_state_matrix(self):
        try:
            self.state_matrix.append(self.little_endian_convertation(int(self.nothing_up_my_sleeve_number[int(0):int(8)], int(16)))) # Вырезаем первые 8 байт из "Козыря в рукаве" и вставляем в массив
            self.state_matrix.append(self.little_endian_convertation(int(self.encryption_key[int(0):int(8)], int(16)))) # Вырезаем первые 8 байт из ключа шифрования и вставляем в массив
            self.state_matrix.append(self.little_endian_convertation(int(self.encryption_key[int(8):int(16)], int(16)))) # Вырезаем вторые 8 байт из ключа шифрования и вставляем в массив
            self.state_matrix.append(self.little_endian_convertation(int(self.encryption_key[int(16):int(24)], int(16)))) # Вырезаем третьи 8 байт из ключа шифрования и вставляем в массив
            self.state_matrix.append(self.little_endian_convertation(int(self.encryption_key[int(24):int(32)], int(16)))) # Вырезаем четвертые 8 байт из ключа шифрования и вставляем в массив
            self.state_matrix.append(self.little_endian_convertation(int(self.nothing_up_my_sleeve_number[int(8):int(16)], int(16)))) # Вырезаем вторые 8 байт из "Козыря в рукаве" и вставляем в массив
            self.state_matrix.append(self.little_endian_convertation(int(self.cryptographic_nonce[int(0):int(8)], int(16)))) # Вырезаем первые 8 байт из одноразового произвольного числа и вставляем в массив
            self.state_matrix.append(self.little_endian_convertation(int(self.cryptographic_nonce[int(8):int(16)], int(16)))) # Вырезаем вторые 8 байт из одноразового произвольного числа и вставляем в массив
            self.state_matrix.append(self.little_endian_convertation(int(self.cryptographic_thread_position[int(0):int(8)], int(16)))) # Вырезаем первые 8 байт из номера в потоке и вставляем в массив
            self.state_matrix.append(self.little_endian_convertation(int(self.cryptographic_thread_position[int(0):int(16)], int(16)))) # Вырезаем вторые 8 байт из номера в потоке и вставляем в массив
            self.state_matrix.append(self.little_endian_convertation(int(self.nothing_up_my_sleeve_number[int(16):int(24)], int(16)))) # Вырезаем третьи 8 байт из "Козыря в рукаве" и вставляем в массив
            self.state_matrix.append(self.little_endian_convertation(int(self.encryption_key[int(32):int(40)], int(16)))) # Вырезаем пятые 8 байт из ключа шифрования и вставляем в массив
            self.state_matrix.append(self.little_endian_convertation(int(self.encryption_key[int(40):int(48)], int(16)))) # Вырезаем шестые 8 байт из ключа шифрования и вставляем в массив
            self.state_matrix.append(self.little_endian_convertation(int(self.encryption_key[int(48):int(56)], int(16)))) # Вырезаем седьмые 8 байт из ключа шифрования и вставляем в массив
            self.state_matrix.append(self.little_endian_convertation(int(self.encryption_key[int(56):int(64)], int(16)))) # Вырезаем восьмые 8 байт из ключа шифрования и вставляем в массив
            self.state_matrix.append(self.little_endian_convertation(int(self.nothing_up_my_sleeve_number[int(24):int(32)], int(16)))) # Вырезаем четвертые 8 байт из "Козыря в рукаве" и вставляем в массив

            self.save_state_matrix = self.state_matrix[:]

            print('\n=========== ДАННЫЕ ===========')
            print('Ключ шифрования:', self.encryption_key)
            print('Nonce:', self.cryptographic_nonce)
            print('Позиции блоков в потоке:', self.cryptographic_thread_position)
            print('Козырь в рукаве:', self.nothing_up_my_sleeve_number)
            print('Количество раундов:', self.cryptographic_rounds)
            print('Исходная матрица:', self.state_matrix)

        except Exception:
            raise BufferError('[-] Ошибка заполнения матрицы начального состояния в initial_state_matrix()!\n')

    def little_endian_convertation(self, input_number_to_convert): # Преобразование в порядок "от младшему байта к старшему байту (LSB-MSB)"
        try:
            get_buffer = list(range(int(4)))
            # Запись с младшего бита
            get_buffer[0] = input_number_to_convert >> int(24) & 0xFF  # 0xFF - чтобы не выйти за границу в 32 бита
            get_buffer[1] = (input_number_to_convert >> int(16)) & 0xFF
            get_buffer[2] = (input_number_to_convert >> int(8)) & 0xFF
            get_buffer[3] = input_number_to_convert & 0xFF

            get_result = get_buffer[int(0)] + 2 ** 8 * get_buffer[int(1)] + int(2) ** int(16) * get_buffer[int(2)] + int(2) ** int(24) * get_buffer[int(3)]  # 32 бита
            return get_result
        except Exception:
            raise BufferError('[-] Ошибка конвертации входных значений в little_endian()!\n')

    def cryptographic_rounds_actions(self):
        try:
            print('\n=========== РОТИРОВАНИЕ ПО РАУНДАМ ===========')
            for round_counter in range(int(0), self.cryptographic_rounds, int(2)):
                print('Раунд:', round_counter, 'Состояние матрицы: ', self.state_matrix)
                self.cryptographic_column_round()
                self.cryptographic_raw_round()

            print('\n=========== СЛОЖЕНИЕ МАТРИЦ ===========')
            for state_matrix_segment_counter in range(int(16)):
                addition_old_matrix_with_new_matrix = self.little_endian_convertation(self.state_matrix[state_matrix_segment_counter] + self.save_state_matrix[state_matrix_segment_counter])
                for result_matrix_segment_counter in range(int(7)):
                    self.salsa_20_result.append(addition_old_matrix_with_new_matrix >> (int(32) - int(4) * result_matrix_segment_counter) & 0xF)
                    print('Сегмент матрицы:', result_matrix_segment_counter, 'Значение:', self.salsa_20_result)
        except Exception:
            raise BufferError('[-] Ошибка выполнения раундов шифрования в execute_rounds!\n')

    def cryptographic_column_round(self):
        try:
            self.cryptographic_one_round_action(int(0), int(4), int(8), int(12)) # Первый столбец матрицы
            self.cryptographic_one_round_action(int(5), int(9), int(13), int(1)) # Второй столбец матрицы
            self.cryptographic_one_round_action(int(10), int(14), int(2), int(6)) # Третий столбец матрицы
            self.cryptographic_one_round_action(int(15), int(3), int(7), int(11)) # Четвертый столбец матрицы
        except Exception:
            raise BufferError('[-] Ошибка выполнения преобразования столбцов в cryptographic_column_round()!\n')

    def cryptographic_raw_round(self):
        try:
            self.cryptographic_one_round_action(int(0), int(1), int(2), int(3)) # Первая строка матрицы
            self.cryptographic_one_round_action(int(5), int(6), int(7), int(4)) # Вторая строка матрицы
            self.cryptographic_one_round_action(int(10), int(11), int(8), int(9)) # Третья строка матрицы
            self.cryptographic_one_round_action(int(15), int(12), int(13), int(14)) # Четвертая строка матрицы
        except Exception:
            raise BufferError('[-] Ошибка выполнения преобразования строк в cryptographic_column_round()!\n')

    def cryptographic_one_round_action(self, zero_input_segment, first_input_segment, second_input_segment, third_input_segment):
        try:
            self.state_matrix[first_input_segment] ^= self.call_rotate(self.state_matrix[zero_input_segment] + self.state_matrix[third_input_segment], int(7)) # 1-й сегмент (XOR)= 0 сегмент матрицы + 3 сегмент матрицы
            self.state_matrix[second_input_segment] ^= self.call_rotate(self.state_matrix[first_input_segment] + self.state_matrix[zero_input_segment], int(9)) # 2-й сегмент (XOR)= 1 сегмент матрицы + 0 сегмент матрицы
            self.state_matrix[third_input_segment] ^= self.call_rotate(self.state_matrix[first_input_segment] + self.state_matrix[second_input_segment], int(13)) # 3-й сегмент (XOR)= 1 сегмент матрицы + 2 сегмент матрицы
            self.state_matrix[zero_input_segment] ^= self.call_rotate(self.state_matrix[third_input_segment] + self.state_matrix[second_input_segment], int(18)) # 0-й сегмент (XOR)= 3 сегмент матрицы + 2 сегмент матрицы
        except Exception:
            raise BufferError('[-] Ошибка в преобразовании входных значений в one_round_action()!\n')

    def salsa_20_encryption(self, get_input_text):
        try:
            get_text_buffer = get_input_text.encode("utf-8").hex()  # Конвертация в 16-ричные значения (HEX)
            get_output_text = ""
            get_text_size = len(get_text_buffer)
            print('\n=========== ЗАПИСЬ РЕЗУЛЬТАТА ===========')
            for get_bytes_counter in range(get_text_size):
                get_output_text += format(self.salsa_20_result[get_bytes_counter] ^ int(get_text_buffer[get_bytes_counter: get_bytes_counter + int(1)], int(16)), "x")
                print('Сегмент матрицы:', get_bytes_counter, 'Значение:', get_output_text)

            print('\nЗашифрованный текст:', get_output_text)
            return get_output_text
        except Exception:
            raise BufferError('[-] Ошибка в процессе шифрования текста в salsa20_encryption()!\n')

    def salsa_20_decryption(self, get_input_text):
        try:
            get_text_size = len(get_input_text)
            get_output_text = ""

            print('\n=========== ЗАПИСЬ РЕЗУЛЬТАТА ===========')
            for get_bytes_counter in range(get_text_size):
                get_output_text += format(self.salsa_20_result[get_bytes_counter] ^ int(get_input_text[get_bytes_counter: get_bytes_counter + int(1)], int(16)), "x")
                print('Сегмент матрицы:', get_bytes_counter, 'Значение:', get_output_text)

            print('\nДешифрованный текст в прямой записи:', get_output_text, '| Дешифрованный текст в utf-8:', bytes.fromhex(get_output_text).decode('utf-8'))
            return bytes.fromhex(get_output_text).decode('utf-8')
        except Exception:
            raise BufferError('[-] Ошибка в процессе дешифрования текста в salsa_20_decryption()!\n')