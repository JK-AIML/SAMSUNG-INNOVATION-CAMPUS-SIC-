import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Data from the provided information
locations = [
    'Silk Board Junction (Evening)',
    'MG Road (Evening)',
    'MG Road (Afternoon)',
    'MG Road (Morning)',
    'Silk Board Junction (Morning)'
]

current_timings = [75.7, 74.7, 71.4, 68.7, 68.5]
optimized_timings = [64.0, 63.0, 60.0, 58.0, 58.0]
speed_improvements = [3.9, 3.9, 3.8, 3.6, 3.5]

# Create a DataFrame
data = pd.DataFrame({
    'Location': locations,
    'Current Timing (s)': current_timings,
    'Optimized Timing (s)': optimized_timings,
    'Speed Improvement (km/h)': speed_improvements,
    'Time Reduction (s)': [c - o for c, o in zip(current_timings, optimized_timings)],
    'Time Reduction (%)': [(c - o) / c * 100 for c, o in zip(current_timings, optimized_timings)]
})

# Sort by time reduction percentage for better visualization
data = data.sort_values('Time Reduction (%)', ascending=False)

# Create the main plot comparing current vs optimized timing
def plot_timing_comparison():
    fig, ax1 = plt.subplots(figsize=(14, 8))
    
    # Set width of bars
    bar_width = 0.35
    index = np.arange(len(locations))
    
    # Create bars
    current_bars = ax1.bar(index - bar_width/2, data['Current Timing (s)'], bar_width, 
                           label='Current Timing', color='#e74c3c', edgecolor='black')
    
    optimized_bars = ax1.bar(index + bar_width/2, data['Optimized Timing (s)'], bar_width,
                             label='Optimized Timing', color='#2ecc71', edgecolor='black')
    
    # Add primary y-axis label
    ax1.set_ylabel('Signal Timing (seconds)', fontsize=12, fontweight='bold')
    ax1.set_ylim(0, max(data['Current Timing (s)']) * 1.15)
    
    # Create a secondary y-axis for speed improvement
    ax2 = ax1.twinx()
    ax2.plot(index, data['Speed Improvement (km/h)'], 'o-', color='#3498db', linewidth=2, markersize=8)
    ax2.set_ylabel('Speed Improvement (km/h)', fontsize=12, fontweight='bold', color='#3498db')
    ax2.tick_params(axis='y', labelcolor='#3498db')
    ax2.set_ylim(0, max(data['Speed Improvement (km/h)']) * 1.5)
    
    # Add value labels on top of bars
    for i, bar in enumerate(current_bars):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}s', ha='center', va='bottom', fontsize=9)
    
    for i, bar in enumerate(optimized_bars):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}s', ha='center', va='bottom', fontsize=9)
    
    # Add speed improvement labels
    for i, value in enumerate(data['Speed Improvement (km/h)']):
        ax2.text(i, value + 0.2, f'+{value:.1f} km/h', 
                ha='center', va='bottom', color='#3498db', fontweight='bold', fontsize=9)
    
    # Add time reduction percentage texts
    for i, value in enumerate(data['Time Reduction (%)']):
        ax1.text(i, data['Optimized Timing (s)'].iloc[i] - 10, 
                f'-{value:.1f}%', ha='center', va='top', 
                color='black', fontweight='bold', fontsize=10)
    
    # Customize the plot
    ax1.set_title('SIGNAL TIMING OPTIMIZATION', fontsize=16, fontweight='bold', pad=20)
    ax1.set_xticks(index)
    ax1.set_xticklabels(data['Location'], rotation=45, ha='right')
    ax1.set_xlabel('Location and Time of Day', fontsize=12, fontweight='bold')
    ax1.grid(axis='y', linestyle='--', alpha=0.3)
    
    # Create legend
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2 + [plt.Line2D([0], [0], marker='o', color='#3498db', linestyle='-')], 
              labels + labels2 + ['Speed Improvement'], 
              loc='upper right')
    
    plt.tight_layout()
    plt.savefig('signal_timing_optimization.png')
    plt.show()

# Plot showing time reduction (seconds and percentage)
def plot_time_reduction():
    fig, ax1 = plt.subplots(figsize=(12, 8))
    
    bars = ax1.bar(data['Location'], data['Time Reduction (s)'], 
                  color='#9b59b6', edgecolor='black', alpha=0.8)
    
    # Add secondary y-axis for percentage reduction
    ax2 = ax1.twinx()
    ax2.plot(data['Location'], data['Time Reduction (%)'], 'o-', 
            color='#f39c12', linewidth=2, markersize=8)
    
    # Add labels
    ax1.set_ylabel('Time Reduction (seconds)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Time Reduction (%)', fontsize=12, fontweight='bold', color='#f39c12')
    ax2.tick_params(axis='y', labelcolor='#f39c12')
    
    # Add value labels
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.2,
                f'{height:.1f}s', ha='center', va='bottom', fontsize=9)
    
    for i, value in enumerate(data['Time Reduction (%)']):
        ax2.text(i, value + 0.5, f'{value:.1f}%', 
                ha='center', va='bottom', color='#f39c12', fontweight='bold', fontsize=9)
    
    # Customize plot
    ax1.set_title('SIGNAL TIMING REDUCTION ANALYSIS', fontsize=16, fontweight='bold', pad=20)
    ax1.set_xticklabels(data['Location'], rotation=45, ha='right')
    ax1.grid(axis='y', linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('signal_timing_reduction.png')
    plt.show()

# Run the visualizations
plot_timing_comparison()
# Uncomment to show the time reduction analysis
# plot_time_reduction()