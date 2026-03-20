import numpy as np
import matplotlib.pyplot as plt

# --- 1. CONFIGURATION DES CONSTANTES PHYSIQUES ---
C = 1.0
G = 1.0
M_BH = 10.0
R_G = 2 * G * M_BH / C**2
R_ERGO = 1.5 * R_G

# --- 2. DÉFINITION DES FORCES ---
def get_fractal_zpe_force(x, y):
    if abs(x) + abs(y) > 1e5: 
        return np.array([0.0, 0.0])
    c = complex(x / R_G, y / R_G) * 0.5
    z = 0.0j
    divergence = 0
    max_iter = 20
    for n in range(max_iter):
        z = z**2 + c
        if abs(z) > 2:
            divergence = n
            break
    amplitude = (max_iter - divergence) / max_iter
    angle = np.angle(z) if abs(z) > 0 else 0
    fx = amplitude * np.cos(angle + np.pi/2)
    fy = amplitude * np.sin(angle + np.pi/2)
    return np.array([fx * 0.1, fy * 0.1])

def mantissa_extraction(energy_value):
    epsilon = 1e-10
    val = abs(energy_value) + epsilon
    log_e = np.log10(val)
    mantisse = log_e - np.floor(log_e)
    lambda_growth = 1.5
    reproductive_factor = np.exp(lambda_growth * mantisse)
    return reproductive_factor

# --- 3. SIMULATION PRINCIPALE ---
def run_simulation(steps=1000):
    print("--- DEMARRAGE DE LA SIMULATION ---")
    pos = np.array([R_ERGO * 1.5, 0.0])
    vel = np.array([0.0, 0.5 * C])
    dt = 0.05
    trajectory = []
    energy_classic_log = []
    energy_reproductive_log = []
    time_log = []
    
    for t in range(steps):
        r = np.linalg.norm(pos)
        if r <= R_G:
            print(f">>> IMPACT SUR L'HORIZON (Temps {t*dt:.2f}) <<<")
            break
        force_grav = -G * M_BH * pos / (r**3)
        force_penrose = np.array([0.0, 0.0])
        if r < R_ERGO:
            tangent = np.array([-pos[1], pos[0]]) / r
            force_penrose = tangent * 0.05 * (R_ERGO - r) / R_ERGO
        force_zpe = get_fractal_zpe_force(pos[0], pos[1])
        total_force = force_grav + force_penrose + force_zpe
        vel += total_force * dt
        pos += vel * dt
        e_kin = 0.5 * np.linalg.norm(vel)**2
        e_pot = -G * M_BH / r
        e_classic = e_kin + e_pot
        if r < R_ERGO:
            e_rep = mantissa_extraction(e_classic)
        else:
            e_rep = 0.0
        trajectory.append(pos.copy())
        energy_classic_log.append(e_classic)
        energy_reproductive_log.append(e_rep)
        time_log.append(t * dt)
        
    return (np.array(trajectory), np.array(energy_classic_log), 
            np.array(energy_reproductive_log), np.array(time_log))

# --- 4. EXECUTION ET VISUALISATION ---
# Lancement
traj, e_class, e_rep, t = run_simulation()

# Graphiques
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))

# Gauche : Trajectoire
ax1.set_title("Trajectoire Cométaire & Ergosphère")
circle_bh = plt.Circle((0, 0), R_G, color='black', label='Horizon')
circle_ergo = plt.Circle((0, 0), R_ERGO, color='blue', fill=False, linestyle='--', label='Ergosphère')
ax1.add_patch(circle_bh)
ax1.add_patch(circle_ergo)
ax1.plot(traj[:, 0], traj[:, 1], 'r-', linewidth=1, label='Trajectoire')
ax1.set_xlim(-R_ERGO*2, R_ERGO*2)
ax1.set_ylim(-R_ERGO*2, R_ERGO*2)
ax1.set_aspect('equal')
ax1.legend()
ax1.grid(True)

# Droite : Énergie
ax2.set_title("Protocole Mantisse (Extraction)")
ax2.plot(t, e_class, label='Énergie Classique', color='gray', alpha=0.6)
ax2.plot(t, e_rep, label='Énergie Reproductive', color='red', linewidth=2)
ax2.fill_between(t, e_rep, color='red', alpha=0.2)
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.savefig("simulation_results.png")
print("--- SIMULATION TERMINEE : RESULTATS SAUVEGARDES ---")