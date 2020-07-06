import matplotlib.pyplot as plt


def create_scatter_for_rank(rank: int, point_list: list):
    x = list()
    y = list()
    for point in point_list:
        if point.get('elo') / 100 == rank or rank == -1:
            x.append(point.get('elo'))
            y.append(point.get('emv'))
    plt.scatter(x, y)
    path = (str(rank), "full_set")[rank == -1]
    plt.savefig("../results/R" + path + ".png")
