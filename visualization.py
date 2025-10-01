import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from conflict_detector import get_position_at_time

def animate_missions(missions: list):
    """
    Animate the 3D flight paths of the given missions over time.
    Each drone is shown as a moving marker along its path.
    Additionally, a short colored trail segment is drawn from the previous to current position,
    with color determined by the current time using a colormap.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Determine the global time range
    min_time = min([min(mission.timestamps) for mission in missions])
    max_time = max([max(mission.timestamps) for mission in missions])
    step = 0.1
    times = np.arange(min_time, max_time + step, step)

    # Assign a color to each mission for marker/path
    colors = plt.cm.get_cmap('tab10', len(missions))
    # Colormap for time-based trail
    trail_cmap = plt.cm.get_cmap('plasma')

    # For each mission, store the marker object and previous position
    markers = []
    prev_positions = []
    trail_lines = []

    for idx, mission in enumerate(missions):
        # Initial marker at the first waypoint
        pos = get_position_at_time(mission, min_time)
        marker, = ax.plot([pos.x], [pos.y], [pos.z], marker='o', color=colors(idx), label=f"Mission {mission.id}")
        markers.append(marker)
        prev_positions.append(pos)
        # Optionally, plot the full path as a faint line for context
        xs = [wp.x for wp in mission.waypoints]
        ys = [wp.y for wp in mission.waypoints]
        zs = [wp.z for wp in mission.waypoints]
        ax.plot(xs, ys, zs, color=colors(idx), alpha=0.3, linestyle='--')
        # Initialize an empty trail line (for the animated segment)
        trail_line, = ax.plot([], [], [], color=trail_cmap(0.0), linewidth=2)
        trail_lines.append(trail_line)

    # Set axis labels and limits
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Missions Flight Paths (Animated)')

    # Set axis limits based on all waypoints
    all_x = [wp.x for m in missions for wp in m.waypoints]
    all_y = [wp.y for m in missions for wp in m.waypoints]
    all_z = [wp.z for m in missions for wp in m.waypoints]
    ax.set_xlim(min(all_x), max(all_x))
    ax.set_ylim(min(all_y), max(all_y))
    ax.set_zlim(min(all_z), max(all_z))

    ax.legend()

    def update(frame_idx):
        t = times[frame_idx]
        norm_t = (t - min_time) / (max_time - min_time) if max_time > min_time else 0.0
        for idx, mission in enumerate(missions):
            # Get current and previous positions
            prev_pos = prev_positions[idx]
            curr_pos = get_position_at_time(mission, t)
            # Move marker
            markers[idx].set_data([curr_pos.x], [curr_pos.y])
            markers[idx].set_3d_properties([curr_pos.z])
            # Draw short trail segment from previous to current position
            trail_color = trail_cmap(norm_t)
            trail_lines[idx].set_data([prev_pos.x, curr_pos.x], [prev_pos.y, curr_pos.y])
            trail_lines[idx].set_3d_properties([prev_pos.z, curr_pos.z])
            trail_lines[idx].set_color(trail_color)
            # Update previous position for next frame
            prev_positions[idx] = curr_pos
        # Return all artists to update
        return markers + trail_lines

    ani = animation.FuncAnimation(
        fig, update, frames=len(times), interval=50, blit=False, repeat=False
    )
    plt.show()
