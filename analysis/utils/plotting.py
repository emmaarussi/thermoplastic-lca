"""Common plotting utilities for the thermoplastic LCA analysis."""

import matplotlib.pyplot as plt
import numpy as np

def setup_plot_style():
    """Set up the common plot style."""
    plt.style.use('default')
    plt.rcParams['figure.facecolor'] = 'white'
    plt.rcParams['axes.facecolor'] = 'white'

def add_value_labels(ax, bars, fmt='{:.2f}'):
    """Add value labels on top of bars."""
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                fmt.format(height),
                ha='center', va='bottom')

def setup_grid(ax, axis='y', linestyle='--', alpha=0.7):
    """Add a grid to the plot."""
    ax.grid(True, axis=axis, linestyle=linestyle, alpha=alpha)

def save_plot(fig, filename, dpi=300):
    """Save plot with common settings."""
    plt.savefig(filename,
                dpi=dpi,
                bbox_inches='tight',
                facecolor='white',
                edgecolor='none')
    plt.close()
