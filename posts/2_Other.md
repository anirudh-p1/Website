Superposition
How a small number of dimensions can carry a crowded vocabulary of features.

Interpretability often begins with a strange visual question: what happens when a model has more useful features than it has dimensions to represent them?

In a toy feature space, vectors can share directions while remaining recoverable through their geometry. The cost is interference. The reward is a compact representation.

For a matrix of activations $X$, a useful first diagnostic is the Frobenius norm:

$$
\lVert X \rVert_F = \sqrt{\sum_{i,j} |X_{ij}|^2}
$$

The sketch below is deliberately small. Increase the density to see more feature directions competing for the same representational space.

[INSERT_PLOT_SUPERPOSITION]

The plot is a placeholder for a larger investigation: when does sparsity make superposition legible, and when does it become a source of brittle behavior?
