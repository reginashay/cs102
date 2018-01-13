def encrypt_caesar(plaintext):
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("0123456")
    '0123456'
    >>> encrypt_caesar("@#^&*${}><~?")
    '@#^&*${}><~?'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    de = 26
    i = 3
    for c in plaintext:
        if (68 <= ord(c)+i <= 90) or (100 <= ord(c)+i <= 122):
            ciphertext += chr(ord(c)+i)
        elif (ord(c) <= 64) or (91 <= ord(c) <= 96) or (123 <= ord(c)):
            ciphertext += chr(ord(c))
        else:
            ciphertext += chr(ord(c)+i-de)
    return ciphertext


def decrypt_caesar(ciphertext):
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("0123456")
    '0123456'
    >>> decrypt_caesar("@#^&*${}><~?")
    '@#^&*${}><~?'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    de = 26
    i = 3
    for c in ciphertext:
        if (65 <= ord(c)-i <= 87) or (97 <= ord(c)-i <= 119):
            plaintext += chr(ord(c)-i)
        elif (ord(c) <= 64) or (91 <= ord(c) <= 96) or (123 <= ord(c)):
            plaintext += chr(ord(c))
        else:
            plaintext += chr(ord(c)-i+de)
    return plaintext
