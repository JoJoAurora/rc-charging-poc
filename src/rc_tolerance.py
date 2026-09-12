import numpy as np
import matplotlib.pyplot as plt

# Supply parameters
V0 = 5.0
VIH = 0.7 * V0

# Part A chosen components and datasheet tolerances
R_nominal = 100e3      # 100 kOhm
C_nominal = 100e-12    # Note: convert to Farads; for 100nF use 100e-9
C_nominal = 100e-9     # 100 nF

tol_R = 0.05           # +/- 5% resistor tolerance
tol_C = 0.10           # +/- 10% capacitor tolerance

# Extreme component values
R_min = R_nominal * (1 - tol_R)
R_max = R_nominal * (1 + tol_R)
C_min = C_nominal * (1 - tol_C)
C_max = C_nominal * (1 + tol_C)

# Equation (13) release times
k = -np.log(1 - VIH / V0)
t_nominal = k * R_nominal * C_nominal
t_fastest = k * R_min * C_min
t_slowest = k * R_max * C_max

def charging(t, R, C):
    tau = R * C
    return V0 * (1 - np.exp(-t / tau))

# Time axis based on min case to display all curves full duration
tau_max = R_max * C_max
t = np.linspace(0, 5 * tau_max, 500)

fig, ax = plt.subplots()

# Nominal curve (solid and bold)
ax.plot(t, charging(t, R_nominal, C_nominal), color="black", linewidth=2.0,
        label=f"Nominal ({t_nominal*1e3:.2f} ms)")

# Min curve (dashed)
ax.plot(t, charging(t, R_min, C_min), color="black", linestyle="--", linewidth=1.3,
        label=f"Min Case ({t_fastest*1e3:.2f} ms)")

# Max curve (dash-dot)
ax.plot(t, charging(t, R_max, C_max), color="black", linestyle="-.", linewidth=1.3,
        label=f"Max Case ({t_slowest*1e3:.2f} ms)")

# Dotted reference line for V_IH
ax.axhline(VIH, linestyle=":", color="0.4", label=r"$V_{IH} = 0.7 V_0$")

ax.grid(False)
ax.set_xlabel("Time (s)")
ax.set_ylabel("Voltage (V)")
ax.set_title("POR Charging Curves under Component Tolerances")
ax.legend(loc="lower right")

fig.savefig("../figures/generated/rc_tolerance.pdf")
plt.show()