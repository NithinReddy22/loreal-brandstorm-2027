"""
Generates standard 3D STL mesh for La Roche-Posay OptiChroma v2.4 Enclosure
==========================================================================
Produces a clean binary or ASCII STL file representing:
- 35mm optical barrel with 32mm OD and 27mm ID
- 1.5mm recessed annular anti-blanching contact rim
- Dual 45° LED emitter lightpipe housings
- Top camera mounting flange (42x52mm) with 12mm aperture
- Universal clamp arm
"""

import math
import os
import struct


def write_stl(filename, facets):
    """Writes facets as binary STL."""
    with open(filename, 'wb') as f:
        # 80 byte header
        header = b'OptiChroma v2.4 Enclosure (La Roche-Posay Brandstorm 2027)'.ljust(80, b'\0')
        f.write(header)
        # Number of triangles
        f.write(struct.pack('<I', len(facets)))
        for normal, v1, v2, v3 in facets:
            f.write(struct.pack('<fff', *normal))
            f.write(struct.pack('<fff', *v1))
            f.write(struct.pack('<fff', *v2))
            f.write(struct.pack('<fff', *v3))
            f.write(struct.pack('<H', 0))


def compute_normal(p1, p2, p3):
    u = (p2[0]-p1[0], p2[1]-p1[1], p2[2]-p1[2])
    v = (p3[0]-p1[0], p3[1]-p1[1], p3[2]-p1[2])
    nx = u[1]*v[2] - u[2]*v[1]
    ny = u[2]*v[0] - u[0]*v[2]
    nz = u[0]*v[1] - u[1]*v[0]
    l = math.sqrt(nx*nx + ny*ny + nz*nz)
    if l > 1e-6:
        return (nx/l, ny/l, nz/l)
    return (0.0, 0.0, 1.0)


def add_quad(facets, p1, p2, p3, p4):
    n1 = compute_normal(p1, p2, p3)
    n2 = compute_normal(p1, p3, p4)
    facets.append((n1, p1, p2, p3))
    facets.append((n2, p1, p3, p4))


def generate_cylinder(r1, r2, h, z_offset=0.0, segments=36):
    facets = []
    angles = [2.0 * math.pi * i / segments for i in range(segments)]
    for i in range(segments):
        a1 = angles[i]
        a2 = angles[(i + 1) % segments]
        
        # Wall quad
        b1 = (r1 * math.cos(a1), r1 * math.sin(a1), z_offset)
        b2 = (r1 * math.cos(a2), r1 * math.sin(a2), z_offset)
        t1 = (r2 * math.cos(a1), r2 * math.sin(a1), z_offset + h)
        t2 = (r2 * math.cos(a2), r2 * math.sin(a2), z_offset + h)
        add_quad(facets, b1, b2, t2, t1)
    return facets


def generate_tube(r_outer, r_inner, h, z_offset=0.0, segments=36):
    facets = []
    angles = [2.0 * math.pi * i / segments for i in range(segments)]
    for i in range(segments):
        a1 = angles[i]
        a2 = angles[(i + 1) % segments]

        # Outer wall
        ob1 = (r_outer * math.cos(a1), r_outer * math.sin(a1), z_offset)
        ob2 = (r_outer * math.cos(a2), r_outer * math.sin(a2), z_offset)
        ot1 = (r_outer * math.cos(a1), r_outer * math.sin(a1), z_offset + h)
        ot2 = (r_outer * math.cos(a2), r_outer * math.sin(a2), z_offset + h)
        add_quad(facets, ob1, ob2, ot2, ot1)

        # Inner wall
        ib1 = (r_inner * math.cos(a1), r_inner * math.sin(a1), z_offset)
        ib2 = (r_inner * math.cos(a2), r_inner * math.sin(a2), z_offset)
        it1 = (r_inner * math.cos(a1), r_inner * math.sin(a1), z_offset + h)
        it2 = (r_inner * math.cos(a2), r_inner * math.sin(a2), z_offset + h)
        add_quad(facets, it1, it2, ib2, ib1)

        # Bottom rim cap
        add_quad(facets, ob1, ib1, ib2, ob2)
        # Top rim cap
        add_quad(facets, ot1, ot2, it2, it1)
    return facets


def generate_box(dx, dy, dz, center_xy=True, z_offset=0.0):
    facets = []
    x0 = -dx / 2.0 if center_xy else 0.0
    x1 = dx / 2.0 if center_xy else dx
    y0 = -dy / 2.0 if center_xy else 0.0
    y1 = dy / 2.0 if center_xy else dy
    z0 = z_offset
    z1 = z_offset + dz

    # 6 faces
    add_quad(facets, (x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)) # bottom
    add_quad(facets, (x0, y0, z1), (x0, y1, z1), (x1, y1, z1), (x1, y0, z1)) # top
    add_quad(facets, (x0, y0, z0), (x0, y0, z1), (x1, y0, z1), (x1, y0, z0)) # front
    add_quad(facets, (x1, y1, z0), (x1, y1, z1), (x0, y1, z1), (x0, y1, z0)) # back
    add_quad(facets, (x0, y1, z0), (x0, y1, z1), (x0, y0, z1), (x0, y0, z0)) # left
    add_quad(facets, (x1, y0, z0), (x1, y0, z1), (x1, y1, z1), (x1, y1, z0)) # right
    return facets


def main():
    facets = []
    # 1. Main optical baffle barrel (working distance = 35mm, OD = 32mm, ID = 27mm)
    facets.extend(generate_tube(r_outer=16.0, r_inner=13.5, h=32.0, z_offset=1.5, segments=48))

    # 2. Recessed annular contact rim (1.5mm recess, outer OD = 32.5mm, inner ID = 23mm)
    facets.extend(generate_tube(r_outer=16.25, r_inner=11.5, h=1.5, z_offset=0.0, segments=48))

    # 3. Top camera flange plate (42x52x3mm at z=32mm to 35mm)
    facets.extend(generate_box(dx=42.0, dy=52.0, dz=3.0, center_xy=True, z_offset=32.0))

    # 4. Dual 45° LED lightpipe housings
    for sign in [-1, 1]:
        pipe = generate_box(dx=8.0, dy=9.0, dz=12.0, center_xy=True, z_offset=14.0)
        # Shift in x
        shifted = []
        for n, p1, p2, p3 in pipe:
            s1 = (p1[0] + sign * 15.0, p1[1], p1[2])
            s2 = (p2[0] + sign * 15.0, p2[1], p2[2])
            s3 = (p3[0] + sign * 15.0, p3[1], p3[2])
            shifted.append((n, s1, s2, s3))
        facets.extend(shifted)

    # 5. Universal mounting clamp arm
    clamp = generate_box(dx=16.0, dy=28.0, dz=3.0, center_xy=False, z_offset=32.0)
    shifted_clamp = []
    for n, p1, p2, p3 in clamp:
        s1 = (p1[0] + 21.0, p1[1] - 14.0, p1[2])
        s2 = (p2[0] + 21.0, p2[1] - 14.0, p2[2])
        s3 = (p3[0] + 21.0, p3[1] - 14.0, p3[2])
        shifted_clamp.append((n, s1, s2, s3))
    facets.extend(shifted_clamp)

    # Clamp downward jaw
    jaw = generate_box(dx=4.0, dy=28.0, dz=20.0, center_xy=False, z_offset=12.0)
    shifted_jaw = []
    for n, p1, p2, p3 in jaw:
        s1 = (p1[0] + 33.0, p1[1] - 14.0, p1[2])
        s2 = (p2[0] + 33.0, p2[1] - 14.0, p2[2])
        s3 = (p3[0] + 33.0, p3[1] - 14.0, p3[2])
        shifted_jaw.append((n, s1, s2, s3))
    facets.extend(shifted_jaw)

    out_path = os.path.join(os.path.dirname(__file__), "optichroma_enclosure_v2_4.stl")
    write_stl(out_path, facets)
    print(f"Generated {out_path} with {len(facets)} triangles ({os.path.getsize(out_path)} bytes)")


if __name__ == "__main__":
    main()
