# Sequence to Sequence Network
## Next generation Neural Network.

 Traditional neural networks use a weight calculation to achieve their
functionality. This method is very processor intensive, and one needs to
be trained with exposing the data to the neural network thousands of times,
at great cost.

  Biological neural networks mostly need a single exposure to new
information. This questions the weight method, as the optimal solution to
this problem domain.

  Another questionable item is the process of training. It relies on
subtle changes to the weights by using back propagation, calculating the
reverse derivative of the transfer function. We do not believe that nature
uses such a complex internal working to achieve functionality of the neural
network.

## The S2S method.

  At the heart of the neural network operation, the network can be
conceptualized a Sequence to Sequence operation. This is easily achieved
in the S2S by remembering the input sequence and the output sequence, and execute
a look up on the closest match.

 The advantages are multi fold.

 - No training required:

    The data is exposed to the S2S system once, and done.

 - Only store, add,  and subtract operations are  needed:

    The simplicity of operators is a further ease of hardware implementation.

 - Possibility to signal 'no match' condition:

  Signalling 'no match' condition is useful for redirecting the flow of
'thinking' to an alternate path.

 - Traceable, predictable decision making:

 The match can always be traced to a particular memorized (trained) item. No more
uncertainty where a particular result came from.

| File | Function | Notes |
| ----- | ----- | ---- |
|s2snp.py | Main S2S implementation| Simple |


// EOF

