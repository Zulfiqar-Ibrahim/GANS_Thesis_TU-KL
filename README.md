# GANS_Thesis_TU-KL
I am a student of Masters in Intelligent System in TU Kaiserslautern. This repo will contain all the research work related to my thesis in GANs. Before this endeavor, I have worked on a project to create a synthetic dataset. This dataset is used for the Yolo net's training. We had used Unreal Engin for simulation and Blender for 3D models of Sugarbeet plants. These models of sugar beet plants are placed in a simulated Farmland environment. A Camera is attached to a tractor that takes images of sugar beet planted in the soil.  Once the images are collected, I  then use the OpenCV python library for the creation of the dataset. 

Now, we are aiming to use Generative Adversarial Networks (GAN), a Deep learning approach to create an infinite amount of data with some variation. This task requires a deep understanding of such networks and the Maths behind them. There are many state-of-the-art GANs available in the market which can be used to fulfill our purpose. 

## Data Extraction Pipeline

In Kallstatd, Germany, We have visited the local apple orchard farm where we collected the videos through our robot. The ZED depth stereo cameras were used for this tasks. My task was then to design and develop pipeline using OpenCV and ZED toolkit which will extract images of focused objects (apple trees) from .svo files. ZED depth cameras have played huge role for the identification of such area within a frame. 


