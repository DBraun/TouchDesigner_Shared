[//]: # (For development of this README.md, use http://markdownlivepreview.com/)

### ADSR_Lookup.tox - ADSR Lookup CHOP
It resembles the Attack, Decay, Sustain, Release envelope of a synthesizer.

### almostIdentity.tox - Almost Identity Lookup CHOP
A lookup CHOP that's almost linear. You can specify a crossover point at which it becomes linear, but before that it will be cubic and start at a specific minimum. Code from [Inigo Quilez](http://www.iquilezles.org/www/articles/functions/functions.htm)

### random_sample.tox - Random Sample
Select N random samples of a CHOP with any number of channels and any number of samples.

### sCurve.tox - sCurve Lookup CHOP
The sCurve from the TD Palette but implemented in GLSL. It generates a CHOP that's useful for the Lookup CHOP. You can also look at the source GLSL and adapt it for custom shaders. It's like a parameterized easing function.