""" Huffman algorithm """
import heapq
from pprint import pprint

DICTIONARY = dict[str, str]

class Huffman:
    """ Huffman algorithm """
    def encode(self, message: str):
        """ encode by Huffman """
        dictionary = self.get_dictionary(message)

        result = "".join([dictionary[element] for element in message])
        return result

    def get_dictionary(self, message: str) -> DICTIONARY:
        """ dictionary of Huffman code """
        unique = set(message)
        probabilities = []

        for letter in unique:
            heapq.heappush(probabilities, [message.count(letter), 0, letter])

        scheme = self.__create_scheme(probabilities)
        dictionary = {element[2]: element[1] for element in scheme}

        return dictionary

    def __create_scheme(self, probabilities):
        if len(probabilities) <= 1:
            return [[probabilities[0][0], str(probabilities[0][1]), probabilities[0][2]]]

        if len(probabilities) == 2:
            first, second = probabilities
            first[1] = '0'
            second[1] = '1'
            return [first, second]

        first_lowest = heapq.heappop(probabilities)
        second_lowest = heapq.heappop(probabilities)

        lowest_sum = first_lowest[0] + second_lowest[0]

        heapq.heappush(probabilities, [lowest_sum, 0])
        probabilities = self.__create_scheme(probabilities)

        code = None
        for idx, element in enumerate(probabilities):
            if element[0] == lowest_sum and len(element) < 3:
                code = element[1]
                del probabilities[idx]
                break

        first_lowest[1] = code + '0'
        second_lowest[1] = code + '1'

        heapq.heappush(probabilities, first_lowest)
        heapq.heappush(probabilities, second_lowest)

        return probabilities

    def decode(self, message: str, dictionary: DICTIONARY) -> str:
        reverse_dictionary = {value: key for key, value in dictionary.items()}

        result = ""

        idx = 0
        while idx < len(message):
            for length in range(1, len(message) + 1):
                element = message[idx : idx + length]

                if element in reverse_dictionary:
                    result += reverse_dictionary[element]
                    idx += length
                    break

        return result

    def assertion(self, message: str):
        encoded = self.encode(message)
        print(encoded)
        dictionary = self.get_dictionary(message)
        pprint(dictionary)

        assert message == self.decode(encoded, dictionary)


huffman = Huffman()
