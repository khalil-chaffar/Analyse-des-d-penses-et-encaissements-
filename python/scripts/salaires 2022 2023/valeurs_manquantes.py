import pandas as pd
import matplotlib.pyplot as plt
import missingno as msno
import seaborn as sns

def visualiser_valeurs_mq(df):
    msno.bar(df)
    plt.show(block=False)
    input("Press Enter to continue...")
