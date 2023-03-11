""" Huffman algorithm """
import heapq
from pprint import pprint

DICTIONARY = dict[str, str]

class Huffman:
    """ Huffman algorithm """
    def encode(self, message: str):
        """ encode by Huffman algorithm """
        dictionary = self.get_dictionary(message)

        # get code for every character in message
        result = "".join([dictionary[element] for element in message])
        return result

    def get_dictionary(self, message: str) -> DICTIONARY:
        """ dictionary of Huffman code """
        unique = set(message)
        probabilities = []

        for letter in unique:
            heapq.heappush(probabilities, [message.count(letter), 0, letter])

        # get encoding scheme and convert it to dictionary
        scheme = self.__create_scheme(probabilities)
        dictionary = {element[2]: element[1] for element in scheme}

        return dictionary

    def __create_scheme(self, probabilities):
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

    def assertion(self, message: str):
        """Test a string. Prints encoded message, dictionary and 
        checks weather message == decode(encode(message)).
        In case it's not — returns error.

        Args:
            message (str): test message
        """
        encoded = self.encode(message)
        print(encoded)
        dictionary = self.get_dictionary(message)
        pprint(dictionary)

        assert message == self.decode(encoded, dictionary)


if __name__ == "__main__":
    huffman = Huffman()
    huffman.assertion('this is an example of a huffman tree')
