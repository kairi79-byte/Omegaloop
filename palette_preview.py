import matplotlib.pyplot as plt
import matplotlib.patches as patches

palettes = {
    "1. Oxford Chalk & Slate (Clean Academic)": {
        "Background": "#F8FAFC",
        "Sidebar / Cards": "#F1F5F9",
        "Border Slate": "#CBD5E1",
        "Primary Navy": "#0F172A",
        "Accent Royal Blue": "#2563EB"
    },
    "2. Nordic Quantum Teal (Modern Lab)": {
        "Background": "#F0FDF4",
        "Sidebar / Cards": "#E2E8F0",
        "Border Mint": "#A7F3D0",
        "Primary Dark Slate": "#1E293B",
        "Accent Emerald Teal": "#0D9488"
    },
    "3. Solar Quantized Amber (Vintage Archive)": {
        "Background": "#FFFBEB",
        "Sidebar / Cards": "#FEF3C7",
        "Border Warm Gray": "#D6D3D1",
        "Primary Deep Walnut": "#292524",
        "Accent Warm Amber": "#B45309"
    }
}

fig, axes = plt.subplots(3, 1, figsize=(10, 6), facecolor="#FFFFFF")
fig.suptitle("OmegaLoop Light Theme Palettes", fontsize=14, fontweight="bold", y=0.98)

for idx, (name, colors) in enumerate(palettes.items()):
    ax = axes[idx]
    ax.set_title(name, loc="left", fontsize=11, fontweight="bold", pad=8)
    ax.set_xlim(0, len(colors))
    ax.set_ylim(0, 1)
    ax.axis("off")
    
    for c_idx, (role, hex_code) in enumerate(colors.items()):
        rect = patches.Rectangle((c_idx, 0), 0.9, 0.75, facecolor=hex_code, edgecolor="#94A3B8", linewidth=1.5, rx=0.08)
        ax.add_patch(rect)
        # Determine readable text color
        text_color = "#FFFFFF" if role in ["Primary Navy", "Accent Royal Blue", "Primary Dark Slate", "Accent Emerald Teal", "Primary Deep Walnut", "Accent Warm Amber"] else "#0F172A"
        ax.text(c_idx + 0.45, 0.42, role, ha="center", va="center", color=text_color, fontsize=8, fontweight="bold")
        ax.text(c_idx + 0.45, 0.2, hex_code, ha="center", va="center", color=text_color, fontsize=7.5)

plt.tight_layout()
plt.show()