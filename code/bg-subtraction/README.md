### Background subtraction
Two working examples of background subtraction.  The only two algorithms that
were installed with opencv by default appear to be MOG and KNN.  

Bot hof these algorthims have a lot of noise in the foreground mask.  Initial
attempts will be to get a different, more modern algorithm working (such as CNT)
followed by denoising and applying other pre-processing algorithms.

CNT is a no go, does not appear to be supported in opencv 4.1 (can only find a
github repo for it
[https://github.com/sagi-z/BackgroundSubtractorCNT](https://github.com/sagi-z/BackgroundSubtractorCNT).


