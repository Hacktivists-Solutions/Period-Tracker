def avg_cycle(menstrual_cycles):
    
    total_days = 0
    total_cycles = 0

    for cycle in menstrual_cycles:
        # Calculate cycle length (in days)
        cycle_length = (cycle.end_date - cycle.start_date).days + 1
        total_days += cycle_length
        total_cycles += 1

    if total_cycles > 0:
        # Compute average cycle length
        return total_days / total_cycles
    else:
        return 0
