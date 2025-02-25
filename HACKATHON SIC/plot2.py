import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Data from the provided information
days = ['Monday', 'Tuesday', 'Wednesday', 'Saturday', 'Sunday', 'Sunday']
times = ['08:00', '08:00', '08:00', '15:00', '11:00', '12:00']
traffic_volumes = [1294.3, 1226.1, 1109.0, 1091.9, 1093.7, 1121.7]

# Create labels for x-axis that combine day and time
labels = [f"{day}\n{time}" for day, time in zip(days, times)]

# Create a DataFrame
data = pd.DataFrame({
    'Day': days,
    'Time': times,
    'Traffic Volume': traffic_volumes,
    'Label': labels,
    'Day Type': ['Weekday' if day in ['Monday', 'Tuesday', 'Wednesday'] else 'Weekend' for day in days]
})

# Create the plot
plt.figure(figsize=(12, 8))

# Create color map for weekday vs weekend
colors = ['#3498db' if day_type == 'Weekday' else '#e74c3c' for day_type in data['Day Type']]

# Create the bar plot
bars = plt.bar(labels, data['Traffic Volume'], color=colors, width=0.6, edgecolor='black', linewidth=1)

# Add value labels on top of bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 10,
             f'{height:.1f}', ha='center', va='bottom', fontweight='bold')

# Add title and labels
plt.title('PEAK HOUR ANALYSIS', fontsize=16, fontweight='bold', pad=20)
plt.ylabel('Traffic Volume (vehicles/hour)', fontsize=12, fontweight='bold')
plt.xlabel('Day and Time', fontsize=12, fontweight='bold')

# Add grid for better readability
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Customize y-axis to start from a reasonable value
plt.ylim(1000, 1350)

# Add a legend
weekday_patch = plt.Rectangle((0, 0), 1, 1, fc='#3498db', edgecolor='black')
weekend_patch = plt.Rectangle((0, 0), 1, 1, fc='#e74c3c', edgecolor='black')
plt.legend([weekday_patch, weekend_patch], ['Weekday', 'Weekend'], loc='upper right')

# Add a horizontal line for average traffic volume
avg_volume = data['Traffic Volume'].mean()
plt.axhline(y=avg_volume, color='green', linestyle='--', alpha=0.7)
plt.text(len(data) - 0.5, avg_volume + 5, f'Average: {avg_volume:.1f}', 
         ha='right', va='bottom', color='green', fontweight='bold')

# Adjust layout
plt.tight_layout()

# Add annotations for weekday and weekend sections
plt.annotate('Weekday Peak Hours', xy=(1, 1050), xytext=(1, 1020),
             arrowprops=dict(arrowstyle='->'), fontsize=10, ha='center')
plt.annotate('Weekend Peak Hours', xy=(4, 1050), xytext=(4, 1020),
             arrowprops=dict(arrowstyle='->'), fontsize=10, ha='center')

# Save and show the plot
plt.savefig('peak_hour_analysis.png')
plt.show()

# Alternative: Create a grouped bar chart separating weekdays and weekends
def create_grouped_chart():
    # Prepare data
    weekday_data = data[data['Day Type'] == 'Weekday']
    weekend_data = data[data['Day Type'] == 'Weekend']
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
    
    # Weekday plot
    weekday_bars = ax1.bar(weekday_data['Label'], weekday_data['Traffic Volume'], 
                           color='#3498db', width=0.6, edgecolor='black')
    ax1.set_title('Weekday Peak Hours', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Traffic Volume (vehicles/hour)', fontsize=12)
    ax1.set_ylim(1000, 1350)
    ax1.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Weekend plot
    weekend_bars = ax2.bar(weekend_data['Label'], weekend_data['Traffic Volume'], 
                          color='#e74c3c', width=0.6, edgecolor='black')
    ax2.set_title('Weekend Peak Hours', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Traffic Volume (vehicles/hour)', fontsize=12)
    ax2.set_ylim(1000, 1350)
    ax2.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add value labels
    for ax, bars in [(ax1, weekday_bars), (ax2, weekend_bars)]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 10,
                   f'{height:.1f}', ha='center', va='bottom', fontweight='bold')
    
    # Add super title
    fig.suptitle('PEAK HOUR ANALYSIS', fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.savefig('peak_hour_analysis_grouped.png')
    plt.show()

# Uncomment to run the grouped chart
# create_grouped_chart()