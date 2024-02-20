# Solomonoff induction

NOTE: This is outdated. I went with an n-gram model over bytes.

I'm writing a blog post about LLM's next-token prediction and Solomonoff induction. I want to write this blog post by only considering a finite set of possible functions for generating reality.
Reality will be a sequence of 0's and 1's that we will observe over "time".

The DGP of reality will be Markov chain with 8 states, where each state has two arrows out of it, kind of a sparse matrix. Here's the basic idea.

We have states {000,001,010,011,100,101,110,111}. We start off in state 000. If we observe 0 while in state (b1, b2, b3), we go to state (b2 b3 0), otherwise we observe a 1 and go to state (b2 b3 1). so, it's kind of like an LLM with a context length of 3. we see that each state only has two non-zero transition probabilities.

The DGP of reality will be specified by a specific probability transition matrix.
We will entertain a finite hypothesis (program) space for solomonoff induction, so that it's computable. We will consider other markov chains (exactly specified). We will consider simpler ones with context lengths of 2, 1, and 0   (context length 2 -> 2^2=4 states, context length 1 -> 2^1 = 2 states, context length 0 -> 2^0 = 1 state. for the one state we will consider a probability
transitiion matrix of [.5]. we'll work the other ones out as we go).

to do the solomonoff induction, i need to compute the KC for each stochastic model. i think i can make it a function of the entropy of the MC models?
so, I can compute the KC of each, so universal prior is computable, and then I can use DGP to generate sequence and show how next-bit (token) prediction works, using the universal prior and bayes rule for updating. as we observe more data (tokens or bits), some of these models will be designed to have zero probability, but others, including of course the DPG of reality, will have
a non-zero probability (compatible with the sequence so far observed). hopefully the DGP MC will be the one that has the highest posterior, but it may not. that's okay too. i imagine that eventually, after enough observations are made, it will... otherwise solomnoff induction has some explaining to do. ;->

then, after using solomonoff induction, i'd like to bring it back around to LLM's and their autoregressive model. that's also an MC. but clearly, since the space of possible programs they're considering is much larger, e.g., thousands of tokens (around 5000 i think) and context lengths in the thousands (and so |tokens|^(context length) states, but each state only has |tokens|
non-zero transition probabilities).

the universal prior over the restricted hypothesis space must be normalized, which is easy enough to do. (we're no longer taking the sum over every prefix-free program)

note that these are stochastic programs. we are generating PRNG values (biased coin flips) for each transition probability in DGP. we can either say that w/seed it is a deterministic program, or that each stochastic model represents compatibility with an infinite # of programs and we are averaging over them or selecting these entire classes and assigning equal weight to? i only mention this because i'm a bit confused but i must resolve it for the universal prior calculations and such.
