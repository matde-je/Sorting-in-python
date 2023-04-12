import pandas as pd
import matplotlib.pyplot as plt
import time

def partitions(data, n):
    chunks = []
    for chunk in pd.read_csv(data, chunksize=n):
        chunks.append(chunk)
    return chunks

def quicksort(chunk):
    if len(chunk) <= 1:
        return chunk
    pivot = chunk[len(chunk) // 2]
    left = [x for x in chunk if x < pivot]
    middle = [x for x in chunk if x == pivot]
    right = [x for x in chunk if x > pivot]
    return quicksort(left) + middle + quicksort(right)

def sorting(lst, ascending=True):
    iterations = 0
    lst = quicksort(lst)
    if not ascending:
        lst = lst[::-1]
    return lst, iterations, lst[0], lst[-1]

def execute(data, n, ascending=True):
    pd_df = pd.DataFrame(columns=["Time", "Max", "Min", "Iterations"])
    for i, partition in enumerate(partitions(data, n)):
        lst = partition["x"].tolist()
        start_time = time.time()
        sorted_lst, iterations, min_val, max_val = sorting(lst, ascending)
        end_time = time.time()
        pd_df.loc[i] = [end_time - start_time, max_val, min_val, iterations]
    return pd_df

data_file = '/home/matilde/Documents/trabalhoeda/Sorting-in-python/data.csv'
ascending = True
max_n = 10001
n_rows = 1000
times = []
lst = []

for n in range(n_rows, max_n + 1, n_rows):
    start_time = time.time()
    execute(data_file, n, ascending)
    end_time = time.time()
    times.append(end_time - start_time)
    lst.append(n)

plt.plot(lst, times)
plt.xlabel("n")
plt.ylabel("Tempo total de execução (segundos)")
plt.show()

if __name__ == "__main__":
    chunks = partitions(data_file, 100)
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}:")
        print(chunk)
        
    pd_df = pd.read_csv(data_file)
    sorted_data = quicksort(pd_df['x'].tolist())
    result = execute(data_file, 100, ascending)
    print(result)
    lst = pd_df['x'].tolist()
    sorted_lst, iterations, min_val, max_val = sorting(lst, ascending)
    print(f"Sorted list: {sorted_lst}")
    print(f"Min value: {min_val}")
    print(f"Max value: {max_val}")
