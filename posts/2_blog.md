Moser’s Circle Problem: When a Beautiful Pattern Breaks
A hands-on tour of chords, crossings, and the surprisingly delicate meaning of “maximum.”

There is a particular kind of mathematical surprise that feels almost like a magic trick: a sequence begins

$$
1,\ 2,\ 4,\ 8,\ 16,\ 31,\dots
$$

The first five terms suggest an obvious rule. Double the number each time. But the sixth term refuses to be
$32$; it is $31$. That small disagreement is the doorway into Moser’s circle problem.

## The question

Put $n$ points on a circle and connect every pair of points with a straight chord. How many regions can the
circle be divided into?

Try changing the number and arrangement of points below. The pale lines are all the chords, while the number
of regions is computed from the actual interior crossings in the picture.

[INSERT_CIRCLE_EXPLORER]

## Start with the easy count

Every pair of points determines one chord. The number of pairs is

$$
{n \choose 2} = \frac{n(n-1)}{2}.
$$

That counts the original lines, but not the pieces they create. A chord with several crossing points gets
split into several edges, and each new edge can help enclose a new face.

The crucial observation is that an interior crossing is determined by choosing four boundary points. Once
four points are selected, the two diagonals of their quadrilateral cross. So the number of potential
crossings is

$$
{n \choose 4}.
$$

If no three chords pass through the same interior point, all of those crossings are distinct. Euler’s
formula then turns the bookkeeping into

$$
F = 1 + {n \choose 2} + {n \choose 4},
$$

where $F$ is the number of regions, including the outside region.

## Why the pattern breaks

For $n=5$, the formula gives

$$
1 + {5 \choose 2} + {5 \choose 4} = 1 + 10 + 5 = 16.
$$

It is tempting to interpret that as evidence for powers of two. But with $n=6$,

$$
1 + {6 \choose 2} + {6 \choose 4} = 1 + 15 + 15 = 31.
$$

The missing region is not a mistake in the formula. It is the point: six points can be arranged so that
three different chords meet at one central crossing. Six choices of four points do not produce six distinct
crossings in that symmetric arrangement. Several expected intersections collapse into one, so the count drops.

In general position, where no three chords concur, the maximum is

$$
1 + {n \choose 2} + {n \choose 4}.
$$

For a specially arranged circle, the answer can be smaller. “How many regions?” needs the hidden qualifier
“for which placement of the points?”

## A useful habit

The pattern $1,2,4,8,16$ is not useless; it is a clue. But a clue is not a proof. The productive next move
is to ask an easier question:

* How many pairs of points are there?
* How many quadruples of points are there?
* What does each new chord do to the planar graph?

Those questions replace pattern-spotting with structure. The final formula is less visually obvious than
doubling, but it explains both the beautiful beginning and the exact place where it fails.

> A broken pattern can be better than a perfect one: it tells you where the geometry is hiding.

## Further viewing

This post is inspired by 3Blue1Brown’s video **“This pattern breaks, but for a good reason | Moser’s circle
problem.”** The interactive sketch above is an original companion: it lets you see why general position
matters instead of treating the formula as a sequence to memorize.
