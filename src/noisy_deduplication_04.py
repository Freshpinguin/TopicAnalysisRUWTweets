from src.data_schemas import OrigDataSchema
import pandas as pd
from datasketch import MinHash, MinHashLSH
from tqdm.auto import tqdm
tqdm.pandas()
from typing import Iterable

def jaccard_duplicates(df: pd.DataFrame, threshold: float=0.7, shingle_length: int=6)-> pd.Series:
    """
    Finds jaccard duplicates for texts in DataFrame format.
    """
    def jaccard_sim(set_a: set, set_b: set) -> float:
        """
        Calc jaccard sim between two sets.
        """
        intersection = set_a & set_b
        union = set_a | set_b
        return len(intersection) / len(union)

    def shingle(text:str, shingle_len: int=shingle_length) -> set[str]:
        """
        Makes shingles out of text.
        """
        return set(text[head:head + shingle_len] for head in range(0, len(text) - shingle_len))
    

    

    def query(calc_val: list, row: tuple[int,str]) -> list:
        """
        Queries in calc list for similar text.
        """
        returning_list = []
        for id, text in calc_val:
            if jaccard_sim(shingle(text, shingle_length), shingle(row[OrigDataSchema.TEXT])) > threshold:
                returning_list.append(id)
        return returning_list

    def calc_row(row: pd.Series, calc_val: list[tuple])-> list:
        """
        Queries for duplicates of pd.DataFrame row and updates calc values.
        """
        duplicated = query(calc_val=calc_val, row=row)
        if not duplicated:
            calc_val.append((row.name,row[OrigDataSchema.TEXT]))

        return duplicated
    
    calc_values = []

    return df.progress_apply(lambda row: calc_row(row, calc_values), axis=1)


def efficient_minhash_lsh(df: pd.DataFrame,threshold: float=0.7, shingle_length:int=6)-> pd.Series:
    """
    Calculates minhash_lsh similarity for each row. Iterates over row and checks if there has been a row with similiairty greater then threshold. If so, adds those id to a new column.
    """

    def shingle(text:str, shingle_len: int=shingle_length) -> set[str]:
        """
        Makes shingles out of text.
        """
        return set(text[head:head + shingle_len] for head in range(0, len(text) - shingle_len))
    
    def minhash_insert(shingles: set[str]) -> MinHash:
        """
        Calculates minhash from set of shingles.
        """
        m = MinHash(num_perm=128)
        m.update_batch([token.encode('utf-8') for token in shingles])
        return m
    
    def lsh_query(lsh_index: MinHashLSH, minhash: MinHash) -> list:
        """
        Queries lsh and returns if there have been any mathes.
        """
        return lsh_index.query(minhash)
    
    def calc_row(row: pd.Series, lsh: MinHashLSH) -> list:
        """
        Builds minhash of text in row. Queries lsh for the minhash. If result found, return true.
        Adds minhash to lsh. <-- Sideffect.
        """

        minhash = minhash_insert(shingle(row[OrigDataSchema.TEXT]))

        duplicated = lsh_query(lsh, minhash)
        if not duplicated:
            lsh.insert(row.name, minhash)

        return duplicated
    
    lsh = MinHashLSH(threshold=threshold, num_perm=128)

    return df.progress_apply(lambda row: calc_row(row, lsh), axis=1)



def _iterate_nr(iterator: Iterable, nr:int)-> Iterable:
    for _ in range(nr):
        try:
            yield next(iterator)
        except StopIteration:
            return 


def duplicates_ex(df: pd.DataFrame, row_name: str='dupl', nr: int=30) -> None:
    """
    Shows found duplicates and prints them and there corresponding duplicates as well as some statistics.
    """
    df_min = df[~df[row_name].apply(lambda x: x==[])]
    
    print(f"Duplicates found: {df_min.shape[0]}, fraction of all: {df_min.shape[0]/df.shape[0]} \n")
    for _,row in _iterate_nr(df_min.iterrows(),nr):
        
        print(row['text'])
        print(df.query(f"index=={row[row_name][0]}").iloc[0]['text'])

        print("="*200)


def save_meta_data(df: pd.DataFrame, lang:str, row_name: str='dupl', path_to_meta_data: str= "/Users/robinfeldmann/TopicAnalysisRUWTweets/Data/AggregatedData/noisy_dedupl.csv") -> None:
       meta_df = pd.read_csv(path_to_meta_data)

       df_min = df[~df[row_name].apply(lambda x: x==[])]

       duplicates = df_min.shape[0]
       duplicates_fraction = df_min.shape[0]/df.shape[0]
       example_0_0 = df_min.iloc[0]['text']
       example_0_1 = df.query(f"index=={df_min.iloc[0][row_name][0]}").iloc[0]['text']

       example_1_0 = df_min.iloc[1]['text']
       example_1_1 = df.query(f"index=={df_min.iloc[1][row_name][0]}").iloc[0]['text']

       example_2_0 = df_min.iloc[2]['text']
       example_2_1 = df.query(f"index=={df_min.iloc[2][row_name][0]}").iloc[0]['text']


       row = {'duplicates': duplicates,
              'old_lines': df.shape[0],
              'duplicates_fraction': duplicates_fraction,
              'lang': lang,
              'ex_0_0': example_0_0,
              'ex_0_1': example_0_1,
              'ex_1_0': example_1_0,
              'ex_1_1': example_1_1,
              'ex_2_0': example_2_0,
              'ex_2_1': example_2_1
              }

       pd.concat([meta_df, pd.DataFrame([row])]).to_csv(path_to_meta_data)



def load_dedupl_save_pipeline(source_path: str, target_path: str):
    df = pd.read_csv(source_path)
    df = df.drop_duplicates(subset=OrigDataSchema.ID)
    df = df[[OrigDataSchema.TEXT,OrigDataSchema.TIMESTAMP,OrigDataSchema.ID]]

    df['dupl'] = efficient_minhash_lsh(df, shingle_length=6, threshold=0.7)

    lang = source_path.split('/')[-1].split('.')[0]

    save_meta_data(df, lang=lang)
    duplicates_ex(df, nr=0)


    df[df['dupl'].apply(lambda x: x==[])].to_csv(target_path)