import pandas as pd


def test_sem_duplicatas_apos_upsert():
    df = pd.DataFrame({
        "data_referencia": ["2024-01-01", "2024-01-01", "2024-01-02"],
        "valor": [10.75, 10.75, 10.80]
    })

    df_sem_dup = df.drop_duplicates(subset=["data_referencia"])

    assert df_sem_dup["data_referencia"].is_unique


def test_valores_sao_numericos():
    df = pd.DataFrame({
        "valor": [10.75, 10.80, 15.01]
    })

    assert pd.api.types.is_numeric_dtype(df["valor"])