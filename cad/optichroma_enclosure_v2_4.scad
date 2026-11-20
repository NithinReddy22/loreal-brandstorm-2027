/*
================================================================================
LA ROCHE-POSAY OPTICHROMA™ v2.4 — PARAMETRIC HARDWARE CAD ENCLOSURE
================================================================================
Brand: La Roche-Posay | L'Oréal Brandstorm 2027
Playing Field 3: Reinvent the Doctor-Patient Relationship
Design Specification: Frozen Student Proof-of-Concept MVP
Material: Post-Consumer Recycled Polycarbonate (rPC) / Matte Black PETG

KEY GEOMETRIC & OPTICAL PARAMETERS:
1. Working Distance: 35.0 mm fixed optical standoff from camera plate to skin plane.
2. Anti-Blanching Standoff: 1.5 mm recessed annular ring (prevents capillary diascopy).
3. Dual LED Lightpipes: 45° incident angle for shadow-free darkfield illumination.
4. Cross-Polarizer Slots:
   - Analyzer Slot (Camera): Orthogonal 90° orientation.
   - Emitter Slots (LEDs): Symmetrical 0° orientation.
5. In-Frame Calibration Bay: 4x4 mm slot for 18% neutral gray ceramic disc.
6. Universal Mount: Modular spring clamp receiver + MagSafe ring alignment groove.
================================================================================
*/

$fn = 60; // Render resolution smoothness

// --- PARAMETRIC DIMENSIONS (in millimeters) ---
working_distance = 35.0;        // Optical centerline height
barrel_od = 32.0;               // Outer diameter of main baffle barrel
barrel_id = 27.0;               // Inner cavity diameter
wall_thickness = 2.5;           // Nominal wall thickness

// Anti-blanching contact geometry
recess_depth = 1.5;             // Recess height to prevent capillary blanching
annular_rim_od = 32.0;          // Outer skin contact ring diameter
annular_rim_id = 23.0;          // Central uncompressed diagnostic window

// Optical apertures and slots
camera_aperture_dia = 12.0;     // Optical port over phone sensor
analyzer_slot_w = 14.0;         // Camera polarizer sheet width
analyzer_slot_t = 0.8;          // Polarizer sheet thickness
led_polarizer_w = 8.0;          // LED polarizer width
led_polarizer_t = 0.8;          // LED polarizer thickness
calib_disc_w = 4.2;             // 18% neutral gray target bay width
calib_disc_depth = 1.2;         // Target pocket depth

// Lightpipe emitter parameters
led_angle = 45.0;               // Angle of incidence to skin normal
led_pocket_dia = 5.5;           // Nichia 757 / SMD emitter pocket
diffuser_slot_dia = 7.0;        // 0.5mm frosted PMMA diffuser slot

// Universal mounting flange
flange_w = 42.0;
flange_l = 52.0;
flange_t = 3.0;
magsafe_ring_od = 54.0;
magsafe_ring_id = 46.0;


// --- MAIN ENCLOSURE MODULE ---
module optichroma_barrel() {
    difference() {
        union() {
            // Main cylindrical optical baffle
            cylinder(h = working_distance, d = barrel_od);

            // Annular skin contact ring with rounded safety chamfer
            translate([0, 0, 0])
                cylinder(h = 3.0, d1 = annular_rim_od + 1.0, d2 = annular_rim_od);

            // Top mounting interface flange
            translate([-flange_w/2, -flange_l/2, working_distance - flange_t])
                cube([flange_w, flange_l, flange_t]);

            // MagSafe alignment ridge
            translate([0, 0, working_distance - 0.6])
                difference() {
                    cylinder(h = 0.6, d = magsafe_ring_od);
                    cylinder(h = 1.0, d = magsafe_ring_id, center = true);
                }

            // Dual 45° LED emitter lightpipe housings
            for (angle = [0, 180]) {
                rotate([0, 0, angle])
                translate([barrel_od/2 - 2, 0, working_distance * 0.45])
                rotate([0, led_angle, 0])
                    cylinder(h = 14.0, d = 9.0);
            }
        }

        // --- INTERNAL SUBTRACTIVE CUTOUTS ---

        // 1. Central optical viewing barrel (cavity)
        translate([0, 0, -1])
            cylinder(h = working_distance + 2, d = barrel_id);

        // 2. Anti-blanching 1.5mm recessed cavity
        // Leaves outer rim touching skin, but central 23mm floating 1.5mm above tissue
        translate([0, 0, -0.1])
            cylinder(h = recess_depth + 0.1, d = annular_rim_id);

        // 3. Camera aperture through top plate
        translate([0, 0, working_distance - flange_t - 1])
            cylinder(h = flange_t + 2, d = camera_aperture_dia);

        // 4. Orthogonal Analyzer Polarizer Sheet Slot (90° orientation)
        translate([-analyzer_slot_w/2, -analyzer_slot_w/2, working_distance - flange_t - analyzer_slot_t - 0.5])
            cube([analyzer_slot_w, analyzer_slot_w, analyzer_slot_t]);

        // 5. In-Frame 18% Neutral Gray Calibration Disc Bay
        // Positioned at the internal perimeter (top-left optical quadrant)
        translate([-barrel_id/2 + 1.0, -barrel_id/2 + 1.0, 1.0])
            cube([calib_disc_w, calib_disc_w, calib_disc_depth]);

        // 6. Dual LED Lightpipe bore channels, diffusers, and 0° polarizers
        for (angle = [0, 180]) {
            rotate([0, 0, angle])
            translate([barrel_od/2 - 2, 0, working_distance * 0.45])
            rotate([0, led_angle, 0]) {
                // Light bore into chamber
                translate([0, 0, -5])
                    cylinder(h = 24.0, d = led_pocket_dia);
                // Polarizer sheet slot (0° parallel to plane)
                translate([-led_polarizer_w/2, -led_polarizer_w/2, 6.0])
                    cube([led_polarizer_w, led_polarizer_w, led_polarizer_t]);
                // PMMA diffuser disc recess
                translate([0, 0, 8.0])
                    cylinder(h = 1.0, d = diffuser_slot_dia);
            }
        }

        // 7. Internal Anti-Reflective Micro-Fluting Grooves (Suppress internal stray flare)
        for (z = [4 : 3 : working_distance - 6]) {
            translate([0, 0, z])
                difference() {
                    cylinder(h = 0.8, d = barrel_id + 0.8);
                    cylinder(h = 1.0, d = barrel_id - 0.1, center = true);
                }
        }
    }
}


// --- UNIVERSAL SPRING-CLAMP ATTACHMENT ARM ---
module universal_spring_clamp() {
    clamp_w = 28.0;
    clamp_l = 48.0;
    pad_t = 8.0;

    translate([flange_w/2, -clamp_w/2, working_distance - flange_t]) {
        difference() {
            union() {
                // Cantilever clamp arm
                cube([18.0, clamp_w, flange_t]);
                // Downward clamping jaw
                translate([14.0, 0, -22.0])
                    cube([4.0, clamp_w, 22.0]);
                // Ergonomic thumb-lever
                translate([14.0, 0, flange_t])
                    rotate([0, -25, 0])
                        cube([12.0, clamp_w, 2.5]);
            }
            // Non-slip silicone grip pad recess
            translate([13.0, 2.0, -20.0])
                cube([1.5, clamp_w - 4.0, 18.0]);
        }
    }
}


// --- COMPLETE SYSTEM ASSEMBLY ---
module optichroma_complete_assembly() {
    color([0.15, 0.15, 0.15]) // Matte Black rPC Enclosure
        optichroma_barrel();

    color([0.20, 0.22, 0.25]) // Clamp arm
        universal_spring_clamp();

    // Visual demonstration of internal components (non-printable indicators)
    // 18% Gray Ceramic disc (Matte Gray)
    color([0.46, 0.46, 0.46])
        translate([-barrel_id/2 + 1.0, -barrel_id/2 + 1.0, 1.0])
            cube([calib_disc_w, calib_disc_w, calib_disc_depth - 0.2]);

    // Cross-Polarizer Analyzer Window (Polarized Tint)
    color([0.2, 0.4, 0.8, 0.5])
        translate([0, 0, working_distance - flange_t - 0.9])
            cylinder(h = 0.6, d = 11.5);
}

// Render complete assembly
optichroma_complete_assembly();
