import simpy
import random
import matplotlib.pyplot as plt

# List to store phase completion times for visualization
phase_times = []
total_cost = 0  # Track the total cost

# Utility Functions
def apply_risk(base_duration):
    """Simulate risk affecting the duration."""
    risk_factor = random.uniform(0.8, 1.2)  # Risk between 80%-120%
    return round(base_duration * risk_factor)

def calculate_cost(duration, hourly_rate, team_size):
    """Calculate the cost for a phase."""
    return duration * hourly_rate * team_size

def log_milestone(phase, milestone, env):
    """Log milestones during phases."""
    print(f"Milestone '{milestone}' in {phase} reached at time {env.now}")

# Define SDLC phases as functions
def requirements_gathering(env, team_size, base_duration):
    start_time = env.now
    print(f"Requirements Gathering started at {start_time}")
    adjusted_duration = apply_risk(base_duration / (1 + (team_size - 1) * 0.5))
    yield env.timeout(adjusted_duration)
    end_time = env.now
    print(f"Requirements Gathering completed at {end_time}")
    phase_times.append(('Requirements Gathering', start_time, end_time))

def design(env, team_size, base_duration):
    start_time = env.now
    print(f"Design started at {start_time}")
    adjusted_duration = apply_risk(base_duration / (1 + (team_size - 1) * 0.5))
    yield env.timeout(adjusted_duration)
    end_time = env.now
    print(f"Design completed at {end_time}")
    phase_times.append(('Design', start_time, end_time))

def development(env, team_size, base_duration):
    start_time = env.now
    print(f"Development started at {start_time}")
    adjusted_duration = apply_risk(base_duration / (1 + (team_size - 1) * 0.75))
    half_time = adjusted_duration // 2
    yield env.timeout(half_time)
    log_milestone('Development', 'Prototype completed', env)
    yield env.timeout(half_time)
    end_time = env.now
    phase_cost = calculate_cost(adjusted_duration, hourly_rate=50, team_size=team_size)
    global total_cost
    total_cost += phase_cost
    print(f"Development completed at {end_time}, Cost: ${phase_cost}")
    phase_times.append(('Development', start_time, end_time))

def testing(env, team_size, base_duration):
    start_time = env.now
    print(f"Testing started at {start_time}")
    adjusted_duration = apply_risk(base_duration / (1 + (team_size - 1) * 0.75))
    yield env.timeout(adjusted_duration)
    end_time = env.now
    print(f"Testing completed at {end_time}")
    phase_times.append(('Testing', start_time, end_time))

def deployment(env, team_size, base_duration):
    start_time = env.now
    print(f"Deployment started at {start_time}")
    adjusted_duration = apply_risk(base_duration / (1 + (team_size - 1) * 0.25))
    yield env.timeout(adjusted_duration)
    end_time = env.now
    print(f"Deployment completed at {end_time}")
    phase_times.append(('Deployment', start_time, end_time))

# Simulation setup with parallel tasks
def run_sdlc(env, team_size, durations):
    yield env.process(requirements_gathering(env, team_size, durations['requirements']))
    yield env.process(design(env, team_size, durations['design']))
    dev = env.process(development(env, team_size, durations['development']))
    test = env.process(testing(env, team_size, durations['testing']))
    yield dev & test
    yield env.process(deployment(env, team_size, durations['deployment']))

# Collect user inputs
team_size = int(input("Enter the team size: "))
durations = {
    'requirements': int(input("Enter the base duration for Requirements Gathering (weeks): ")),
    'design': int(input("Enter the base duration for Design (weeks): ")),
    'development': int(input("Enter the base duration for Development (weeks): ")),
    'testing': int(input("Enter the base duration for Testing (weeks): ")),
    'deployment': int(input("Enter the base duration for Deployment (weeks): ")),
}

# Initialize simulation environment
env = simpy.Environment()
env.process(run_sdlc(env, team_size, durations))
env.run()

# Visualization of the results
# Extract phase names, start times, and end times
phase_names = [phase[0] for phase in phase_times]
start_times = [phase[1] for phase in phase_times]
end_times = [phase[2] for phase in phase_times]

# Calculate the duration of each phase
durations = [end - start for start, end in zip(start_times, end_times)]

# Plotting the results
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(phase_names, durations, left=start_times, color='skyblue')
ax.set_xlabel('Time (Weeks)')
ax.set_title('Software Development Life Cycle Simulation')
ax.grid(True)
plt.suptitle(f'Total Cost: ${total_cost}', fontsize=14, y=0.95)
plt.tight_layout()
plt.show()
