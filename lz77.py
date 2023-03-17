"Lempel-Ziv algorithm"
from math import ceil
from os import path


class LZ77:
    """
    Lempel-Ziv algorithm.
    """
    @staticmethod
    def compress(message: str, buffer_size: int = 5) -> list[tuple]:
        """
        Compressing message with lz77 algorithm.

        Args:
            message (str): message to compress
            buffer_size (int): size of the buffer (default 5)

        Returns:
            list[tuple[int, int, str]]: compressed message
            (list of tuples with three elements: <offset, length, next>)

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

            # finding the subsrting in the buffer
            while message[start : ind + 1] in buffer and ind != len(message):
                ind += 1

                # extending the buffer by two when the substring is not in it
                if message[start : ind + 1] not in buffer:
                    buffer *= 2

            # saving extended buffer to check the correctness of the offset
            ext_buff = buffer
            # returning the buffer to it's initial form if it was extended
            buffer = copy_buff
            i = ind + 1

            # finding offset
            substr = message[start : i]
            copy_substr = substr[:-1]

            # finding the substring in the buffer
            # decrementing the i by one to find the substring
            while substr not in buffer:
                i -= 1
                substr = message[start : i]

            offset = 0 if len(substr) == 0 else buffer.rfind(substr)

            if len(substr) != 0:
                offset = len(buffer) - offset

            # checking if the substring is in the extended buffer
            # to get the correct offset
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
                result += (buffer * ceil(length / offset))[start : stop] + next_sym
            else:
                result += buffer[start : stop] + next_sym

        return result


    @classmethod
    def read_compress_file(cls, file_path: str):
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
            print(f"There is not such file {file_path}")
            return None

        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        name = file_path.split('/')[-1].split('.')[0] + '_encoded'

        with open(f'{name}.txt', 'w', encoding='utf-8') as fil:
            result = []

            for offset, length, next_character in cls.compress(content):
                result.append(f"{offset}{length}{next_character or ' '}")

            fil.write("".join(result))

        return None

    @classmethod
    def assertion(cls, message: str) -> bool:
        """
        Assert an initial message is equal to the encoded an decoded one.

        Args:
            message (str): message to check the correctness

        Returns:
            bool: True if they are equal, False otherwise.

        >>> lz77 = LZ77()
        >>> lz77.assertion('abacabacabadaca')
        >>> lz77.assertion('1100101110011100101110101010001000010101100011110')
        """
        if not isinstance(message, str):
            return None

        encoded = cls.compress(message)

        assert message == cls.decompress(encoded)


if __name__ == "__main__":
    import doctest
    print(doctest.testmod())

    LZ77.assertion("abacabacabadaca")
