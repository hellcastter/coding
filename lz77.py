"Lempel-Ziv algorithm"
from math import ceil

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
            buffer = copy_buff
            i = ind + 1
            # finding offset
            substr = message[start : i]
            while substr not in buffer:
                substr = message[start : i]
                i -= 1
            offset = 0 if len(substr) == 0 else buffer.rfind(substr)
            if len(substr) != 0:
                offset = len(buffer) - offset
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
                   isinstance(z, None | str) for i, j, z in encoded_message):
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


    def assertion(self, message: str) -> bool:
        """
        Assert an initial message is equal to the encoded an decoded one.

        Args:
            message (str): message to check the correctness

        Returns:
            bool: True if they are equal, False otherwise.

        >>> lz77 = LZ77()
        >>> lz77.assertion('abacabacabadaca')
        True
        """
        if not isinstance(message, str):
            return None
        obj = LZ77()
        encoded = obj.compress(message)
        return message == obj.decompress(encoded)


if __name__ == "__main__":
    import doctest
    print(doctest.testmod())
