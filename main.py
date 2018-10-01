from oracle import *
import sys


def get_data():
    """ This function will check if it is possible to read in a file.
        If it is, do so and return the found string (stripped of any
        newline characters) to the main() function.
        If the file cannot be found or was not provided, use hardcoded
        string instead.
    """
    if len(sys.argv) < 2:
        print "Defaulting to hardcoded string."
        data = "I, the server, hereby agree that I will pay $100 to this student"
    else:
        try:
            f = open(sys.argv[1])
            data = f.read()
            f.close()
        except IOError:
            print "File: " + sys.argv[1] + " could not be found."
            data = "I, the server, hereby agree that I will pay $100 to this student"
            print "Defaulting to hardcoded string."

    return data.strip('\n')


def main():
    """ This function will forge a valid tag for the 2-block (32 byte)
        message which consists of the first 32 characters from the message in
        returned by get_data().

        We proceeded as follows:
        - This string's tag can then be found by xor'ing the result
          from the first tag we found with the data in the second range
          of the data.
        - The third range of the data just gets appended to the xor'd data.
        - We find the new tag for the newly acquired data.
        - We try to verify the newly found data. This succeeds for the data
          we provided it by default.
    """

    data = get_data()
    len_message = 32 # Length of the small message from which we forge a tag.

    Oracle_Connect()

    # Define ranges.
    data_1st_range = data[0:32]
    data_2nd_range = data[32:48]
    data_3rd_range = data[48:64]

    # Retrieve tag for the first 32 characters of the data string.
    tag = str(Mac(data_1st_range, len_message))
    len_tag = len(tag)

    # Initialize the xored-data string.
    xored_data = ''

    # XOR the data from found tag with that of the data in the second range.
    # This range is determined by looking at the size for the tag, which was 16 bytes.
    for i in range(len_tag):
        xored_data += chr(ord(tag[i]) ^ ord(data_2nd_range[i]))

    # Concatenate the final bit of data from the message to the xored-data.
    xored_data = xored_data + data_3rd_range

    # Get new tag for the data that we just xor'ed.
    tag = Mac(xored_data, len_message)
    # Try to get verification for this newly found tag.
    ret = Vrfy(data, len(data), tag)

    print
    print ret

    if (ret == 1):
        print("Message verified successfully!")
    else:
        print("Message verification failed.")

    Oracle_Disconnect()

if __name__ == "__main__":
    main()
