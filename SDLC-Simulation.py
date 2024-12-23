import simpy
import matplotlib.pyplot as plt

# List to store phase completion times for visualization
phase_times = []

# Define the SDLC phases as functions
def requirements_gathering(env, team_size):
    start_time = env.now
    print(f"Requirements Gathering started at {start_time}")
    base_duration = 4  # Base duration in weeks
    efficiency_factor = 0.5
    adjusted_duration = round(base_duration / (1 + (team_size - 1) * efficiency_factor))
    yield env.timeout(adjusted_duration)
    end_time = env.now
    print(f"Requirements Gathering completed at {end_time}")
    phase_times.append(('Requirements Gathering', start_time, end_time))

def design(env, team_size):
    start_time = env.now
    print(f"Design started at {start_time}")
    base_duration = 2
    efficiency_factor = 0.5
    adjusted_duration = round(base_duration / (1 + (team_size - 1) * efficiency_factor))
    yield env.timeout(adjusted_duration)
    end_time = env.now
    print(f"Design completed at {end_time}")
    phase_times.append(('Design', start_time, end_time))

def development(env, team_size):
    start_time = env.now
    print(f"Development started at {start_time}")
    base_duration = 8
    efficiency_factor = 0.75
    adjusted_duration = round(base_duration / (1 + (team_size - 1) * efficiency_factor))
    yield env.timeout(adjusted_duration)
    end_time = env.now
    print(f"Development completed at {end_time}")
    phase_times.append(('Development', start_time, end_time))

def testing(env, team_size):
    start_time = env.now
    print(f"Testing started at {start_time}")
    base_duration = 3
    efficiency_factor = 0.75
    adjusted_duration = round(base_duration / (1 + (team_size - 1) * efficiency_factor))
    yield env.timeout(adjusted_duration)
    end_time = env.now
    print(f"Testing completed at {end_time}")
    phase_times.append(('Testing', start_time, end_time))

def deployment(env, team_size):
    start_time = env.now
    print(f"Deployment started at {start_time}")
    base_duration = 1
    efficiency_factor = 0.25
    adjusted_duration = round(base_duration / (1 + (team_size - 1) * efficiency_factor))
    yield env.timeout(adjusted_duration)
    end_time = env.now
    print(f"Deployment completed at {end_time}")
    phase_times.append(('Deployment', start_time, end_time))


# Simulation setup
def run_sdlc(env, team_size):
    yield env.process(requirements_gathering(env, team_size))
    yield env.process(design(env, team_size))
    yield env.process(development(env, team_size))
    yield env.process(testing(env, team_size))
    yield env.process(deployment(env, team_size))

# Initialize simulation environment
env = simpy.Environment()

# Start the SDLC simulation with a team of 3 members
env.process(run_sdlc(env, team_size=3))

# Run the simulation
env.run()

# Visualization of the results
# Extract phase names, start times, and end times
phase_names = [phase[0] for phase in phase_times]
start_times = [phase[1] for phase in phase_times]
end_times = [phase[2] for phase in phase_times]

# Plotting the results
fig, ax = plt.subplots(figsize=(10, 6))

# Calculate phase durations
durations = [end - start for start, end in zip(start_times, end_times)]

# Plot each phase as a horizontal bar
ax.barh(phase_names, durations, left=start_times, color='skyblue')

# Add labels and title
ax.set_xlabel('Time')
ax.set_title('Software Development Life Cycle Simulation')

# Show grid for better readability
ax.grid(True)

# Show the plot
plt.tight_layout()
plt.show()
