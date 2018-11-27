[//]: # (For development of this README.md, use http://markdownlivepreview.com/)

### 2D_texture_array_averager.tox - 2D Texture Array Averager
This will take a 2D Texture Array (from a Texture3D TOP) and add the layers together according to a geometric distribution. If the falloff is F, the most recent layer is weighted by 1.0, the second most recent by 1.0*F, the third by 1.0*F^2 and so on. If F is 1.0, then the result is like a Box Filter over the Cache (every layer is weighted equally). If F is 0.0, then only the most recent layer is shown.

### a_b_tester.tox - A/B Tester TOP
A tool for A/B comparing of images. It has labels so you know whether you're looking at A or B.

### barrel_blur.tox - Barrel Blur
Lens distortion effect from [George Toledo](http://georgetoledo.com) (No license specified)

### barrel_blur_chroma.tox - Barrel Blur Chromatic Aberration
Lens distortion effect with chromatic aberration from [Mikkel Gjoel](http://loopit.dk) (No license specified)

### bitpacking.toe - Bitpacking
Convert a 16-bit R-channel to 8-bit RGBA (you need half has many pixels). Convert a 16-bit RGBA to 8-bit RGBA (you need twice as many pixels). There are also examples for converting in the opposite direction.

### bloom_filter.tox - Bloom Filter
My version of a bloom filter based on what I've read and seen in a few places. It thresholds an image, blurs it, levels it, and adds that top of the original image. It has two stages. The second stage uses the first blur pass as its input rather than the thresholded image. In this way, the blur is cumulative.

### Blur_and_Composite.toe - Blur and Composite
A condensed GLSL pipeline for blurring and compositing (over/under/max).

### BrushStrokes.toe - Brush Strokes
Based on a [Shadertoy](https://www.shadertoy.com/view/ldcSDB) by [Cornus Ammonis](https://twitter.com/cornusammonis), use a reaction-diffusion buffer to spread colors in an image. (licensed CC BY 4.0)

### censor_bar.tox - Censor Bar
Isolate a rectangular portion of an image and apply an effect to it. The rectangular zone can be rotated too.

### color_palette_bch_trigonometric.tox - Color Palette BCH Trigonometric
http://iquilezles.org/www/articles/palettes/palettes.htm Use the TOP to CHOP to figure out what the parameters do. This uses the BCH color space. Behind the scenes it uses some extra trigonometry, but you can try to keep the parameters between 0 and 1. The final clamp occurs in RGB space.

### color_palette_rgb_trigonometric.tox - Color Palette RGB Trigonometric
http://iquilezles.org/www/articles/palettes/palettes.htm Use the TOP to CHOP to figure out what the parameters do.

### cube_map_cache.tox - Cube Map Cache
Wire a cube map into this component and cache it so that the cube map doesn't need to render continuously. [Derivative Forum](http://www.derivative.ca/Forum/viewtopic.php?f=4&t=5935&hilit=render+demand)

### curl_noise_4D.tox - Curl Noise 4D
Curl noise of a Simplex 3D or 4D vector field. This is great for driving velocities in particle simulations.

### depth_of_field_pixelflow.toe - Depth of Field
Depth of field using a depth pass and a GLSL TOP. You can specify a plane-of-focus distance value or a UV from which you can infer the POF. Code is adapted from [PixelFlow](https://github.com/diwi/PixelFlow) (MIT License)

### dither_style.tox - Dither Style
8x8 Bayer matrix [dithering](http://devlog-martinsh.blogspot.se/2011/03/glsl-8x8-bayer-matrix-dithering.html).

### equirectangular_littleplanet_shader.tox - Equirectangular "Little Planet" Shader
Turn equirectangular images into "little planet" images. It has options for scale and X/Y rotation.

### feedback_HSV.tox - Feedback HSV
A condensed GLSL pipeline for HSV feedback.

### feedback_TOP_cross.tox - Feedback TOP Cross
A condensed GLSL pipeline for feedback with a Cross TOP.

### feedback_TOP_over.tox - Feedback TOP Over
A condensed GLSL pipeline for feedback with an Over TOP.

### flood_fill.tox - Flood Fill
An interactive tool for isolating sections of an image based on luminance or specific RGB channels.

### frozen_image_detector.tox - Frozen Image Detector
Detect if an image has stayed the same for too many frames. It's like an optimized Analyze TOP.

### gaussian_blur.tox - Gaussian Blur
Gaussian Blur with two-pass separated filter, variable filter size, and bilinear texture lookups. Code was adapted from [ofxBlur](https://github.com/kylemcdonald/ofxBlur/blob/master/src/ofxBlur.cpp)
[Derivative Thread](http://www.derivative.ca/Forum/viewtopic.php?f=4&t=9330&hilit=gaussian)

### GLSL_Cell_Rotate.tox - GLSL Cell Rotate
Divide an image into a grid of rectangular cells. Each cell can rotate on its own axis.

### GLSL_Kaleidoscope.tox - Kaleidoscope
Kaleidoscopic effects with two modes and z-axis rotation. Code adapted from [Felix Turner](https://www.airtightinteractive.com/)

### GLSL_Lookup_Table.tox - GLSL Lookup Table
It's like a stepped UV map and is useful for the Remap TOP.

### GLSL_Noise_Tile.tox - GLSL Noise Tile
Create tileable non-symmetrical noise.

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

### hilbert_curve_2D.tox - Hilbert Curve 2D
The 2D [https://en.wikipedia.org/wiki/Hilbert_curve](https://en.wikipedia.org/wiki/Hilbert_curve) at various iterations, as both TOPs and SOPs. Calculations were made with [scurve](https://github.com/cortesi/scurve)

### hilbert_curve_3D.tox - Hilbert Curve 3D
The 3D [https://en.wikipedia.org/wiki/Hilbert_curve](https://en.wikipedia.org/wiki/Hilbert_curve) at various iterations, as both TOPs and SOPs. Calculations were made with [scurve](https://github.com/cortesi/scurve)

### HSV_lookup.tox - HSV Lookup
Change the hue of an image based on a 2D lookup map.

### kohonen.tox - Kohonen Self-Organizing Map (SOM)
I saw this [video](vimeo.com/189578632) by Reza Ali and thought I'd try my hand at it.
The tutorials most useful for me were [http://davis.wpi.edu/~matt/courses/soms/](http://davis.wpi.edu/~matt/courses/soms/) for overall info and [http://ai-junkie.com/ann/som/som1.html](http://ai-junkie.com/ann/som/som1.html) for code.
[Demo](https://vimeo.com/192259397)

### Kuwahara_paint.tox - Kuwahara Paint
Taken from [Shadertoy](https://www.shadertoy.com/view/MdyXRt). Overall effect is sort of painterly. Buffer A takes an image and adds noise. Buffer B calculates the median and deviation on some square kernel (default width 3). "Image" denoises using the Kuwahara filter.

### lookup_n_inputs.tox - Lookup N Inputs
Give a 2D grayscale and N images, and you'll receive a composite of the images. Black in the grayscale will show the first image, and whiter values will result in higher order images approaching the Nth image.

### Mask_Effect.tox - Mask Effect
A utility for when you want to use a Circle TOP and a Matte TOP.

### movie_out_with_alpha.tox - Movie Out With Alpha
This component makes bottom-half-alpha images so that Movie File In TOPs elsewhere can treat the bottom half as alpha.

### normals_pass_edge_detect.toe - Normals Pass Edge Detect
Render the normals of geometry to RGB and do an edge detection. This is sometimes a good way to get a cartoony wireframe effect.

### OpticalFlow.tox - Optical Flow
Optical Flow visualizes the movement in an image. The red channel represents horizontal motion, and the green channel represents vertical motion. This tox also provides two debug modes for fine-tuning the optical flow parameters. The first mode is "Normal", which uses arrows to indicate the velocity around a region. The second mode is "Shading" which puts bright colors in high-motion areas and leaves inactive areas alone. Major portions of this tox come from reading the source code of [PixelFlow](https://github.com/diwi/PixelFlow/) (MIT License). Beware that the output is just an Red-Green channel image.

### perceptual_color.tox - Perceptual Color
Why look at grayscale when you can look at color? This component contains color palettes come from [here](https://github.com/politiken-journalism/scale-color-perceptual).

### pixel_sorting.toe - Pixel Sorting
A starting point for sorting pixels in an image or video. [Derivative Thread](http://www.derivative.ca/Forum/viewtopic.php?f=4&t=9006&hilit=pixel+sorting)

### RGB_Separate.tox - RGB Separate
Break an image into three different sums of colors (default would be R-G-B). Afterward, translate the three channels separately and add them back together.

### SlitScanSimplest.tox - Slit Scan Simplest
A simple slit scan effect based on [Static No.19](https://vimeo.com/77768949) by Daniel Crooks

### tex_3d_multi_in.tox - Tex 3D Multi-in
This component takes any number of input TOPs and creates a Texture 3D holding all of them.

### trigger_chop_vis.tox - Trigger Chop Visualization
This component visualizes the parameters of a trigger CHOP with a familiar ADSR curve.### velocity_line_visualizer.tox - Velocity Line Visualizer
Renders a velocity map as a field of lines that point in the direction of the region's velocity. Code is adapted from [PixelFlow](https://github.com/diwi/PixelFlow/). (MIT License)

### velocity_surface_shader.tox - Velocity Surface Shader
Renders a velocity map as a colorful image. Code is adapted from [PixelFlow](https://github.com/diwi/PixelFlow/). (MIT License)