# Building an Interactive Distance Measurement Tool in Python with OpenCV and Homography

**Workflow of the tool**
The interaction has two stages.
**Stage 1: Select the board corners**
The user clicks the four corners of the board in this order:
- Top-left
- Top-right
- Bottom-right
- Bottom-left
These four points are used to compute the perspective transformation.

**Stage 2: Measure distance**
After the warped image appears, the user clicks two points in the warped view.
The program then:
- draws a line between the two points,
- calculates the Euclidean distance,
- converts it from pixels to centimeters,
- and displays the result on the image.

<img width="1919" height="1027" alt="Screenshot 2026-03-10 154423" src="https://github.com/user-attachments/assets/65738a1b-20aa-4efc-98e4-b74b4d796917" />
<img width="1919" height="1028" alt="Screenshot 2026-03-10 154438" src="https://github.com/user-attachments/assets/11415a83-cbf2-4330-a35b-c3fd8ca93012" />
<img width="1919" height="1032" alt="Screenshot 2026-03-10 165706" src="https://github.com/user-attachments/assets/832102d1-c054-42b6-9dda-e2d97aac61b8" />
<img width="1917" height="1026" alt="Screenshot 2026-03-10 154448" src="https://github.com/user-attachments/assets/d232b8e3-3aed-4734-896f-d74182de2e66" />
