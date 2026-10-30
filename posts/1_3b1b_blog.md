3B1B Blog
Notes on visual mathematics, intuition, and the ideas behind 3Blue1Brown.

This is the home for the 3Blue1Brown blog. Replace this text with your first
post, or add another Markdown file to the `posts/` folder when you are ready
for a second page.

## Start writing

Write normally in Markdown. Inline mathematics such as $a^2 + b^2 = c^2$ and
display mathematics work automatically:

$$
\int_0^1 x^2\,dx = \frac{1}{3}
$$

The existing page styling is shared by every file in this folder, so content
can change without touching the application code.

An interactive look at taking the logarithm of an image.

M.C. Escher's 1956 lithograph, "The Print Gallery," presents an impossible topological paradox: a young man stands in an art gallery, looking at a print of a ship in a harbor, only for that harbor city to warp around and contain the very gallery he is standing inside. 

To create this mind-bending looping expansion, Escher relied on an intuitive understanding of structural self-similarity. Decades later, mathematicians proved that the underlying grid structure is explicitly modeled by complex analysis—specifically by taking the complex logarithm of a standard image grid.

<div class="scrolly-container">
  <!-- The Sticky Visual Stage: Stays pinned on screen while user scrolls -->
  <div class="visual-stage">
    <div class="image-wrapper">
      <img src="https://wikimedia.org" alt="M.C. Escher Print Gallery" />
    </div>
  </div>

  <!-- The Narrative Track: Normal scrolling text cards that trigger the transitions -->
  <div class="narrative-track">
    <div class="narrative-card">
      <h3>1. The Flat Composition</h3>
      <p>We begin with the full composition. On the macroscopic layer, the lines are straight on the left and right margins, but they twist violently as they converge inward toward an empty central point.</p>
    </div>
    
    <div class="narrative-card">
      <h3>2. Zooming to the Observer</h3>
      <p>As you scroll deeper, look down at the bottom-right corner. A young client is standing inside an art house, gazing at a print hanging on the wall. This print represents the beginning of the mathematical mapping transformation.</p>
    </div>
    
    <div class="narrative-card">
      <h3>3. Diving into the Complex Log Matrix</h3>
      <p>Following the lines upward and left, the canvas stretches conformally. Local intersections remain at exactly 90 degrees, but the viewport expands exponentially, completing a closed loop that re-enters the boy's own head from the top down.</p>
    </div>
  </div>
</div>

<style>
/* 1. Structural Scrollytelling Grid Layout */
.scrolly-container {
  display: grid;
  grid-template-columns: 1.2fr 1.8fr;
  gap: 2rem;
  margin: 4rem 0;
  position: relative;
  /* Gives the page enough height to scroll through the animation progress */
  height: 300vh; 
}

/* 2. Sticky Stage: Keeps the image static while the narrative scrolls */
.visual-stage {
  position: sticky;
  top: 10vh;
  height: 75vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background: #FAF9F6;
  border: 1px solid #D9D6CE;
  border-radius: 4px;
}

/* 3. Image Wrapper with Native CSS View Timeline mapping */
.image-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  /* Binds the transform animation directly to the container scroll status */
  animation: escherZoomTour linear;
  animation-timeline: scroll(root);
}

.image-wrapper img {
  width: 90%;
  height: auto;
  object-fit: contain;
  transition: filter 0.3s ease;
}

/* 4. Text Layout Setup running down the left flank */
.narrative-track {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
  padding-bottom: 25vh;
}

.narrative-card {
  background: rgba(250, 249, 246, 0.95);
  border-left: 2px solid #B45635;
  padding: 1.5rem;
  margin-bottom: 45vh;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02);
}

.narrative-card h3 {
  margin-top: 0 !important;
  color: #1E1E1E;
}

/* 5. Keyframes: Maps exact canvas scale and translation adjustments based on scroll % */
@keyframes escherZoomTour {
  0% {
    transform: scale(1) translate(0, 0);
  }
  45% {
    /* Zooms smoothly and shifts view focus down to the boy in the lower right corner */
    transform: scale(2.8) translate(-22%, -18%);
  }
  90%, 100% {
    /* Blows up the canvas magnification pushing directly through the center twist hole */
    transform: scale(8.5) translate(28%, 8%);
  }
}

/* Responsive adjustments for handheld layouts */
@media (max-width: 768px) {
  .scrolly-container {
    display: flex;
    flex-direction: column;
    height: auto;
  }
  .visual-stage {
    position: relative;
    top: 0;
    height: 40vh;
  }
  .image-wrapper {
    animation: none; /* Fallback for mobile screen sizes */
  }
}
</style>

Continuing down past the interactive canvas block, the layout seamlessly returns back to normal content flow.
