import pandas as pd
import matplotlib.pyplot as plt
import time

def partitions(data, n):
    chunks = []
    for chunk in pd.read_csv(data, chunksize=n):
        chunks.append(chunk)
    return chunks

def quicksort(chunk, iterations=0):
    if len(chunk) <= 1:
        return chunk
    pivot = chunk[len(chunk) // 2]
    left = [x for x in chunk if x < pivot]
    middle = [x for x in chunk if x == pivot]
    right = [x for x in chunk if x > pivot]
    sorted_left, iterations = quicksort(left, iterations + 1)
    sorted_right, iterations = quicksort(right, iterations + 1)
    return quicksort(left) + middle + quicksort(right), iterations

def sorting(chunk, ascending=True):
    chunk, iterations = quicksort(chunk)
    if not ascending:
        chunk = chunk[::-1]
    return chunk, iterations, chunk[0], chunk[-1]

def execute(data, n, ascending=True):
    pd_df = pd.DataFrame(columns=["Time", "Max", "Min", "Iterations"])
    for i, partition in enumerate(partitions(data, n)):
        lst = partition["x"].tolist()
        start_time = time.time()
        sorted_lst, iterations, min_val, max_val = sorting(lst, ascending)
        end_time = time.time()
        pd_df.loc[i] = [end_time - start_time, max_val, min_val, iterations]
    return pd_df

data_file = #insert your data file path here, here is mine as an exemple:'/home/matilde/Documents/trabalhoeda/Sorting-in-python/data.csv'
max_n = 10001
n_rows = 1000
times = []
lst = []

#graph
for n in range(n_rows, max_n + 1, n_rows):
    start_time = time.time()
    execute(data_file, n)
    end_time = time.time()
    times.append(end_time - start_time)
    lst.append(n)

plt.plot(lst, times)
plt.xlabel("n")
plt.ylabel("Tempo total de execução (segundos)")
plt.show()

#testing
if __name__ == "__main__":
    chunks = partitions(data_file, 100)
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}:")
        print(chunk)
        
    pd_df = pd.read_csv(data_file)
    sorted_data = quicksort(pd_df['x'].tolist())
    result = execute(data_file, 100)
    print(result)
    lst = pd_df['x'].tolist()
    sorted_lst, iterations, min_val, max_val = sorting(lst)
    print(f"Sorted list: {sorted_lst}")
    print(f"Min value: {min_val}")
    print(f"Max value: {max_val}")
