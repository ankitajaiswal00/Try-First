
MaskTheFace is computer vision-based script to mask faces in images. It uses a dlib based face landmarks detector to identify the face tilt and six key features of the face necessary for applying mask. Based on the face tilt, corresponding mask template is selected from the library of mask. The template mask is then transformed based on the six key features to fit perfectly on the face. The complete block diagram can be seen below. MaskTheFace provides a number of masks to select from. It is difficult to collect mask dataset under various conditions. MaskTheFace can be used to convert any existing face dataset to masked-face dataset. MaskTheFace identifies all the faces within an image, and applies the user selected masks to them taking into account various limitations such as face angle, mask fit, lighting conditions etc. A single image, or entire directory of images can be used as input to code.


### Arguments
|    Argument    |                                                                                                       Explanation                                                                                                       |
|:--------------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
|      path      |                                                                            Path to the image file or a folder containing images to be masked                                                                            |
|    mask_type   | Select the mask to be applied. Available options are 'N95', 'surgical_blue', 'surgical_green', 'cloth', 'empty' and 'inpaint'. The details of these mask types can be seen in the image above. More masks will be added |
|     pattern    |                                 Selects the pattern to be applied to the mask-type selected above. The textures are available in the masks/textures folder. User can add more textures.                                 |
| pattern_weight |                                   Selects the intensity of the pattern to be applied on the mask. The value should be between 0 (no texture strength) to 1 (maximum texture strength)                                   |
|      color     |                                                         Selects the color to be applied to the mask-type selected above. The colors are provided as hex values.                                                         |
|  color_weight  |                                      Selects the intensity of the color to be applied on the mask. The value should be between 0 (no color strength) to 1 (maximum color strength)                                      |
|      code      |                                                              Can be used to create specific mask formats at random. More can be found in the section below.                                                             |
|     verbose    |                                                                          If set to True, will be used to display useful messages during masking                                                                         |
|write_original_image|                   If used, the original unmasked image will also be saved in the masked image folder along with processed masked image                                                                              |

### Explanation:


## Supported Masks:
### Mask Types:
Currently MaskTheFace supports the following 4 mask types
1. Surgical
2. N95
3. KN95
4. Cloth
5. Gas


### Mask Variations:
Each of the mask types mentioned above can be varied in the following terms to create even more masks
#### 1. Textures/Patterns variations:
MaskTheFace provides 24 existing patterns that can be applied to mask types above to create more variations of the graph. Moreover, users can easily add custom patterns following the guidelines provided.

#### 2. Color variations:
MaskTheFace provided script to modify existing mask types in terms of colors to generate variations of existing graphs.

####  3. Intensity variations:
MaskTheFace provided script to modify existing mask types in terms of intensity to generate variations of existing graphs.



## Features:
### Support for multiple mask types

### Support for both single and multi-face images:

### Wide face angle coverage

### Brightness corrected mask application

### Bulk masking on datasets




