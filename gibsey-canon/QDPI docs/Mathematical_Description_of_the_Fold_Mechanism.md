**Proof Sketch (≈ 300 words)**

1. **Gate Transformations as $\mathbf{Z}_4 \times \mathbf{Z}_4$.**
   Let the 2D lattice of “fold” shapes be acted on by two fundamental transformations:

   $$
     f_1:\text{(shape)} \;\mapsto\; \text{(shape rotated 90° inwards)},
     \quad
     f_2:\text{(shape)} \;\mapsto\; \text{(shape rotated 90° outwards)}.
   $$

   Because rotating four times (by 90° increments) returns the shape to its original form, each $f_i$ is of order 4.  Their compositions capture all 90° and 180° reorientations (including the identity), and these generate a subgroup isomorphic to $\mathbf{Z}_4 \times \mathbf{Z}_4$.

2. **Three “Roots” as a $\mathbf{(Z_2)^3}$ Factor.**
   Alongside rotational state, each glyph either includes or excludes each of three independent “root” components.  Denote by

   $$
     r_j : \text{glyph} \;\mapsto\; \text{glyph with the }j\text{-th root toggled on/off},
   $$

   for $j=1,2,3$.  Because toggling any root twice recovers the original glyph, each $r_j$ is of order 2.  Further, all three toggles commute, forming a subgroup isomorphic to $(\mathbf{Z}_2)^3$.

3. **Direct Product Structure.**
   Since the root toggles commute with the rotations (i.e.\ one can toggle a root before or after a 90° fold without changing the end result), the total symmetry group is the direct product

   $$
     G \;\cong\; (\mathbf{Z}_2)^3 \;\times\; \mathbf{Z}_4 \;\times\; \mathbf{Z}_4.
   $$

   Counting elements gives $\lvert G\rvert = 2^3 \times 4 \times 4 = 128$.
   (In many QDPI schemes, an additional flip or “mirror” adds another factor of $\mathbf{Z}_2$, bringing the total to 256 variants.)

4. **Entropy Gain vs. Base64.**

   * **Base64:** Each symbol conveys $\log_2(64)=6$ bits.  To encode 8 bits (1 byte), Base64 typically requires 2 symbols ($12$ bits of capacity, with 4 bits wasted if taken in isolation).
   * **QDPI Fold Glyphs:** Under perfect rendering, each distinct glyph represents one of 256 possible states, directly encoding $\log_2(256)=8$ bits in a single symbol.
     Thus, **QDPI** achieves a net of 8 bits per glyph versus 6 bits per Base64 character—a 33% increase in per-symbol information density.

---

```
         Compact Cayley Graph Sketch for G
         
         Let (r1,r2,r3) ∈ (Z2)^3 and (a,b) ∈ Z4 × Z4.
         A glyph is labeled by (r1,r2,r3; a,b).
         
         Generators:
           • x toggles r1
           • y toggles r2
           • z toggles r3
           • f1 increases a mod 4
           • f2 increases b mod 4
         
         Edges in the 256-node graph connect glyphs differing by exactly one generator.
```