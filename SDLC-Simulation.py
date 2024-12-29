import simpy
import random
import matplotlib.pyplot as plt

# List to store phase completion times for visualization
phase_times = []
total_cost = 0  # Track the total cost

def log_phase(phase_name, start_time, end_time):
    """Log phase information for both console and visualization."""
    duration = end_time - start_time
    phase_times.append((phase_name, start_time, end_time, duration))
    print(f"{phase_name} completed: Start={start_time}, End={end_time}, Duration={duration} weeks")


# Utility Functions
def apply_risk(base_duration):
    """Simulate risk affecting the duration."""
    risk_factor = random.uniform(0.8, 1.2)  # Risk between 80%-120%
    return round(base_duration * risk_factor)

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
    log_phase('Requirements Gathering', start_time, end_time)


def design(env, team_size, base_duration):
    start_time = env.now
    print(f"Design started at {start_time}")
    adjusted_duration = apply_risk(base_duration / (1 + (team_size - 1) * 0.5))
    yield env.timeout(adjusted_duration)
    end_time = env.now
    log_phase('Design', start_time, end_time)


def development(env, team_size, base_duration):
    start_time = env.now
    print(f"Development started at {start_time}")
    adjusted_duration = apply_risk(base_duration / (1 + (team_size - 1) * 0.75))
    yield env.timeout(adjusted_duration)
    end_time = env.now
    log_phase('Development', start_time, end_time)


def testing(env, team_size, base_duration):
    start_time = env.now
    print(f"Testing started at {start_time}")
    adjusted_duration = apply_risk(base_duration / (1 + (team_size - 1) * 0.75))
    yield env.timeout(adjusted_duration)
    end_time = env.now
    log_phase('Testing', start_time, end_time)


def deployment(env, team_size, base_duration):
    start_time = env.now
    print(f"Deployment started at {start_time}")
    adjusted_duration = apply_risk(base_duration / (1 + (team_size - 1) * 0.25))
    yield env.timeout(adjusted_duration)
    end_time = env.now
    log_phase('Deployment', start_time, end_time)


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
plt.tight_layout()
plt.show()
