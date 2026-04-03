class HashTableError(Exception):
    pass


class InvalidKeyError(HashTableError):
    pass


class DuplicateKeyError(HashTableError):
    pass


class TableOverflowError(HashTableError):
    pass


class RecordNotFoundError(HashTableError):
    pass