import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.integrate import simps

class MobiusStrip:
    def __init__(self, R, w, n):
        # Set up meshgrid using parametric equations
        self.R, self.w, self.n = R, w, n
        u, v = np.linspace(0, 2*np.pi, n), np.linspace(-w/2, w/2, n)
        self.u, self.v = np.meshgrid(u, v)
        self.x = (R + self.v * np.cos(self.u/2)) * np.cos(self.u)
        self.y = (R + self.v * np.cos(self.u/2)) * np.sin(self.u)
        self.z = self.v * np.sin(self.u/2)

    def surface_area(self):
        # Calculate Area via cross product of partial derivatives
        u, v = self.u, self.v
        dxdu = -(self.R + v*np.cos(u/2))*np.sin(u) - 0.5*v*np.sin(u/2)*np.cos(u)
        dydu = (self.R + v*np.cos(u/2))*np.cos(u) - 0.5*v*np.sin(u/2)*np.sin(u)
        dzdu = 0.5*v*np.cos(u/2)
        dxdv = np.cos(u/2)*np.cos(u)
        dydv = np.cos(u/2)*np.sin(u)
        dzdv = np.sin(u/2)
        dA = np.sqrt((dydu*dzdv-dzdu*dydv)**2 + (dzdu*dxdv-dxdu*dzdv)**2 + (dxdu*dydv-dydu*dxdv)**2)
        return simps(simps(dA, self.v[:,0], axis=0), self.u[0], axis=0)

    def edge_length(self):
        # Calculate Edge length traced along both boundaries, and then sum up
        n2 = self.n*2
        u = np.linspace(0, 2*np.pi, n2)
        for v in [self.w/2, -self.w/2]:
            x = (self.R + v*np.cos(u/2))*np.cos(u)
            y = (self.R + v*np.cos(u/2))*np.sin(u)
            z = v*np.sin(u/2)
            if v == self.w/2:
                xe, ye, ze = x, y, z
            else:
                xe = np.concatenate([xe, x[::-1]])
                ye = np.concatenate([ye, y[::-1]])
                ze = np.concatenate([ze, z[::-1]])
        segs = np.sqrt(np.diff(xe)**2 + np.diff(ye)**2 + np.diff(ze)**2)
        return np.sum(segs)

    def plot(self):
        # 3D plot of Mobius Strip with gradient color and colorbar
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')
        norm = plt.Normalize(self.u.min(), self.u.max())
        colors = cm.plasma(norm(self.u))
        surf = ax.plot_surface(self.x, self.y, self.z, facecolors=colors, edgecolor='none', alpha=1.0)
        mappable = cm.ScalarMappable(cmap=cm.plasma, norm=norm)
        mappable.set_array([])
        fig.colorbar(mappable, ax=ax, orientation='vertical', fraction=0.03, pad=0.08, label="u parameter (angle)")
        
        # Plot edge in red
        n2 = self.n*2
        u = np.linspace(0, 2*np.pi, n2)
        for v in [self.w/2, -self.w/2]:
            x = (self.R + v*np.cos(u/2))*np.cos(u)
            y = (self.R + v*np.cos(u/2))*np.sin(u)
            z = v*np.sin(u/2)
            if v == self.w/2:
                xe, ye, ze = x, y, z
            else:
                xe = np.concatenate([xe, x[::-1]])
                ye = np.concatenate([ye, y[::-1]])
                ze = np.concatenate([ze, z[::-1]])
        ax.plot(xe, ye, ze, 'r', lw=2)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Mobius Strip')
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    m = MobiusStrip(R=1.0, w=0.4, n=200)
    print(f"Surface area: {m.surface_area():.4f}")
    print(f"Edge length: {m.edge_length():.4f}")
    m.plot()