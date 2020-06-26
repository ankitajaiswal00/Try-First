# Try-First

The following project is an implementation of the paper "VITON: An Image-based Virtual Try-on Network" from University of Maryland, College Park, China. https://arxiv.org/abs/1711.08447

## Installation
### Prerequisites

```
PIL
PyTorch
TorchVision
tqdm
```

### Person representation extraction
The person representation used in this project are extracted by a 2D pose estimator and a human parser:
* [Realtime Multi-Person Pose Estimation](https://github.com/ZheC/Realtime_Multi-Person_Pose_Estimation)
* [Self-supervised Structure-sensitive Learning](https://github.com/Engineering-Course/LIP_SSL)


### 
Please downloads the Model files from the links provided below in the appropriate locations.

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




## References

[1] HAN X., WU Z., WU Z., YU R., DAVIS L. S.: Viton: An
image-based virtual try-on network. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (2018).  
[2] BROCK A., DONAHUE J., SIMONYAN K.: Large scale GAN
training for high fidelity natural image synthesis. In International Conference on Learning Representations (2019).  
[3] CAO Z., SIMON T., WEI S.-E., SHEIKH Y.: Realtime multiperson 2d pose estimation using part affinity fields. In Proceedings of the
IEEE Conference on Computer Vision and Pattern Recognition (2017).  
[4] GONG K., LIANG X., ZHANG D., SHEN X., LIN L.: Look
into person: Self-supervised structure-sensitive learning and a new benchmark for human parsing. In Proceedings of the IEEE Conference
on Computer Vision and Pattern Recognition (2017).  
[5] KARRAS T., LAINE S., AILA T.: A style-based generator architecture for generative adversarial networks. arXiv preprint
arXiv:1812.04948 (2018).  
[6] WANG B., ZHENG H., LIANG X., CHEN Y., LIN L., YANG
M.: Toward characteristic-preserving image-based virtual try-on network. In Proceedings of the European Conference on Computer Vision
(2018).
