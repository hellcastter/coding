""" Lempel-Ziv-Welch module """
class LZW:
    """ LZW class """
    def compress(self, message: str) -> list[int]:
        """Compress message

        Args:
            message (str): message to compress

        Returns:
            list[int]: compressed message (list of ints)

        >>> lzw = LZW()
        >>> lzw.compress('abacabadabacacacd')
        [0, 1, 0, 2, 4, 0, 3, 8, 7, 12, 3]
        """
        # get only unique strings of length 1
        dictionary = self.get_initial_dictionary(message)
        code = []

        idx = 0
        message_length = len(message)

        # go through every letter
        while idx < message_length:
            # get str of every length
            for length in range(1, message_length + 1):
                current = message[idx : idx + length]

                # if this substr is in dictionary skip this
                if current in dictionary and idx + length <= message_length:
                    continue

                # get previous substr (without last letter)
                length -= 1
                prev = message[idx : idx + length]

                code.append(dictionary.index(prev))
                dictionary.append(current)

                idx += length
                break

        return code

    @staticmethod
    def get_initial_dictionary(message: str) -> list[str]:
        """get only unique strings of length 1. 

        Args:
            message (str): initial message

        Returns:
            list[str]: dictionary

        >>> lzw = LZW()
        >>> lzw.get_initial_dictionary('abacabadabacacacd')
        ['a', 'b', 'c', 'd']
        """
        return list(sorted(set(message)))

    @staticmethod
    def decompress(code: str, dictionary: list[str]) -> str:
        """decompress compressed message

        Args:
            code (str): code which represents message
            dictionary (list[str]): initial dictionary of message

        Returns:
            str: decoded message

        >>> lzw = LZW()
        >>> lzw.decompress([0, 1, 0, 2, 4, 0, 3, 8, 7, 12, 3], ['a', 'b', 'c', 'd'])
        'abacabadabacacacd'
        """
        message = ""

        for idx, element in enumerate(code):
            decoded = dictionary[element]
            message += decoded

            # if not out of range
            if idx + 1 >= len(code):
                break

            # if next code is in dictionary
            if code[idx + 1] < len(dictionary):
                # add to dict this decoded element + first letter of next
                dictionary.append(decoded + dictionary[code[idx + 1]][0])
            else:
                # add only this decoded and first letter of current
                dictionary.append(decoded + decoded[0])

        return message

    def assertion(self, message: str, verbose = False):
        """Checks weather message == decompress(compress(message))

        Args:
            message (str): original message
            verbose (bool, optional): full info. Defaults to True.

        >>> lzw = LZW()
        >>> lzw.assertion('abacabadabacacacd')
        """
        compressed = self.compress(message)
        dictionary = self.get_initial_dictionary(message)

        if verbose:
            print(f"Compressed: {compressed}")
            print(f"Minimal dictionary: {dictionary}")

        assert message == self.decompress(compressed, dictionary)


if __name__ == '__main__':
    lzw = LZW()
    lzw.assertion('abacabadabacacacd', True)
