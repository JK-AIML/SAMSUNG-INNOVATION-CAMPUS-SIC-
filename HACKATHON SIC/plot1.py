import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Data from the provided information
locations = ['MG Road', 'Silk Board Junction']
traffic_volume = [1002.6, 1018.4]  # vehicles/hour
average_speed = [55.0, 54.9]  # km/h
accident_count = [9, 11]

# Create a DataFrame for easy plotting
data = pd.DataFrame({
    'Location': locations,
    'Average Traffic Volume (vehicles/hour)': traffic_volume,
    'Average Speed (km/h)': average_speed,
    'Accident Count': accident_count
})

# Function to create comparison bar plots
def plot_traffic_metrics():
    # Set up the figure with 3 subplots (one for each metric)
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle('TRAFFIC HOTSPOTS COMPARISON', fontsize=16, fontweight='bold')
    
    # Plot 1: Traffic Volume
    axes[0].bar(locations, traffic_volume, color='royalblue', edgecolor='navy')
    axes[0].set_title('Average Traffic Volume')
    axes[0].set_xlabel('Location')
    axes[0].set_ylabel('Vehicles per Hour')
    axes[0].grid(axis='y', linestyle='--', alpha=0.7)
    
    # Plot 2: Average Speed
    axes[1].bar(locations, average_speed, color='forestgreen', edgecolor='darkgreen')
    axes[1].set_title('Average Speed')
    axes[1].set_xlabel('Location')
    axes[1].set_ylabel('Speed (km/h)')
    axes[1].grid(axis='y', linestyle='--', alpha=0.7)
    
    # Plot 3: Accident Count
    axes[2].bar(locations, accident_count, color='firebrick', edgecolor='darkred')
    axes[2].set_title('Accident Count')
    axes[2].set_xlabel('Location')
    axes[2].set_ylabel('Number of Accidents')
    axes[2].grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add value labels on top of each bar
    for i, ax in enumerate(axes):
        values = [traffic_volume, average_speed, accident_count][i]
        for j, v in enumerate(values):
            ax.text(j, v + (max(values) * 0.02), f"{v}", 
                   ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.88)
    plt.savefig('traffic_hotspots_comparison.png')
    plt.show()

# Function to create a grouped bar chart for all metrics
def plot_grouped_comparison():
    # Create a figure
    plt.figure(figsize=(12, 8))
    
    # Set width of bars
    barWidth = 0.25
    
    # Set positions of the bars on X axis
    r1 = np.arange(len(locations))
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]
    
    # Create bars
    plt.bar(r1, [v/20 for v in traffic_volume], width=barWidth, color='royalblue', 
            edgecolor='navy', label='Traffic Volume (÷20 vehicles/hour)')
    plt.bar(r2, average_speed, width=barWidth, color='forestgreen', 
            edgecolor='darkgreen', label='Average Speed (km/h)')
    plt.bar(r3, accident_count, width=barWidth, color='firebrick', 
            edgecolor='darkred', label='Accident Count')
    
    # Add labels and title
    plt.xlabel('Location', fontweight='bold', fontsize=12)
    plt.ylabel('Value', fontweight='bold', fontsize=12)
    plt.title('TRAFFIC HOTSPOTS - All Metrics Comparison', fontweight='bold', fontsize=16)
    
    # Add xticks on the middle of the group bars
    plt.xticks([r + barWidth for r in range(len(locations))], locations)
    
    # Add value labels on top of each bar
    # Traffic Volume (scaled)
    for i, v in enumerate([v/20 for v in traffic_volume]):
        plt.text(r1[i], v + 0.5, f"{traffic_volume[i]}", ha='center', va='bottom', fontsize=9)
    # Speed
    for i, v in enumerate(average_speed):
        plt.text(r2[i], v + 0.5, f"{v}", ha='center', va='bottom', fontsize=9)
    # Accidents
    for i, v in enumerate(accident_count):
        plt.text(r3[i], v + 0.5, f"{v}", ha='center', va='bottom', fontsize=9)
    
    # Add a legend
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('traffic_hotspots_grouped.png')
    plt.show()

# Run the visualization functions
plot_traffic_metrics()  # Creates three separate bar charts
# plot_grouped_comparison()  # Creates a single grouped bar chart (note: traffic volume is scaled)