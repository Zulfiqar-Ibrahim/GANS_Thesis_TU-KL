# GANS_Thesis_TU-KL
I am a student of Masters in Intelligent System in TU Kaiserslautern. This repo will contain all the research work related to my thesis in GANs. Before this endeavor, I have worked on a project to create a synthetic dataset. This dataset is used for the Yolo net's training. We had used Unreal Engin for simulation and Blender for 3D models of Sugarbeet plants. These models of sugar beet plants are placed in a simulated Farmland environment. A Camera is attached to a tractor that takes images of sugar beet planted in the soil.  Once the images are collected, I  then use the OpenCV python library for the creation of the dataset. 

Now, we are aiming to use Generative Adversarial Networks (GAN), a Deep learning approach to create an infinite amount of data with some variation. This task requires a deep understanding of such networks and the Maths behind them. There are many state-of-the-art GANs available in the market which can be used to fulfill our purpose. 

## Data Extraction Pipeline

In Kallstatd, Germany, We have visited the local apple orchard farm where we collected the videos through our robot. The ZED depth stereo cameras were used for this tasks. My task was then to design and develop pipeline using OpenCV and ZED toolkit which will extract images of focused objects (apple trees) from .svo files. ZED depth cameras have played huge role for the identification of such area within a frame. 

In this pipeline, first we have resized the frame width and height according to our need than we use Watershed technique for the segmentation since there are many false contours in Binary images.The watershed algorithm is a classic algorithm used for segmentation and is especially useful when extracting touching or overlapping objects in images, such as the coins in the figure above.Using traditional image processing methods such as thresholding and contour detection, we would be unable to extract each individual coin from the image — but by leveraging the watershed algorithm, we are able to detect and extract each coin without a problem.When utilizing the watershed algorithm we must start with user-defined markers. These markers can be either manually defined via point-and-click, or we can automatically or heuristically define them using methods such as thresholding and/or morphological operations.

Based on these markers, the watershed algorithm treats pixels in our input image as local elevation (called a topography) — the method “floods” valleys, starting from the markers and moving outwards, until the valleys of different markers meet each other. In order to obtain an accurate watershed segmentation, the markers must be correctly placed.


<p align="center">
  <img align="center" src="Images/watershed0.jpg" width="600" height="600">
</p>

The above frame is result of watershed algorithm on binary image that already contains depth information. Watershed allows to further enhance the boundary between background and foreground. Once the clear distinction between back/for ground is established we then moved to segmentation. 

<p align="center">
  <img align="center" src="Images/final_image1.jpg" width="600" height="600">
</p>

This is the final image after watershed and segmentation processes. As you can see closely that even the leaves are properly separated from background. This is necessary in image generation through GANs because GANs must observe important portion of image in order to regenerate the it.