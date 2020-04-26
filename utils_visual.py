import matplotlib.pyplot as plt

def plot_pnl(ret, dates):
    cumret = (ret + 1).cumprod()
    fig, ax = plt.subplots(figsize = (10, 6))
    ax.plot(dates, cumret)
    ax.set_xlabel('Date')
    ax.set_ylabel('Cummulative Return')
    fig.savefig('pnl.png')