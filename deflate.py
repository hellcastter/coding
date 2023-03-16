"Compression algorithm: DEFLATE"

import heapq
from math import ceil
from os import path

DICTIONARY = dict[str, str]


class LZ77:
    """
    Lempel-Ziv algorithm.
    """
    def compress(self, message: str, buffer_size: int = 5) -> list[tuple]:
        """
        Compressing message with lz77 algorithm.

        Args:
            message (str): message to compress
            buffer_size (int): size of the buffer (default 5)

        Returns:
            list[tuple[int, int, str]]: compressed message
            (list of tuples with three elements: <offset, lenght, next>)

        >>> lz77 = LZ77()
        >>> lz77.compress('abacabacabadaca')
        [(0, 0, 'a'), (0, 0, 'b'), (2, 1, 'c'), (4, 7, 'd'), (2, 1, 'c'), (2, 1, None)]
        """
        if not all([isinstance(message, str), isinstance(buffer_size, int)]):
            return None
        result = []
        buffer = ''
        ind = 0
        while ind < len(message):
            start = ind
            copy_buff = buffer
            while message[start : ind + 1] in buffer and ind != len(message):
                ind += 1
                if message[start : ind + 1] not in buffer:
                    buffer *= 2
            ext_buff = buffer
            buffer = copy_buff
            i = ind + 1
            # finding offset
            substr = message[start : i]
            copy_substr = substr[:-1]
            while substr not in buffer:
                i -= 1
                substr = message[start : i]
            offset = 0 if len(substr) == 0 else buffer.rfind(substr)
            if len(substr) != 0:
                offset = len(buffer) - offset
            if offset != 0:
                while copy_substr != ext_buff[
                    len(buffer) - offset : len(buffer) - offset + len(copy_substr)]:
                    offset -= 1
            # getting the next symbol
            if len(message[start : ind + 1]) == ind - start:
                next_sym = None
            else:
                next_sym = message[start : ind + 1][-1]
            # forming tuples
            result.append((offset, len(message[start : ind]), next_sym))
            # updating buffer
            buffer += message[start : ind + 1]
            buffer = buffer[-buffer_size:] if len(buffer) > 5 else buffer
            ind += 1
        return result


    @staticmethod
    def decompress(encoded_message: list[tuple], buffer_size: int = 5) -> str:
        """
        Decompressing encoded message.

        Args:
            encoded_message (list[tuple]): encoded message

        Returns:
            str: decoded string

        >>> lz77 = LZ77()
        >>> lz77.decompress([(0, 0, 'a'), (0, 0, 'b'), (2, 1, 'c'), \
(4, 7, 'd'), (2, 1, 'c'), (2, 1, None)])
        'abacabacabadaca'
        """
        if not isinstance(encoded_message, list) or not isinstance(buffer_size, int):
            return None
        if not all(len(i) == 3 and isinstance(i, tuple) for i in encoded_message):
            return None
        if not all(isinstance(i, int) and isinstance(j, int) and
                   (z is None or isinstance(z, str)) for i, j, z in encoded_message):
            return None
        result = ''
        for offset, length, next_sym in encoded_message:
            buffer = result[-buffer_size:]
            start = len(buffer) - offset
            stop = start + length
            next_sym = '' if next_sym is None else next_sym
            if offset < length:
                result += (buffer * ceil(length/offset))[start : stop] + next_sym
            else:
                result += buffer[start : stop] + next_sym
        return result


class Huffman:
    """ Huffman algorithm """
    def encode(self, message: str) -> str:
        """encode by Huffman algorithm
        Args:
            message (str): message to encode   
        Returns:
            str: encoded message
        >>> huffman = Huffman()
        >>> huffman.encode('Lorem ipsum dolor sit.')[0]
        '1111110100011101011100010110110011100101110011100101110101010001000010101100011110'
        """
        dictionary = self.get_dictionary(message)

        # get code for every character in message
        result = "".join([dictionary[element] for element in message])
        return result, dictionary

    def get_dictionary(self, message: str) -> DICTIONARY:
        """dictionary of Huffman code
        Args:
            message (str): message to encode
        Returns:
            DICTIONARY: dictionary that was used to encode
        >>> huffman = Huffman()
        >>> huffman.get_dictionary('abacabacacabaca')
        {'b': '00', 'a': '1', 'c': '01'}
        """
        unique = set(message)
        probabilities = []

        for letter in unique:
            heapq.heappush(probabilities, [message.count(letter), 0, letter])

        # get encoding scheme and convert it to dictionary
        scheme = self.__create_scheme(probabilities)
        dictionary = {element[2]: element[1] for element in scheme}

        return dictionary

    def __create_scheme(self, probabilities):
        """
        encoding scheme
        It has to be a tree, but I decided to work with lists
        """
        # if only 1 element in string
        if len(probabilities) <= 1:
            return [[probabilities[0][0], str(probabilities[0][1]), probabilities[0][2]]]

        # if we divided it to 2 symbols
        if len(probabilities) == 2:
            first, second = probabilities
            first[1] = '0'
            second[1] = '1'
            return [first, second]

        # three and more letters
        # get 2 elements with lowest probabilities and sum them
        first_lowest = heapq.heappop(probabilities)
        second_lowest = heapq.heappop(probabilities)

        lowest_sum = first_lowest[0] + second_lowest[0]

        heapq.heappush(probabilities, [lowest_sum, 0])

        # recursively add 2 elements with lowest probabilities
        probabilities = self.__create_scheme(probabilities)

        # code for this 2-elements
        code = None
        for idx, element in enumerate(probabilities):
            # find 2-elements and delete it from heapq
            # if len(element) == 3 => that's not 2-elements, it's a character
            # with the same probability
            if element[0] == lowest_sum and len(element) < 3:
                code = element[1]
                del probabilities[idx]
                break

        # add 0 and 1 to left and right element
        first_lowest[1] = code + '0'
        second_lowest[1] = code + '1'

        heapq.heappush(probabilities, first_lowest)
        heapq.heappush(probabilities, second_lowest)

        return probabilities


    def decode(self, message: str, dictionary: DICTIONARY) -> str:
        """Decode message by Huffman algorithm
        Args:
            message (str): encoded message
            dictionary (DICTIONARY): dictionary that was created while encoding
        Returns:
            str: decoded message
        >>> huffman = Huffman()
        >>> huffman.decode('1001011001011011001011', {'b': '00', 'a': '1', 'c': '01'})
        'abacabacacabaca'
        """
        reverse_dictionary = {value: key for key, value in dictionary.items()}

        result = ""

        idx = 0

        # find a code that's in dictionary and decode it
        while idx < len(message):
            for length in range(1, len(message) + 1):
                code = message[idx : idx + length]

                if code in reverse_dictionary:
                    result += reverse_dictionary[code]
                    idx += length
                    break

        return result


class Deflate:
    """
    DEFLATE algorithm.
    """

    def deflate_encode(self, message: str, buffer_size: int = 5, to_file = False,
                       return_dict = False):
        """
        DEFLATE algorithm.

        Args:
            message (str): message to encode
            buffer_size (int): buffer size for lz77 algorithm

        Returns:
            str: encoded str

        >>> defl = Deflate()
        >>> defl.deflate_encode('Hello')
        '11010011010111011000000111'
        """
        lz77 = LZ77()
        huffman = Huffman()
        encoded_lz77 = "".join([str(offset) + str(length) + symb if symb is not None else
                                str(offset) + str(length) + ' '
                                for offset, length, symb in lz77.compress(message, buffer_size)])
        encoded_huffman, dictionary = huffman.encode(encoded_lz77)
        if to_file:
            with open('deflate.txt', 'w', encoding='utf-8') as file:
                file.write(encoded_huffman)
            return None
        if return_dict:
            return encoded_huffman, dictionary
        return encoded_huffman


    def deflate_decode(self, encoded_str: str, dictionary: DICTIONARY, buffer_size: int = 5):
        """
        Decoding deflate algorithms.

        Args:
            encoded_str (str): encode message
            buffer_size (int): buffer size for lz77 algorithm

        Returns:
            str: decoded str

        >>> defl = Deflate()
        >>> b, d = defl.deflate_encode('Hello', return_dict = True)
        >>> defl.deflate_decode(b, d)
        'Hello'
        """
        if not isinstance(encoded_str, str) or not isinstance(buffer_size, int):
            return None
        lz77 = LZ77()
        huffman = Huffman()
        decoded_huffman = huffman.decode(encoded_str, dictionary)
        list_of_tuples = [(int(decoded_huffman[i]), int(decoded_huffman[i + 1]),
                           decoded_huffman[i + 2])
                           for i in range(0, len(decoded_huffman), 3)]
        return lz77.decompress(list_of_tuples, buffer_size)


    @staticmethod
    def read_compress_file(file_path: str):
        """
        Read content from file.

        Args:
            path (str): path to the existing file

        Returns:
            list[tuple[int, int, str]]: compressed message
            (list of tuples with three elements: <offset, lenght, next>)
        """
        if not isinstance(file_path, str) or not path.exists(file_path):
            return None
        if not path.isfile(file_path):
            return None

        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        name = file_path.split('/')[-1].split('.')[0] + '_encoded'
        with open(f'{name}.txt', 'w', encoding='utf-8') as file:
            obj = Deflate()
            file.write(obj.deflate_encode(content))
        return None


if __name__ == "__main__":
    import doctest
    print(doctest.testmod())
