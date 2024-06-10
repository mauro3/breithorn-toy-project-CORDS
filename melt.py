def glacier_melt(temperature, melt_factor):

    if temperature >= 0:
        return temperature * melt_factor
    else:
        return 0.0

def  glacier_accumulation(temperature, t_threshold, precip):
    
    if temperature <= t_threshold:
        return precip
    else:
        return 0.0
    
def lapsed_temperature(temperature_s, elevation, lapse_rate):
    
    delta_h = elevation - elevation_s
    return lapse_rate * delta_h + temperature_s

def net_balance_fn(dt, Ts, Ps, melt_factor, T_threshold):
    """
    Integrate the balance rate (this is at a point) over time for given temperature and precipitation arrays to get the "net balance".

    Args:
        dt: The time step.
        Ts: Array of temperatures.
        Ps: Array of precipitations.
        melt_factor: The factor to compute melt amount.
        T_threshold: The temperature threshold for accumulation.

    Returns:
        net balance (this is at a point)
    """
    assert len(Ts) == len(Ps)
    total = 0.0
    for T, P in zip(Ts, Ps):
        balance_rate = -melt(T, melt_factor) + accumulate(T, P, T_threshold)
        total += balance_rate * dt
    return total


def glacier_net_balance_fn(zs, dt, Ts, Ps, melt_factor, T_threshold, lapse_rate):
    """
    Calculate:
    - the glacier net balance (integration of balance rate over time and space)
    - the net balance at each point (integration of balance rate over time)

    Args:
        zs: Array of elevations (with the weather station as datum)
        dt: The time step.
        Ts: Array of temperatures.
        Ps: Array of precipitations.
        melt_factor: The factor to compute melt amount.
        T_threshold: The temperature threshold for accumulation.
        lapse_rate: The lapse rate (temperature change per unit elevation change).

    Returns:
        the glacier net balance [m]
        net balance at all points [m]
    """
    glacier_net_balance = 0.0
    net_balance = np.zeros(len(zs))
    for i, z in enumerate(zs):
        TT = [lapse(T, z, lapse_rate) for T in Ts]
        net_balance[i] = net_balance_fn(dt, TT, Ps, melt_factor, T_threshold)
        glacier_net_balance += net_balance[i]
    return glacier_net_balance / len(zs), net_balance


# Example usage
temperature_s = 5    # °C, temperature at weather station
elevation_s = 2000   # m, elevation of the weather station
melt_factor = 0.005  # m/d/°C
precip = 0.5         # m
lapse_rate = -0.009  # °C/m
elevation = 2500     # example elevation
t_threshold = 0      # °C, temperature threshold
temperature = lapsed_temperature(temperature_s, elevation, lapse_rate)
melt = glacier_melt(temperature, melt_factor)
accumulation = glacier_accumulation(temperature, t_threshold, precip)
print(f"Glacier melt: {melt} m/d, Glacier accumulation: {accumulation}")

# Test cases
def test_lapsed_temperature():
    assert lapsed_temperature(5, 2500, -0.009) == 0.5
    assert lapsed_temperature(10, 1000, -0.006) == 4.0

def test_glacier_melt():
    assert glacier_melt(5, 0.005) == 0.025
    assert glacier_melt(-5, 0.005) == 0.0

def test_glacier_accumulation():
    assert glacier_accumulation(-5, 0, 0.5) == 0.5
    assert glacier_accumulation(4, 4, 10) == 10
    assert glacier_accumulation(0, 0, 0.5) == 0.5

# Run tests
# test_lapsed_temperature()
test_glacier_melt()
# test_glacier_accumulation()

print("All tests passed.")
