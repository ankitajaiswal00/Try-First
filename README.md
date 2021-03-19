# Try-First

The following project is an implementation of the paper "VITON: An Image-based Virtual Try-on Network" from University of Maryland, College Park, China. https://arxiv.org/abs/1711.08447

## Table of contents
* [Introduction](#Introduction)
* [Implementation Details](#Implementation_Details)
* [Training Process](#Training_Process)
* [Installation](#Installation)

## Introduction:-
TryFirst is an interactive web-app which benefits users by allowing them to try-on a particular cloth to see how it suits them.
Thus, allowing consumers to virtually try on clothes will not only enhance their shopping experience, transforming the way
people shop for clothes, but also save cost for retailer. 

## Features:-
* Users can avail the option to try apparels virtually
* Similarily, one can try face masks virtually
* Size recommending model to solve queries regarding differennt size charts from different brands.


## Implemenetation_details
* Pose Generation using openpose.
* Parser are generated using SS-nan (opensource pre-trained model) . 
* Used Generative Adversarial Networks with Adversarial loss, perceptual loss and L1 loss for smoothening.
* Used U-Net for generator and a downsampler for discriminator.

## Training Process
* The pose generated and parser and person image are concatenated along with and cloth imgae are fedded to GMM.
* output of above is a warped cloth.
* Now that concatenated image along with warped cloth is feeded to Gans.
* Final output is image of person wearing desired cloth.
* Final loss of generator on validation : 3.62001
* Final loss of discriminator on validation :0.003821
* Epochs Trained : 50
* Optimizer : Ranger

## Installation
### Prerequisites

```
PIL
PyTorch
TorchVision
tqdm
dlib
OpenCV
```

### Person representation extraction
The person representation used in this project are extracted by a 2D pose estimator and a human parser:
* [Realtime Multi-Person Pose Estimation](https://github.com/ZheC/Realtime_Multi-Person_Pose_Estimation)
* [Self-supervised Structure-sensitive Learning](https://github.com/Engineering-Course/LIP_SSL)


### 
Download the Model files from the links provided below in the appropriate locations.

1. <a href="https://drive.google.com/file/d/1u_Sih08XFxl0DTBzd7oXBqKiDsTNcp_x/view?usp=sharing">TOM Model</a>
2. <a href="https://drive.google.com/file/d/1u-t_gMOve8ZzT_lGGWg04vWkJAEb2qx-/view?usp=sharing">GMM Model</a>
3. <a href="https://drive.google.com/file/d/1JO_PU2ZD-Jgs9egWQQOnXX92OOodIsyx/view?usp=sharing">Pose Vector Model</a>
4. <a href="https://drive.google.com/file/d/1bOEbiJgxshbaNFrrw-Ek-dfcC_tKb27R/view?usp=sharing">Pose Parser Model</a>


### Download repository
```
$ git clone https://github.com/JaZz-9/Try-First
```

After adding the models, run the following command:

1. Installing all the pre-requisite libraries.
```bash
pip install -r requirements.txt
```
2. Executing model using streamlit script
```
streamlit run app.py
```
               
 
## To localhost the website:
To run the Web-App: 
``` 
python main.py

```

## Screenshots From Website:
<br>
HomePage:
<img src='https://github.com/JaZz-9/Try-First/blob/master/Outputs/website%20ss/homepg.png' /> <t>
  
Collection:
<img src='https://github.com/JaZz-9/Try-First/blob/master/Outputs/website%20ss/collection.png' /> <br>
          
Size Predictor:
<img src='https://github.com/JaZz-9/Try-First/blob/master/Outputs/website%20ss/size%20predictor%20form.png' /><br>

Mask the Face
<img src='https://github.com/JaZz-9/Try-First/blob/master/Outputs/website%20ss/mashtheface.png'/><br>

## Outputs
<img src='https://github.com/hackabit19/Fakes/blob/master/Results/000164_0.jpg' /></t><img src='https://github.com/hackabit19/Fakes/blob/master/Results/000164_0.png' /><img src='https://github.com/hackabit19/Fakes/blob/master/Results/000568_1.jpg' />
</br>



## References
[1] Bochao Wang, Huabin Zheng, Xiaodan Liang, Yimin Chen: Toward Characteristic-Preserving Image-based Virtual Try-On Network (2020). 
[2] HAN X., WU Z., WU Z., YU R., DAVIS L. S.: Viton: An
image-based virtual try-on network. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (2018).  
[3] BROCK A., DONAHUE J., SIMONYAN K.: Large scale GAN
training for high fidelity natural image synthesis. In International Conference on Learning Representations (2019).  
[4] CAO Z., SIMON T., WEI S.-E., SHEIKH Y.: Realtime multiperson 2d pose estimation using part affinity fields. In Proceedings of the
IEEE Conference on Computer Vision and Pattern Recognition (2017).  
[5] GONG K., LIANG X., ZHANG D., SHEN X., LIN L.: Look
into person: Self-supervised structure-sensitive learning and a new benchmark for human parsing. In Proceedings of the IEEE Conference
on Computer Vision and Pattern Recognition (2017).  
[6] KARRAS T., LAINE S., AILA T.: A style-based generator architecture for generative adversarial networks. arXiv preprint
arXiv:1812.04948 (2018).  
[7] WANG B., ZHENG H., LIANG X., CHEN Y., LIN L., YANG
M.: Toward characteristic-preserving image-based virtual try-on network. In Proceedings of the European Conference on Computer Vision
(2018).
