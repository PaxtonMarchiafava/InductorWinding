# Inductor Winding

At Humber College, the capstone project in the Electromechanical Engineering Technology program is a two-semester team-based project where students design and build real-world automation systems. Our project involves designing and building an automated inductor winding cell using a FANUC robot, a Cognex vision system, and SICK safety scanners. The goal is to streamline the production of inductors by automating the precise placement and winding of copper with an air core.

 - FANUC Robot: Handles inductor loading/unloading and wire positioning.
 - Cognex Camera: Verifies wire orientation and alignment before winding, ensuring quality control.
 - SICK Safety Scanners: Provide perimeter safety monitoring and zone control, allowing safe human interaction during operation and maintenance.

The system features an HMI to run the system, and pulls an "order" from a spreadsheet to generate coil properties like inductance, current limits, or size restrictions.

## Mechanical
**See drawings [here](../ENGINEERING/MECHANICAL.pdf)**

The mechanical design of the inductor winding cell is built on an aluminum extrusion frame for modularity and ease of assembly. A custom 3D-printed winding assembly driven by a stepper servo motor handles the coil winding process. DC motors feed wire through steel brake lines, which guide it around the lathe chuck like structure. A FANUC robot moves the inductors between stations, while hot glue is applied to secure the windings. The system integrates all components into a compact, efficient layout optimized for automated coil production.


## Electrical
**See drawings [here](..\ENGINEERING\ELECTRICAL.pdf)**

## The Team
to add:
camera, hmi

### Paxton Coghlin
<a href="..\TeamInfo\Paxton\Resume.pdf"><img src="..\TeamInfo\Paxton\Portrait.JPG" alt="Paxton Coghlin" style="height:360px;"></a>
 - Team Lead
 - PLC Lead

### Grant Maddock
<a href="..\TeamInfo\Paxton\Resume.pdf"><img src="..\TeamInfo\Grant\Portrait.JPG" alt="Paxton Coghlin" style="height:360px;"></a>
 - Robotics Lead

### Josh Le Blanc
<a href="..\TeamInfo\Paxton\Resume.pdf"><img src="..\TeamInfo\Josh\Portrait.JPG" alt="Paxton Coghlin" style="height:360px;"></a>
 - Mechanical Lead

### Jaidan Mitchell
<a href="..\TeamInfo\Paxton\Resume.pdf"><img src="..\TeamInfo\Jaidan\Portrait.JPG" alt="Paxton Coghlin" style="height:360px;"></a>
 - Safety Lead

### Rushawn Waite
<a href="..\TeamInfo\Paxton\Resume.pdf"><img src="..\TeamInfo\Shawn\Portrait.JPG" alt="Paxton Coghlin" style="height:360px;"></a>
 - Electrical Lead