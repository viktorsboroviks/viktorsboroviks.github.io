'''Generate example tables and diagrams.'''
# pylint: disable=invalid-name
import csv
import matplotlib.pyplot as plt
import numpy as np
import nice_colors


def eq_gain(loss):
    '''Equivalent gain for a given loss (%).'''
    return (1/(1. - abs(loss/100.)) - 1) * 100


def total_loss(osc):
    '''Total loss after oscillation of a relative value (%).'''
    return (osc/100.)**2 * 100


def create_csv(data, column_names, filename):
    '''Create .csv table.'''
    with open(filename, 'w', encoding='UTF-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(column_names)
        for row in data:
            formatted_row = [f'{value:.2f}' for value in row]
            writer.writerow(formatted_row)


def gen_osc(amplitude, num, direction='increase'):
    '''Generate arrays for x,y to display oscillation of price,
       starting with 100%.'''
    x = [0]
    y = [100.]
    for _ in range(num):
        if direction == 'increase':
            y.append(y[-1] * (1 + amplitude/100.))
            y.append(y[-1] * (1 - amplitude/100.))
        else:
            y.append(y[-1] * (1 - amplitude/100.))
            y.append(y[-1] * (1 + amplitude/100.))
        x.append(x[-1] + 0.5)
        x.append(x[-1] + 0.5)
    return x, y


TABLE1_NAME = 'abs_change.csv'
TABLE1_COLUMNS = ['Loss (%)', 'Gain to break even (%)', 'Gain/Loss ratio']
TABLE1_LOSSES = [0.1, 0.2, 0.5,
                 1, 2, 5,
                 10, 20, 50,
                 75, 90, 99]


def create_table1():
    '''Create a .csv table for equivalent gains.'''
    def generate_data():
        data = []
        for loss in TABLE1_LOSSES:
            data.append([loss,
                         eq_gain(loss),
                         eq_gain(loss)/loss])
        return data

    create_csv(generate_data(), TABLE1_COLUMNS, TABLE1_NAME)


TABLE2_NAME = 'rel_change.csv'
TABLE2_COLUMNS = ['Price oscillation (%)', 'Resulting loss (%)']
TABLE2_OSC = [0.1, 0.2, 0.5,
              1, 2, 5,
              10, 20, 50,
              75, 90, 99]


def create_table2():
    '''Create a .csv table for total losses after oscillation.'''
    def generate_data():
        data = []
        for osc in TABLE2_OSC:
            data.append([osc,
                         total_loss(osc)])
        return data

    create_csv(generate_data(), TABLE2_COLUMNS, TABLE2_NAME)


FIG12_LOSS_MIN = 0.1


def create_fig_abs_change_rate(filename, loss_max):
    '''Create figure for losses/equivalent relative gains.'''
    # 100 linearly spaced numbers
    x = np.linspace(FIG12_LOSS_MIN, loss_max, 100)
    y = eq_gain(x)

    fig = plt.figure(figsize=(2, 1.5))
    ax = fig.subplots(1, 1)

    # set style for spines
    ax.spines['left'].set_position(('data', 0))
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    # plot the main line
    ax.plot(x, y, color=nice_colors.BLUE)

    # show the 1-to-1 ratio
    ax.plot([0, loss_max], [0, loss_max],
            color=nice_colors.RED,
            linestyle='dashed')

    ax.set_xlabel('Losses (%)')
    ax.set_ylabel('Gains to break even (%)')

    fig.savefig(filename)


FIG34_OSC_MIN = 0


def create_fig_rel_change_rate(filename, osc_max):
    '''Create figure for total losses after oscillation of value.'''
    # 100 linearly spaced numbers
    x = np.linspace(FIG34_OSC_MIN, osc_max, 100)
    y = total_loss(x)

    fig = plt.figure(figsize=(2, 1.5))
    ax = fig.subplots(1, 1)

    # set style for spines
    ax.spines['left'].set_position(('data', 0))
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    # plot the main line
    ax.plot(x, y, color=nice_colors.BLUE)

    ax.set_xlabel('Oscillation (%)')
    ax.set_ylabel('Resulting loss (%)')

    fig.savefig(filename)


def create_fig_osc(filename, figsize, amplitude, num, direction):
    '''Create figure for price oscillation over some period.'''
    # 100 linearly spaced numbers
    x, y = gen_osc(amplitude, num, direction=direction)

    fig = plt.figure(figsize=figsize)
    ax = fig.subplots(1, 1)

    # set style for spines
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    # plot the main line
    ax.plot(x, y, color=nice_colors.BLUE)

    ax.set_xlabel('Iterations')
    ax.set_ylabel('Price (%)')

    fig.savefig(filename)


FIG1_LOSS_MAX = 20
FIG1_NAME = 'abs_change_rate1.svg'
FIG2_LOSS_MAX = 99
FIG2_NAME = 'abs_change_rate2.svg'
FIG3_OSC_MAX = 1
FIG3_NAME = 'rel_change_rate1.svg'
FIG4_OSC_MAX = 100
FIG4_NAME = 'rel_change_rate2.svg'
FIG5_AMP = 10
FIG5_N = 6
FIG5_DIR = 'increase'
FIG5_SIZE = (2, 1.5)
FIG5_NAME = 'rel_osc_inc.svg'
FIG6_AMP = 10
FIG6_N = 6
FIG6_DIR = 'decrease'
FIG6_SIZE = (2, 1.5)
FIG6_NAME = 'rel_osc_dec.svg'
FIG7_AMP = 10
FIG7_N = 150
FIG7_DIR = 'increase'
FIG7_SIZE = (5, 1.5)
FIG7_NAME = 'rel_osc_inc_n150.svg'


def main():
    '''Main.'''
    create_table1()
    create_table2()
    create_fig_abs_change_rate(FIG1_NAME, FIG1_LOSS_MAX)
    create_fig_abs_change_rate(FIG2_NAME, FIG2_LOSS_MAX)
    create_fig_rel_change_rate(FIG3_NAME, FIG3_OSC_MAX)
    create_fig_rel_change_rate(FIG4_NAME, FIG4_OSC_MAX)
    create_fig_osc(FIG5_NAME, FIG5_SIZE, FIG5_AMP, FIG5_N, FIG5_DIR)
    create_fig_osc(FIG6_NAME, FIG6_SIZE, FIG6_AMP, FIG6_N, FIG6_DIR)
    create_fig_osc(FIG7_NAME, FIG7_SIZE, FIG7_AMP, FIG7_N, FIG7_DIR)


if __name__ == "__main__":
    main()
