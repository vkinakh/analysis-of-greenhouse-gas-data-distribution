"""
Import .DAT file with greenhouse gas emission data in Poland and read as pandas DataFrame.
Then build visualisation using matplotlib.pyplot.
"""
import pandas as pd
from simpledbf import Dbf5
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FormatStrFormatter

column_names = {'1A2_CO2EQ' : "Manufacturing Industries and Constructrion" ,
                '1A3_CO2EQ' : "Transport",
               '1A4B_CO2EQ' : "Residential Sector (fossil fuels)",
                'WOODCO2EQ' : "Residential Sector (wood)",
                'CO2EQ' : "Agriculture/Forestry/Fishery",
               'EO_CO2EQ' : "Total (including all above)"}


def regression_fill(arr):
    reg = []
    l = len(arr)
    for i in range(l - 1):
        reg.append(arr[i])
        t = (arr[i] + arr[i+1]) / 2
        reg.append(t)
    return reg


def create_plots(df, col, name):
    """Creates two plots in one - from min to mean and from mean to max"""
    # Prepare data for plot
    first_df = df[df[col] != 0][col]

    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    # Get some statistics
    min_val = np.min(first_df)
    max_val = np.max(first_df)
    mean_val = np.mean(first_df)

    # Create first hist
    n1, bins1, pathes = ax1.hist(first_df, 30, histtype="bar", rwidth=0.8, range=[min_val, mean_val])
    #ax1.hist(temp_df, bins=bins, histtype="bar", rwidth=0.8, color="skyblue", ec="skyblue")

    # Create line
    modeling_layer_x = regression_fill(bins1[0:len(n1)])
    modeling_layer_y = regression_fill(n1)
    modeling_layer_x = regression_fill(modeling_layer_x)
    modeling_layer_y = regression_fill(modeling_layer_y)

    # Visualisation
    ax1.plot(modeling_layer_x, modeling_layer_y)
    ax1.set_ylabel(r'$\mathregular{km^2}$')
    ax1.set_xlabel('Greenhouse gas emission in Gg/cell')
    ax1.set_xticks(bins1)
    ax1.set_xticklabels(bins1, rotation=85)
    ax1.xaxis.set_major_formatter(FormatStrFormatter('%.3f'))
    ax1.set_title(name)
    vals = ax1.get_yticks()
    ax1.set_yticklabels(['{}'.format(int(x * 4)) for x in vals])

    # Prepare data for second hist
    second_df = df[df[col] >= mean_val][col]
    # Prepare second bins
    diff = (max_val - mean_val) / 30
    m = mean_val
    b = []
    while m <= max_val:
        b.append(m)
        m += diff

    # Create second plot
    n2, bins2, pathes = ax2.hist(second_df, bins=b, histtype="bar", rwidth=0.8)

    # Create line
    modeling_layer_x = regression_fill(bins2[0:len(n2)])
    modeling_layer_y = regression_fill(n2)
    modeling_layer_x = regression_fill(modeling_layer_x)
    modeling_layer_y = regression_fill(modeling_layer_y)

    # Visualisation
    ax2.plot(modeling_layer_x, modeling_layer_y)
    ax2.set_ylabel(r'$\mathregular{km^2}$')
    ax2.set_xlabel('Greenhouse gas emission in Gg/cell')
    ax2.set_xticklabels(bins2,rotation=85)
    ax2.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    vals = ax2.get_yticks()
    ax2.set_yticklabels(['{}'.format(int(x * 0.4)) for x in vals])

    fig.tight_layout()
    plt.savefig(str(col) + ".png", dpi=300)


def create_plot(df, col):
    """Creates bar chart for this column"""
    # Create df for this column
    temp_df = df[df[col] != 0][col]

    # Create bins for chart
    # Find min and max for limits
    min_val = np.min(temp_df)
    max_val = np.max(temp_df)
    # For better visualisation
    max_val /= 5
    mean_val = np.mean(temp_df)

    # Find difference for steps
    diff = max_val - min_val

    # Find step
    step = diff / 5

    # Create list of bins
    bins = []
    while min_val <= max_val:
        bins.append(min_val)
        min_val += step

    fig, ax = plt.subplots()
    n, bins, pathes = ax.hist(temp_df, bins = bins, histtype = "bar", rwidth = 0.8)
    ax.hist(temp_df, bins= bins, histtype= "bar", rwidth=0.8,color = "skyblue", ec="skyblue")

    # Create spare points
    modeling_layer_x = regression_fill(bins[0:len(n)])
    modeling_layer_y = regression_fill(n)
    modeling_layer_x = regression_fill(modeling_layer_x)
    modeling_layer_y = regression_fill(modeling_layer_y)

    # Visualisation
    ax.plot(modeling_layer_x, modeling_layer_y)
    ax.set_ylabel('Number of cells')
    ax.set_xlabel('Greenhouse gas emission ')
    plt.xticks(bins, rotation = 85)
    ax.set_title(col)
    fig.tight_layout()
    plt.savefig(str(col) + '.png')



dbf = Dbf5('Energy_GHG_emissions_region.dbf')
df = dbf.to_dataframe()



if __name__ == "__main__":
    for key, value in column_names.items():
        create_plots(df, key , value)




