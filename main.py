import time
import pandas as pd
import zlib
import hashlib

class HashTable:
    class Pair:
        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.next = None

    def __init__(self, size):
        if size == 0:
            raise ValueError("Size is zero")
        self.size = size
        self.data = [None] * size

    def crc32_hash(self, key):
        if isinstance(key, str):
            key = key.encode('utf-8')
        elif isinstance(key, (int, float)):
            key = str(key).encode('utf-8')
        return zlib.crc32(key) % self.size

    def sha1_hash(self, key):
        # Преобразуем ключ в строку, чтобы он подходил для хеширования SHA-1
        key_bytes = str(key).encode('utf-8')
        # Получаем SHA-1 хеш в виде 160-битного числа
        hash_obj = hashlib.sha1(key_bytes)
        # Преобразуем его в целое число и берем остаток от деления на размер таблицы
        return int(hash_obj.hexdigest(), 16) % self.size

    def sha256_hash(self, key):
        # Преобразуем ключ в строку, чтобы он подходил для хеширования SHA-256
        key_bytes = str(key).encode('utf-8')
        # Получаем SHA-256 хеш в виде 256-битного числа
        hash_obj = hashlib.sha256(key_bytes)
        # Преобразуем его в целое число и берем остаток от деления на размер таблицы
        return int(hash_obj.hexdigest(), 16) % self.size

    def md5_hash(self, key):
        # Преобразуем ключ в строку, чтобы он подходил для хеширования MD5
        key_bytes = str(key).encode('utf-8')
        # Получаем MD5 хеш и преобразуем его в целое число
        hash_obj = hashlib.md5(key_bytes)
        # Преобразуем хеш в целое число и берём остаток от деления на размер таблицы
        return int(hash_obj.hexdigest(), 16) % self.size

    def insert_md5(self, key, value):
        index = self.md5_hash(key)
        new_pair = self.Pair(key, value)
        if self.data[index] is None:
            self.data[index] = new_pair
        else:
            current = self.data[index]
            while current.next:
                current = current.next
            current.next = new_pair

    def insert_sha256(self, key, value):
        index = self.sha256_hash(key)
        new_pair = self.Pair(key, value)
        if self.data[index] is None:
            self.data[index] = new_pair
        else:
            current = self.data[index]
            while current.next:
                current = current.next
            current.next = new_pair


    def insert_crc(self, key, value):
        index = self.crc32_hash(key)
        new_pair = self.Pair(key, value)
        if self.data[index] is None:
            self.data[index] = new_pair
        else:
            current = self.data[index]
            while current.next:
                current = current.next
            current.next = new_pair

    def insert_sha1(self, key, value):
        index = self.sha1_hash(key)
        new_pair = self.Pair(key, value)
        if self.data[index] is None:
            self.data[index] = new_pair
        else:
             current = self.data[index]
             while current.next:
                 current = current.next
             current.next = new_pair

    def search(self, key):
        index = self.crc32_hash(key)
        current = self.data[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next
        return None

    def delete(self, key):
        index = self.crc32_hash(key)
        current = self.data[index]
        prev = None
        while current:
            if current.key == key:
                if prev:
                    prev.next = current.next
                else:
                    self.data[index] = current.next
                return True
            prev = current
            current = current.next
        return False

    def count_collisions(self):
        collision_count = 0
        for entry in self.data:
            count = 0
            current = entry
            while current:
                count += 1
                current = current.next
            if count > 1:
                collision_count += 1
        return collision_count

    def display(self):
        for index, entry in enumerate(self.data):
            values = []
            current = entry
            while current:
                values.append(f"{current.key}: {current.value}")
                current = current.next
            if values:
                print(f"Index {index}: {' -> '.join(values)}")


# Загружаем данные из файла Excel
file_path = "config.txt"  # путь хранится в отдельном файле
with open(file_path, 'r') as file:
    excel_path = file.read().strip()

data_frame = pd.read_excel(excel_path)
values = data_frame.iloc[:, 3].tolist()  # Получаем значения из второго столбца
print("for int")
print("___________________________")
# Инициализация хеш-таблицы
hash_table_size = 10000
hash_table1 = HashTable(hash_table_size)
hash_table2 = HashTable(hash_table_size)
hash_table3 = HashTable(hash_table_size)
hash_table4 = HashTable(hash_table_size)

# Вставка элементов в хеш-таблицу и замер времени
start_time = time.time()
for i, value in enumerate(values):
    hash_table1.insert_crc(i, value)
insertion_time = time.time() - start_time
print(f"Time to fill crc hash table: {insertion_time:.5f} seconds")

# Подсчет количества коллизий
collisions = hash_table1.count_collisions()
print(f"Number of collisions: {collisions}")

# Вставка элементов в хеш-таблицу и замер времени
start_time = time.time()
for i, value in enumerate(values):
    hash_table2.insert_sha1(i, value)
insertion_time = time.time() - start_time
print(f"Time to fill sha1 hash table: {insertion_time:.5f} seconds")

# Подсчет количества коллизий
collisions = hash_table2.count_collisions()
print(f"Number of collisions: {collisions}")

# Вставка элементов в хеш-таблицу и замер времени
start_time = time.time()
for i, value in enumerate(values):
    hash_table3.insert_sha256(i, value)
insertion_time = time.time() - start_time
print(f"Time to fill sha256 hash table: {insertion_time:.5f} seconds")

# Подсчет количества коллизий
collisions = hash_table3.count_collisions()
print(f"Number of collisions: {collisions}")

# Вставка элементов в хеш-таблицу и замер времени
start_time = time.time()
for i, value in enumerate(values):
    hash_table4.insert_md5(i, value)
insertion_time = time.time() - start_time
print(f"Time to fill md5 hash table: {insertion_time:.5f} seconds")

# Подсчет количества коллизий
collisions = hash_table4.count_collisions()
print(f"Number of collisions: {collisions}")

print("for string")
print("__________________________")
data_frame = pd.read_excel(excel_path)
values = data_frame.iloc[:, 3].tolist()  # Получаем значения из второго столбца

hash_table_size = 10000
hash_table5 = HashTable(hash_table_size)
hash_table6 = HashTable(hash_table_size)
hash_table7 = HashTable(hash_table_size)
hash_table8 = HashTable(hash_table_size)

# Вставка элементов в хеш-таблицу и замер времени
start_time = time.time()
for i, value in enumerate(values):
    hash_table5.insert_crc(i, value)
insertion_time = time.time() - start_time
print(f"Time to fill crc hash table: {insertion_time:.5f} seconds")

# Подсчет количества коллизий
collisions = hash_table5.count_collisions()
print(f"Number of collisions: {collisions}")

# Вставка элементов в хеш-таблицу и замер времени
start_time = time.time()
for i, value in enumerate(values):
    hash_table6.insert_sha1(i, value)
insertion_time = time.time() - start_time
print(f"Time to fill sha1 hash table: {insertion_time:.5f} seconds")

# Подсчет количества коллизий
collisions = hash_table6.count_collisions()
print(f"Number of collisions: {collisions}")

# Вставка элементов в хеш-таблицу и замер времени
start_time = time.time()
for i, value in enumerate(values):
    hash_table7.insert_sha256(i, value)
insertion_time = time.time() - start_time
print(f"Time to fill sha256 hash table: {insertion_time:.5f} seconds")

# Подсчет количества коллизий
collisions = hash_table7.count_collisions()
print(f"Number of collisions: {collisions}")

# Вставка элементов в хеш-таблицу и замер времени
start_time = time.time()
for i, value in enumerate(values):
    hash_table8.insert_md5(i, value)
insertion_time = time.time() - start_time
print(f"Time to fill md5 hash table: {insertion_time:.5f} seconds")

# Подсчет количества коллизий
collisions = hash_table8.count_collisions()
print(f"Number of collisions: {collisions}")