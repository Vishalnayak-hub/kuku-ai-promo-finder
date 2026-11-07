
import pandas as pd

files = [
    "outputs/screenplay_blocks_v2.csv",
    "outputs/promo_candidates_refined.csv"
]

for file in files:
    df = pd.read_csv(file)

    print("\n" + "=" * 60)
    print("FILE:", file)
    print("SHAPE:", df.shape)

    print("\nCOLUMNS:")
    print(df.columns.tolist())

    print("\nFIRST TWO ROWS:")
    print(df.head(2).to_string(index=False))

    print("\nDATA TYPES:")
    print(df.dtypes)
