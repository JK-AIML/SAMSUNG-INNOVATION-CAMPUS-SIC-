import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import random
import datetime

# ----- 1. DATA GENERATION -----

def generate_sample_traffic_data(days=7, locations=10):
    """
    Generate synthetic traffic data for Bengaluru
    """
    # Popular areas in Bengaluru
    locations = [
        "Silk Board Junction", "Electronic City", "Whitefield", 
        "Marathahalli", "Hebbal", "MG Road", "Koramangala",
        "HSR Layout", "Indiranagar", "Jayanagar"
    ]
    
    # Generate timestamps for a week with hourly data
    start_date = datetime.datetime(2024, 2, 1)
    timestamps = [start_date + datetime.timedelta(hours=i) for i in range(24 * days)]
    
    data = []
    for ts in timestamps:
        hour = ts.hour
        day_of_week = ts.weekday()  # 0 = Monday, 6 = Sunday
        
        # Create realistic traffic patterns
        for location in locations:
            # Base traffic varies by location
            if "Junction" in location or "Road" in location:
                base_traffic = random.randint(800, 1200)
            else:
                base_traffic = random.randint(500, 900)
            
            # Morning rush hour (8-10 AM) on weekdays
            if 8 <= hour <= 10 and day_of_week < 5:
                traffic_volume = base_traffic * random.uniform(1.4, 1.8)
            # Evening rush hour (5-8 PM) on weekdays
            elif 17 <= hour <= 20 and day_of_week < 5:
                traffic_volume = base_traffic * random.uniform(1.5, 1.9)
            # Weekend patterns
            elif day_of_week >= 5:
                if 10 <= hour <= 20:  # Weekend activity hours
                    traffic_volume = base_traffic * random.uniform(1.2, 1.6)
                else:
                    traffic_volume = base_traffic * random.uniform(0.5, 0.9)
            # Late night
            elif 0 <= hour <= 5:
                traffic_volume = base_traffic * random.uniform(0.1, 0.4)
            # Regular daytime
            else:
                traffic_volume = base_traffic * random.uniform(0.7, 1.3)
            
            # Average speed (km/h) - inversely related to traffic volume
            avg_speed = max(5, 60 - (traffic_volume / 200))
            
            # Signal timing in seconds
            if traffic_volume > 1500:
                signal_timing = random.randint(90, 120)
            elif traffic_volume > 1000:
                signal_timing = random.randint(60, 90)
            else:
                signal_timing = random.randint(30, 60)
            
            # Number of accidents (rare events)
            accidents = 1 if random.random() < 0.05 else 0
            
            # Road conditions (0-10 scale)
            road_condition = random.randint(3, 9)
            
            data.append({
                'timestamp': ts,
                'location': location,
                'traffic_volume': int(traffic_volume),
                'avg_speed': round(avg_speed, 1),
                'signal_timing': signal_timing,
                'accidents': accidents,
                'road_condition': road_condition,
                'hour': hour,
                'day_of_week': day_of_week
            })
    
    return pd.DataFrame(data)

# ----- 2. DATA ANALYSIS -----

class BengaluruTrafficAnalyzer:
    def __init__(self, data):
        self.data = data
        self.hotspots = None
    
    def preprocess_data(self):
        """Basic preprocessing of traffic data"""
        # Convert timestamp to datetime if it's not already
        if not pd.api.types.is_datetime64_any_dtype(self.data['timestamp']):
            self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])
        
        # Extract time components if not already present
        if 'hour' not in self.data.columns:
            self.data['hour'] = self.data['timestamp'].dt.hour
        if 'day_of_week' not in self.data.columns:
            self.data['day_of_week'] = self.data['timestamp'].dt.dayofweek
        
        # Add period of day
        self.data['period'] = pd.cut(
            self.data['hour'],
            bins=[0, 6, 12, 18, 24],
            labels=['Night', 'Morning', 'Afternoon', 'Evening'],
            right=False
        )
        
        return self.data
    
    def identify_traffic_hotspots(self):
        """Identify traffic hotspots using clustering"""
        # Group by location and calculate average metrics
        location_stats = self.data.groupby('location').agg({
            'traffic_volume': 'mean',
            'avg_speed': 'mean',
            'accidents': 'sum'
        }).reset_index()
        
        # Scale the features
        scaler = StandardScaler()
        features = ['traffic_volume', 'avg_speed', 'accidents']
        scaled_features = scaler.fit_transform(location_stats[features])
        
        # Apply K-means clustering to identify hotspots
        kmeans = KMeans(n_clusters=3, random_state=42)
        location_stats['cluster'] = kmeans.fit_predict(scaled_features)
        
        # Identify the most congested cluster (high volume, low speed)
        clusters_summary = location_stats.groupby('cluster').agg({
            'traffic_volume': 'mean',
            'avg_speed': 'mean'
        })
        congested_cluster = clusters_summary['traffic_volume'].idxmax()
        
        # Store hotspots
        self.hotspots = location_stats[location_stats['cluster'] == congested_cluster]
        return self.hotspots
    
    def analyze_peak_hours(self):
        """Analyze traffic patterns by hour of day"""
        hourly_patterns = self.data.groupby(['hour', 'day_of_week']).agg({
            'traffic_volume': 'mean',
            'avg_speed': 'mean'
        }).reset_index()
        
        # Define peak hours where traffic volume is high
        peak_threshold = hourly_patterns['traffic_volume'].quantile(0.75)
        peak_hours = hourly_patterns[hourly_patterns['traffic_volume'] >= peak_threshold]
        
        return peak_hours
    
    def analyze_signal_efficiency(self):
        """Analyze traffic signal efficiency"""
        signal_analysis = self.data.groupby(['location', 'period']).agg({
            'traffic_volume': 'mean',
            'signal_timing': 'mean',
            'avg_speed': 'mean'
        }).reset_index()
        
        # Calculate efficiency metric (higher is better)
        signal_analysis['signal_efficiency'] = signal_analysis['avg_speed'] / signal_analysis['signal_timing'] * 100
        
        return signal_analysis.sort_values('signal_efficiency')
    
    def generate_optimization_recommendations(self):
        """Generate traffic management recommendations"""
        recommendations = []
        
        # Get hotspots if not already calculated
        if self.hotspots is None:
            self.identify_traffic_hotspots()
        
        # Get peak hours
        peak_hours_data = self.analyze_peak_hours()
        weekday_peak_hours = peak_hours_data[peak_hours_data['day_of_week'] < 5]
        
        # Get signal efficiency
        signal_efficiency = self.analyze_signal_efficiency()
        inefficient_signals = signal_efficiency.sort_values('signal_efficiency').head(5)
        
        # 1. Hotspot recommendations
        for _, hotspot in self.hotspots.iterrows():
            location = hotspot['location']
            loc_data = self.data[self.data['location'] == location]
            
            # Check if accidents are high
            if hotspot['accidents'] > 0:
                recommendations.append({
                    'location': location,
                    'issue': 'High accident rate',
                    'recommendation': 'Implement dedicated traffic police during peak hours and improve road markings'
                })
            
            # Check for signal timing
            signal_data = signal_efficiency[signal_efficiency['location'] == location]
            if not signal_data.empty and signal_data['signal_efficiency'].min() < signal_efficiency['signal_efficiency'].median():
                recommendations.append({
                    'location': location,
                    'issue': 'Inefficient signal timing',
                    'recommendation': 'Adjust signal timing based on real-time traffic volume'
                })
        
        # 2. Peak hour recommendations
        common_peak_hours = weekday_peak_hours['hour'].value_counts().nlargest(3).index.tolist()
        recommendations.append({
            'location': 'All major junctions',
            'issue': f'Peak congestion during hours {common_peak_hours}',
            'recommendation': 'Implement staggered office hours and encourage public transport usage'
        })
        
        # 3. Signal timing recommendations
        for _, signal in inefficient_signals.iterrows():
            recommendations.append({
                'location': signal['location'],
                'issue': f'Inefficient signal during {signal["period"]}',
                'recommendation': 'Implement adaptive signal control based on traffic volume'
            })
        
        return pd.DataFrame(recommendations)
    
    def visualize_traffic_patterns(self):
        """Create visualizations for traffic patterns"""
        # 1. Traffic volume by hour and day
        plt.figure(figsize=(12, 6))
        hourly_data = self.data.groupby(['hour', 'day_of_week'])['traffic_volume'].mean().reset_index()
        hourly_data['day_name'] = hourly_data['day_of_week'].map({
            0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 
            4: 'Friday', 5: 'Saturday', 6: 'Sunday'
        })
        
        pivot_data = hourly_data.pivot(index='hour', columns='day_name', values='traffic_volume')
        sns.heatmap(pivot_data, cmap='YlOrRd', annot=False)
        plt.title('Traffic Volume by Hour and Day of Week')
        plt.savefig('traffic_heatmap.png')
        
        # 2. Hotspots visualization
        if self.hotspots is not None:
            plt.figure(figsize=(10, 6))
            sns.barplot(x='location', y='traffic_volume', data=self.hotspots)
            plt.xticks(rotation=45, ha='right')
            plt.title('Traffic Hotspots in Bengaluru')
            plt.tight_layout()
            plt.savefig('traffic_hotspots.png')
        
        # 3. Signal efficiency by location
        signal_efficiency = self.analyze_signal_efficiency()
        plt.figure(figsize=(12, 6))
        pivot_signals = signal_efficiency.pivot(index='location', columns='period', values='signal_efficiency')
        sns.heatmap(pivot_signals, cmap='coolwarm', annot=True, fmt='.1f')
        plt.title('Signal Efficiency by Location and Time of Day')
        plt.tight_layout()
        plt.savefig('signal_efficiency.png')

# ----- 3. TRAFFIC OPTIMIZATION -----

class TrafficOptimizer:
    def __init__(self, data):
        self.data = data
        self.analyzer = BengaluruTrafficAnalyzer(data)
        # Preprocess the data
        self.analyzer.preprocess_data()
    
    def optimize_signal_timing(self):
        """Generate optimized signal timings"""
        # Get the current signal efficiency
        signal_data = self.analyzer.analyze_signal_efficiency()
        
        # Create optimized signal timings
        optimized_signals = []
        
        for _, row in signal_data.iterrows():
            location = row['location']
            period = row['period']
            current_timing = row['signal_timing']
            traffic_volume = row['traffic_volume']
            
            # Optimization logic:
            # 1. For high traffic, make signals longer but proportional to volume
            # 2. For low traffic, make signals shorter
            # 3. Balance green time with traffic flow
            
            if traffic_volume > 1500:
                # High traffic: optimize for throughput
                optimized_timing = min(120, int(current_timing * 0.9))
            elif traffic_volume > 1000:
                # Medium traffic: slight reduction if possible
                optimized_timing = min(90, int(current_timing * 0.85))
            else:
                # Low traffic: shorter signals
                optimized_timing = max(30, int(current_timing * 0.7))
            
            # Calculate expected improvement
            expected_speed_improvement = min(15, (current_timing - optimized_timing) / 3)
            
            optimized_signals.append({
                'location': location,
                'period': period,
                'current_timing': current_timing,
                'optimized_timing': optimized_timing,
                'expected_speed_improvement': expected_speed_improvement
            })
        
        return pd.DataFrame(optimized_signals)
    
    def suggest_route_diversions(self):
        """Suggest alternative routes to divert traffic from hotspots"""
        # Get the hotspots
        hotspots = self.analyzer.identify_traffic_hotspots()
        hotspot_locations = hotspots['location'].tolist()
        
        # Define possible alternative routes (in a real system, this would be based on a graph)
        alternative_routes = [
            {
                'hotspot': 'Silk Board Junction',
                'alternative_routes': [
                    'Hosur Road -> Sarjapur Road -> Outer Ring Road',
                    'BTM Layout -> Bannerghatta Road -> JP Nagar'
                ],
                'estimated_time_saving': '15-20 min'
            },
            {
                'hotspot': 'Electronic City',
                'alternative_routes': [
                    'Hosur Road -> Bommanahalli -> BTM Layout',
                    'Nice Road -> Bannerghatta Road'
                ],
                'estimated_time_saving': '10-15 min'
            },
            {
                'hotspot': 'Whitefield',
                'alternative_routes': [
                    'Old Madras Road -> KR Puram -> Hoodi',
                    'ITPL Main Road -> Varthur Kodi -> Sarjapur Road'
                ],
                'estimated_time_saving': '15-25 min'
            },
            {
                'hotspot': 'Marathahalli',
                'alternative_routes': [
                    'HAL Airport Road -> Wind Tunnel Road -> Suranjan Das Road',
                    'Outer Ring Road -> Sarjapur Road -> Haralur Road'
                ],
                'estimated_time_saving': '15-20 min'
            },
            {
                'hotspot': 'Hebbal',
                'alternative_routes': [
                    'Bellary Road -> Outer Ring Road -> Banaswadi',
                    'Hennur Road -> Thanisandra Main Road'
                ],
                'estimated_time_saving': '10-15 min'
            },
            {
                'hotspot': 'MG Road',
                'alternative_routes': [
                    'Cubbon Road -> Infantry Road -> Commercial Street',
                    'Residency Road -> Richmond Road -> Double Road'
                ],
                'estimated_time_saving': '5-10 min'
            },
            {
                'hotspot': 'Koramangala',
                'alternative_routes': [
                    'Inner Ring Road -> Double Road -> Richmond Road',
                    'Sarjapur Road -> Haralur Road -> HSR Layout'
                ],
                'estimated_time_saving': '10-15 min'
            }
        ]
        
        # Filter for identified hotspots
        diversion_plans = [route for route in alternative_routes 
                          if route['hotspot'] in hotspot_locations]
        
        return pd.DataFrame(diversion_plans)
    
    def optimize_public_transport(self):
        """Suggest public transport optimization"""
        # Analyze peak hour patterns
        peak_hours = self.analyzer.analyze_peak_hours()
        weekday_peaks = peak_hours[peak_hours['day_of_week'] < 5]
        
        # Calculate high traffic locations during peak hours
        peak_locations = self.data[
            (self.data['hour'].isin(weekday_peaks['hour'])) & 
            (self.data['day_of_week'] < 5)
        ].groupby('location')['traffic_volume'].mean().sort_values(ascending=False)
        
        # Generate bus route recommendations
        bus_recommendations = []
        
        for location, volume in peak_locations.items():
            if volume > 1000:
                frequency = 'Every 5-10 minutes'
                priority = 'High'
            elif volume > 700:
                frequency = 'Every 10-15 minutes'
                priority = 'Medium'
            else:
                frequency = 'Every 15-20 minutes'
                priority = 'Normal'
            
            bus_recommendations.append({
                'location': location,
                'avg_traffic_volume': volume,
                'recommended_frequency': frequency,
                'priority': priority,
                'special_services': 'Yes' if volume > 1200 else 'No'
            })
        
        return pd.DataFrame(bus_recommendations)
    
    def generate_complete_traffic_plan(self):
        """Generate a complete traffic management plan"""
        # Get signal timing optimization
        signal_optimizations = self.optimize_signal_timing()
        
        # Get route diversions
        route_diversions = self.suggest_route_diversions()
        
        # Get public transport recommendations
        transport_recommendations = self.optimize_public_transport()
        
        # General recommendations
        general_recommendations = [
            {
                'category': 'Infrastructure',
                'recommendation': 'Implement smart traffic lights at top 5 congested junctions',
                'expected_impact': 'Reduce wait time by 20-30%',
                'implementation_timeframe': 'Short-term (3-6 months)'
            },
            {
                'category': 'Policy',
                'recommendation': 'Implement odd-even vehicle scheme during peak hours',
                'expected_impact': 'Reduce traffic volume by 15-20%',
                'implementation_timeframe': 'Medium-term (6-12 months)'
            },
            {
                'category': 'Public Transport',
                'recommendation': 'Increase frequency of metro and bus services during peak hours',
                'expected_impact': 'Shift 10-15% of private vehicle users to public transport',
                'implementation_timeframe': 'Short-term (1-3 months)'
            },
            {
                'category': 'Technology',
                'recommendation': 'Deploy traffic monitoring cameras with AI analytics',
                'expected_impact': 'Improve incident detection time by 60-70%',
                'implementation_timeframe': 'Medium-term (6-9 months)'
            },
            {
                'category': 'Urban Planning',
                'recommendation': 'Develop satellite business districts to decentralize traffic',
                'expected_impact': 'Long-term reduction in commute distances by 20-25%',
                'implementation_timeframe': 'Long-term (2-3 years)'
            }
        ]
        
        return {
            'signal_optimizations': signal_optimizations,
            'route_diversions': route_diversions,
            'transport_recommendations': transport_recommendations,
            'general_recommendations': pd.DataFrame(general_recommendations)
        }

# ----- 4. DASHBOARD SIMULATION -----

def create_traffic_dashboard(analyzer, optimizer):
    """Simulate a traffic management dashboard"""
    # Get the data
    hotspots = analyzer.identify_traffic_hotspots()
    peak_hours = analyzer.analyze_peak_hours()
    signal_efficiency = analyzer.analyze_signal_efficiency()
    
    # Get the optimizations
    signal_optimizations = optimizer.optimize_signal_timing()
    route_diversions = optimizer.suggest_route_diversions()
    transport_recommendations = optimizer.optimize_public_transport()
    
    # Print the dashboard
    print("\n" + "="*80)
    print("                  BENGALURU TRAFFIC MANAGEMENT DASHBOARD")
    print("="*80)
    
    print("\n1. TRAFFIC HOTSPOTS")
    print("-"*80)
    for _, hotspot in hotspots.iterrows():
        print(f"Location: {hotspot['location']}")
        print(f"  • Average Traffic Volume: {hotspot['traffic_volume']:.1f} vehicles/hour")
        print(f"  • Average Speed: {hotspot['avg_speed']:.1f} km/h")
        print(f"  • Accident Count: {hotspot['accidents']}")
        print()
    
    print("\n2. PEAK HOUR ANALYSIS")
    print("-"*80)
    weekday_peaks = peak_hours[peak_hours['day_of_week'] < 5]
    weekend_peaks = peak_hours[peak_hours['day_of_week'] >= 5]
    
    print("Weekday Peak Hours:")
    for _, peak in weekday_peaks.head(3).iterrows():
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        print(f"  • {day_names[int(peak['day_of_week'])]} at {int(peak['hour']):02d}:00 - Traffic Volume: {peak['traffic_volume']:.1f}")
    
    print("\nWeekend Peak Hours:")
    for _, peak in weekend_peaks.head(3).iterrows():
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        print(f"  • {day_names[int(peak['day_of_week'])]} at {int(peak['hour']):02d}:00 - Traffic Volume: {peak['traffic_volume']:.1f}")
    
    print("\n3. SIGNAL TIMING OPTIMIZATION")
    print("-"*80)
    for _, signal in signal_optimizations.head(5).iterrows():
        print(f"Location: {signal['location']} ({signal['period']})")
        print(f"  • Current Signal Timing: {signal['current_timing']:.1f} seconds")
        print(f"  • Optimized Timing: {signal['optimized_timing']:.1f} seconds")
        print(f"  • Expected Speed Improvement: {signal['expected_speed_improvement']:.1f} km/h")
        print()
    
    print("\n4. RECOMMENDED ROUTE DIVERSIONS")
    print("-"*80)
    for _, route in route_diversions.iterrows():
        print(f"Hotspot: {route['hotspot']}")
        print("  Alternative Routes:")
        for alt_route in route['alternative_routes']:
            print(f"    ◦ {alt_route}")
        print(f"  Estimated Time Saving: {route['estimated_time_saving']}")
        print()
    
    print("\n5. PUBLIC TRANSPORT RECOMMENDATIONS")
    print("-"*80)
    for _, rec in transport_recommendations.head(5).iterrows():
        print(f"Location: {rec['location']} (Priority: {rec['priority']})")
        print(f"  • Recommended Bus Frequency: {rec['recommended_frequency']}")
        if rec['special_services'] == 'Yes':
            print(f"  • Special Express Services Recommended")
        print()

    print("\n" + "="*80)
    print("                     REAL-TIME TRAFFIC ALERTS")
    print("="*80)
    
    # Simulate some real-time alerts
    print("\n• HEAVY CONGESTION ALERT: Silk Board Junction - Traffic moving at 5-10 km/h")
    print("• ACCIDENT REPORTED: Near Hebbal Flyover - Right lane blocked")
    print("• METRO DISRUPTION: Green Line running with 15 min delays")
    print("• ROAD CLOSURE: MG Road closed for repairs between Trinity Circle and Anil Kumble Circle")
    
    print("\n" + "="*80 + "\n")

# ----- 5. MAIN APPLICATION -----

def main():
    """Main function to run the traffic management system"""
    print("Bengaluru Traffic Management System")
    print("==================================")
    print("Loading data and initializing analysis...")
    
    # Generate sample data
    traffic_data = generate_sample_traffic_data(days=7)
    print(f"Loaded data for {len(traffic_data)} traffic observations across 7 days.")
    
    # Initialize analyzer and optimizer
    analyzer = BengaluruTrafficAnalyzer(traffic_data)
    analyzer.preprocess_data()
    optimizer = TrafficOptimizer(traffic_data)
    
    # Perform analysis
    print("\nAnalyzing traffic patterns...")
    hotspots = analyzer.identify_traffic_hotspots()
    print(f"Identified {len(hotspots)} traffic hotspots in Bengaluru.")
    
    # Generate visualizations
    print("Generating traffic visualizations...")
    analyzer.visualize_traffic_patterns()
    print("Visualizations saved to disk.")
    
    # Generate traffic management plan
    print("\nGenerating comprehensive traffic management plan...")
    traffic_plan = optimizer.generate_complete_traffic_plan()
    
    # Create dashboard
    create_traffic_dashboard(analyzer, optimizer)
    
    print("Traffic management analysis complete.")
    print("\nRecommendations Summary:")
    print(f"• Signal timing optimizations for {len(traffic_plan['signal_optimizations'])} locations")
    print(f"• Alternative routes for {len(traffic_plan['route_diversions'])} traffic hotspots")
    print(f"• Public transport enhancements for {len(traffic_plan['transport_recommendations'])} areas")
    print(f"• {len(traffic_plan['general_recommendations'])} general infrastructure and policy recommendations")
    
    print("\nThank you for using Bengaluru Traffic Management System!")

if __name__ == "__main__":
    main()