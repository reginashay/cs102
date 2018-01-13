def encrypt_vigenere(plaintext, keyword):
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    >>> encrypt_vigenere("0123456", "!@#$%^")
    '0123456'
    >>> encrypt_vigenere("{}[]&*?", '987654')
    '{}[]&*?'
    """
    alp1 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alp2 = "abcdefghijklmnopqrstuvwxyz"

    while len(keyword) < len(plaintext):
        keyword += keyword

    ciphertext = ""
    de = 26
    for c in range(len(plaintext)):
        wc = ord(plaintext[c])

        if keyword[c] in alp1:
            kind = ord(keyword[c]) - 65
        elif keyword[c] in alp2:
            kind = ord(keyword[c]) - 97

        if (65 <= wc <= 90) and (65 <= kind + wc <= 90):
            ciphertext += chr(wc + kind)
        elif (97 <= wc <= 122) and (97 <= kind + wc <= 122):
            ciphertext += chr(wc + kind)
        elif (wc <= 64) or (91 <= wc <= 96) or (123 <= wc):
            ciphertext += chr(wc)
        else:
            ciphertext += chr(wc + kind - de)

    return ciphertext


def decrypt_vigenere(ciphertext, keyword):
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    # PUT YOUR CODE HERE
    return plaintext
