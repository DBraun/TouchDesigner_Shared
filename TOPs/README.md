[//]: # (For development of this README.md, use http://markdownlivepreview.com/)

### 2D_texture_array_averager.tox - 2D Texture Array Averager
This will take a 2D Texture Array (from a Texture3D TOP) and add the layers together according to a geometric distribution. If the falloff is F, the most recent layer is weighted by 1.0, the second most recent by 1.0*F, the third by 1.0*F^2 and so on. If F is 1.0, then the result is like a Box Filter over the Cache (every layer is weighted equally). If F is 0.0, then only the most recent layer is shown.

### barrel_blur.tox - Barrel Blur
Lens distortion effect from [George Toledo](http://georgetoledo.com) (No license specified)

### barrel_blur_chroma.tox - Barrel Blur Chromatic Aberration
Lens distortion effect with chromatic aberration from [Mikkel Gjoel](http://loopit.dk) (No license specified)

### bitpacking.toe - Bitpacking
Convert a 16-bit R-channel to 8-bit RGBA (you need half has many pixels). Convert a 16-bit RGBA to 8-bit RGBA (you need twice as many pixels). There are also examples for converting in the opposite direction.

### BrushStrokes.toe - Brush Strokes
Based on a [Shadertoy](https://www.shadertoy.com/view/ldcSDB), use a reaction-diffusion buffer to spread colors in an image. (No license specified)

### color_palette_bch_trigonometric.tox - Color Palette BCH Trigonometric
http://iquilezles.org/www/articles/palettes/palettes.htm Use the TOP to CHOP to figure out what the parameters do. This uses the BCH color space. Behind the scenes it uses some extra trigonometry, but you can try to keep the parameters between 0 and 1. The final clamp occurs in RGB space.

### color_palette_rgb_trigonometric.tox - Color Palette RGB Trigonometric
http://iquilezles.org/www/articles/palettes/palettes.htm Use the TOP to CHOP to figure out what the parameters do.

### cube_map_cache.tox - Cube Map Cache
Wire a cube map into this component and cache it so that the cube map doesn't need to render continuously.

### gaussian_blur.tox - Gaussian Blur
Gaussian Blur with two-pass separated filter, variable filter size, and bilinear texture lookups. Code was adapted from [ofxBlur](https://github.com/kylemcdonald/ofxBlur/blob/master/src/ofxBlur.cpp)
[Derivative Thread](http://www.derivative.ca/Forum/viewtopic.php?f=4&t=9330&hilit=gaussian)

### GLSL_kaleidoscope.tox - Kaleidoscope
Kaleidoscopic effects with two modes and z-axis rotation. Code adapted from [Felix Turner](https://www.airtightinteractive.com/)

### GLSL_pack_packer.tox - GLSL Pack Packer
Combine multiple images of the same resolution into one image with a larger resolution. This might be useful for combining multiple images before a Touch Out TOP.

### GLSL_pack_unpacker.tox - GLSL Pack Unpacker
Undo the output from GLSL_pack_packer.

### GLSL_Replicator.tox - GLSL Replicator (Tame Impala Recursion)
With a single pass GLSL top, create psychedelic recursive images.
[Demo](https://vimeo.com/192831889)

### gridlines.tox - Grid lines
A GLSL Top for generating criss-crossing lines of a specific pixel width and spacing.

### hexagonal_grid.tox - Hexagonal Grid
Sample an image with a [hexagon grid](https://www.shadertoy.com/view/ls23Dc). (No license specified)

### kohonen.tox - Kohonen Self-Organizing Map (SOM)
I saw this [video](vimeo.com/189578632) by Reza Ali and thought I'd try my hand at it.
The tutorials most useful for me were [http://davis.wpi.edu/~matt/courses/soms/](http://davis.wpi.edu/~matt/courses/soms/) for overall info and [http://ai-junkie.com/ann/som/som1.html](http://ai-junkie.com/ann/som/som1.html) for code.
[Demo](https://vimeo.com/192259397)

### Kuwahara_paint.tox - Kuwahara Paint
Taken from [Shadertoy](https://www.shadertoy.com/view/MdyXRt). Overall effect is sort of painterly. Buffer A takes an image and adds noise. Buffer B calculates the median and deviation on some square kernel (default width 3). "Image" denoises using the Kuwahara filter.

### lookup_n_inputs.tox - Lookup N Inputs
Give a 2D grayscale and N images, and you'll receive a composite of the images. Black in the grayscale will show the first image, and whiter values will result in higher order images approaching the Nth image.

### movie_out_with_alpha.tox - Movie Out With Alpha
This component makes bottom-half-alpha images so that Movie File In TOPs elsewhere can treat the bottom half as alpha.

### tex_3d_multi_in.tox - Tex 3D Multi-in
This component takes any number of input TOPs and creates a Texture 3D holding all of them.