import pandas as pd
import os


"""
Functionality for Chapter 01.Data Source and Information about Provider.
"""

def move_files_into_one_dir(archive_path: str) -> None:
    """
    Moves all the files that are in a nested directory up to be in on the same level. And deletes empty directories.
    """
    if not os.path.isdir(archive_path+ "/UkraineWar") or not os.path.isdir(archive_path+ "/UkraineWar/UkraineWar"):
        raise FileNotFoundError("Archive doesnt have expected structure")
    for file in os.listdir(archive_path + "/UkraineWar/UkraineWar"):
        os.rename(archive_path + "/UkraineWar/UkraineWar/"+file, archive_path+"/" + file)
    os.rmdir(archive_path+ "/UkraineWar/UkraineWar")
    os.rmdir(archive_path+ "/UkraineWar")
        

def split_csv_by_date(data_path: str) -> None:
    """
    Splits csv files in data_path that span multiple days into single files, one for each day. Then removes the old csvs.
    """
    if not data_path[-1] == "/":
        data_path = data_path + "/"
    for path in [data_path+x for x in sorted(os.listdir(data_path)) if "to" in x and ".csv" in x]:
        df = pd.read_csv(path)
        df['date'] = df['tweetcreatedts'].apply(lambda x: x[:10])
        dfs = {"".join(date.split('-')) + '_UkraineCombinedTweetsDeduped.csv' : df[df['date']==date] for date in df['date'].unique() }
        for name,df_date  in dfs.items():
            df_date.to_csv(data_path + name)
    for path in [data_path+x for x in sorted(os.listdir(data_path)) if "to" in x]:
        os.remove(path)        

def merge_splitted_files(data_path: str) -> None:
    """
    Files for Feb28 are splitted into two parts. Merges them into one.
    """
    if not data_path[-1] == "/":
        data_path = data_path + "/"
    if not "UkraineCombinedTweetsDeduped_FEB28_part2.csv" in os.listdir(data_path) or not "UkraineCombinedTweetsDeduped_FEB28_part1.csv" in os.listdir(data_path):#
        raise FileNotFoundError("Files to merge not found")
    df_1 = pd.read_csv(data_path+"UkraineCombinedTweetsDeduped_FEB28_part1.csv")#
    df_2 = pd.read_csv(data_path+"UkraineCombinedTweetsDeduped_FEB28_part2.csv")
    df = pd.concat([df_1,df_1])
    df.to_csv("UkraineCombinedTweetsDeduped_FEB28.csv")
    os.remove(data_path+"UkraineCombinedTweetsDeduped_FEB28_part1.csv")
    os.remove(data_path+"UkraineCombinedTweetsDeduped_FEB28_part2.csv")

def rename_files(data_path: str) -> None:
    """
    Renames files to YYYYMMDD.csv.
    """
    if not data_path[-1] == "/":
        data_path = data_path + "/"
    for file in os.listdir(data_path):
        if not "Ukraine" in file:
            continue
        df = pd.read_csv(data_path + file,lineterminator='\n')
        name = df.iloc[0]['tweetcreatedts'][:10]
        name = "".join(name.split('-'))
        os.rename(data_path + file, data_path + name + ".csv")

def print_folder_stats(data_path: str) ->  None:
    """
    Prints some information about the number of files, their size and so on.
    """ 
    print(f"Number of files: {len(os.listdir(data_path))}")
    print(f"First date: {sorted(os.listdir(data_path))[0]}, Last date: {sorted(os.listdir(data_path))[-1]}")
    files = [os.stat(data_path+"/" + path).st_size/ (1024 * 1024) for path in  os.listdir(data_path)]
    print(f"Average file size: {sum(files)/len(files) :4.4} in mb")


import matplotlib.pyplot as plt

def plot_file_sizes(data_path: str, save_path: str = None) -> None:
    """
    Plots the sizes of csv files in path.
    """
    plt.rcParams['figure.figsize'] = [10, 5]
    file_sizes = [os.stat(data_path+"/" + path).st_size/ (1024 * 1024) for path in  os.listdir(data_path)]
    file_names = [x.split('.')[0] for x in os.listdir(data_path)]
    
    files = sorted(zip(file_sizes,file_names),key= lambda x:x[1])
    
    Y = [x[0] for x in files]
    X = [x[1] for x in files]
    fig, ax = plt.subplots()
    
    
    ax.plot(X,Y)
    _ = [l.set_visible(False) for (i,l) in enumerate(ax.xaxis.get_ticklabels()) if i % 50 != 0]
    ax.set_title("Files size of csvs over time")
    ax.set_ylabel('File size in mb')

    if save_path:
        plt.savefig(save_path)
    plt.show()
    
    plt.rcParams['figure.figsize'] = [20, 10]