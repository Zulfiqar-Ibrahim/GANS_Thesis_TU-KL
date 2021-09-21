import cv2 as cv
import numpy as np
import os
from matplotlib import pyplot as plt
from pathlib import Path
import imutils
import re
import pyzed.sl as sl
import enum
import sys
from statistics import mean


# In[4]:


print('Check OpenCV version ',cv.__version__)


# In[28]:


class dataGenerationFromSVOfiles():
    '''
    This class is written to extract images from zed camera's files
   
    the extention of such files are .svo and require pyzed library to operate.
   
    This class read SVO sample to read the video and the information of the camera.
   
    It can pick a frame of the svo and save it as a JPEG or PNG file. Depth map and Point Cloud
   
    can also be saved into files.This generated data can also be saved at mentioned location
   
    for further use. We have used the watershed algorithm which is a classic algorithm used for
   
    segmentation and is especially useful when extracting touching or overlapping
   
    objects in images, such as the coins in the figure above.Using traditional image processing methods
   
    such as thresholding and contour detection, we would be unable to extract each individual
   
    coin from the image but by leveraging the watershed algorithm, we are able to detect
   
    and extract each coin without a problem.

    When utilizing the watershed algorithm we must start with user-defined markers.
   
    These markers can be either manually defined via point-and-click, or we can automatically or
   
    heuristically define them using methods such as thresholding and/or morphological operations.
   
   
    '''
   
    def __init__(self,folder_location,scale_percent,save_to_location):
       
        self.folder_location = folder_location
       
        self.init_parameter = sl.InitParameters()
       
        self.init_parameter.set_from_svo_file(self.folder_location)
       
        self.init_parameter.svo_real_time_mode = False
       
        self.init_parameter.depth_mode = sl.DEPTH_MODE.ULTRA
       
        self.init_parameter.coordinate_units = sl.UNIT.MILLIMETER
       
        self.scale_percent =  scale_percent
       
        self.save_to_location = save_to_location
       
        print("Saving to Location is ", save_to_location)
       
    def draw_rec(self,image_bw,image_rgb,image_index_green,image_index_blue,image_index_red):
        """
        this function is designed to draw rectangle on specific object in an image. There
       
        are many morphological operations being performed on binary image which helps to identify
       
        the main object. After these operation , we use findcontour function to narrow down our search and
       
        once the biggest contour is found, we then find the center(x,y) of that contour and draw rectangle around it.
       
        Parameters:
           
            image_bw: Binary image
           
            image_rgb: Normal rgb image
           
            image_index_green: Image counter
           
            image_index_blue: Image counter
           
            image_index_red: Image counter
       
        return =  0
        """
   
        cnts = cv.findContours(image_bw.copy(), cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
       
        cnts = imutils.grab_contours(cnts)
   
        cnts = sorted(cnts, key=cv.contourArea, reverse=True)
   
        rect_areas = []
   
        h_image_rgb, w_image_rgb,_ = image_rgb.shape
   
        w_image_rgb_50 = ( w_image_rgb / 100 ) * 50
   
        h_image_rgb_75 = ( h_image_rgb / 100 ) * 75
   
   
        check_height = True
   
   
        for c in cnts:
       
            (x, y, w, h) = cv.boundingRect(c)
       
            rect_areas.append(w * h)
       
        avg_area = mean(rect_areas)
   
        for c in cnts:
              
   
            M = cv.moments(c)
   
            cX = int(M["m10"] / M["m00"])
   
            cY = int(M["m01"] / M["m00"])
     
           
            rect = cv.boundingRect(c)
   
            x,y,w,h = rect
           
            cnt_area = w * h
       
       
            if cnt_area < 0.6 * avg_area:
           
                pass
       
       
            elif w > w_image_rgb_50 and h > h_image_rgb_75:
           
                if check_height == True:
           
                    wnew = int(w / 2)
           
                    #print(wnew)
           
                    x_new = x + wnew + 10
           
                    cv.rectangle(image_rgb,(x_new,y),(x+w,y+h),(0,255,0),0)
           
                    cv.rectangle(image_rgb,(x,y),(x+wnew,y+h),(255,0,0),0)
               
                    crop_image_green = image_rgb[y+1:y+h,x_new+1:x_new+w-1]
               
                    crop_image_blue = image_rgb[y+1:y+h,x+1:x+wnew-1]
               
                    #cv.imshow("Blue Cropped",crop_image_blue)
               
                    #cv.imshow("Green Cropped",crop_image_green)
                    if self.save_to_location :
               
                        cv.imwrite(os.getcwd()+"/2_fullrow/2_fullrow_croped_gr_"+str(image_index_green)+".jpg",crop_image_green)
                        #image_index_green = image_index_green + 1
               
                        cv.imwrite(os.getcwd()+"/2_backward_fullrow/2_fullrow_croped_bl_"+str(image_index_blue)+".jpg",crop_image_blue)
                        #image_index_blue = image_index_blue + 1
           
                    #print('height is ',h)
                else:
                    pass
       
            elif w < w_image_rgb_50 and h > h_image_rgb_75:
           
                if check_height == True:
               
                    crop_image_red = cv.rectangle(image_rgb,(x,y),(x+w,y+h),(0,0,255),0)
               
                    crop_image_red = image_rgb[y+1:y+h,x+1:x+w-1]
               
                    #cv.imwrite(os.getcwd()+"/2_fullrow/2_fullrow_croped_rd_"+str(image_index_red)+".jpg",crop_image_red)
              
               
                    #cv.imshow("Red Cropped",crop_image_red)
                else :
                    pass
           
            elif h < h_image_rgb_75:
               
                print('hight is low ',h)
               
                check_height = False
           
                pass
           

       
        return 0
       
    def readImagesAndResize(self):
        """
        This Function is written to read the images from .svo file and resize them with given numbers and also flipped
       
        them if we see images upside down. OpenCV implemented a marker-based watershed algorithm where we specify which
       
        valley points are to be merged and which are not. It is not an automatic but an interactive image segmentation.
       
        The "marker-based" means labeling where the region is a foreground or a background, and give different labels for
       
        our object we know. Using one color (or intensity), we label the region which we are sure of being the foreground
       
        or being background with another color. Then, for the region we are not sure of anything, label it with 0.
       
        That is our marker. After that, we apply watershed algorithm. Then our marker will be updated with the labels
       
        we gave and the boundaries of objects will have a value of -1.
       
        """
       
       
        cam = sl.Camera()
       
        err = cam.open(self.init_parameter)
       
        if err != sl.ERROR_CODE.SUCCESS:
           
            sys.stdout.write(repr(err))
       
            cam.close()
       
            exit()
       
        width = cam.get_camera_information().camera_resolution.width

        height = cam.get_camera_information().camera_resolution.height
       
        print("Height,Width of Camera = ",width, height)
       
        image_depth_zed = sl.Mat(width,height,sl.MAT_TYPE.U8_C4)

        runtime = sl.RuntimeParameters()
       
        counter_size=[]
       
        image_index_green = 0
       
        image_index_blue = 0
       
        image_index_red = 0
       
        nb_frames = cam.get_svo_number_of_frames()
       
        mat = sl.Mat()
       
        print(print('Number of frames in svo file ',nb_frames))
       
        key = ''
       
        while key != 113:
   
            err = cam.grab(runtime)
   
            if err == sl.ERROR_CODE.SUCCESS:
       
                svo_position = cam.get_svo_position()
       
                cam.retrieve_image(mat)
       
                cam.retrieve_image(image_depth_zed, sl.VIEW.DEPTH)
       
       
                #frame_flipped_binary = cv.flip(image_depth_zed.get_data(),0)
                frame_not_flipped_binary = image_depth_zed.get_data()
       
       
                #frame_flipped=cv.flip(mat.get_data(),0)
                frame_not_flipped = mat.get_data()
       
       
                width = int(frame_not_flipped.shape[1] * self.scale_percent / 100)
       
                height = int(frame_not_flipped.shape[0] * self.scale_percent / 100)
       
                reduced_size = (width, height)
       
                resized_frame = cv.resize(frame_not_flipped, reduced_size)
       
                resized_frame_binary = cv.resize(frame_not_flipped_binary, reduced_size)
       
                rgb_img_org = cv.cvtColor(resized_frame, cv.COLOR_BGR2RGB)
       
                gray_img=cv.cvtColor(resized_frame_binary,cv.COLOR_BGR2GRAY)
       
                (thresh, im_bw) = cv.threshold(gray_img, 50, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
       
                im_bw = cv.threshold(gray_img, thresh, 255, cv.THRESH_BINARY)[1]
           
                #cv.imshow('Binary Image',im_bw)
               
                kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (7, 7))

                foreground = cv.morphologyEx(im_bw, cv.MORPH_OPEN, kernel)
       
                foreground = cv.morphologyEx(foreground, cv.MORPH_CLOSE, kernel)
       
                kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (17, 17))
       
                background = cv.dilate(foreground, kernel, iterations=3)
       
                unknown = cv.subtract(background, foreground)
       
                markers = cv.connectedComponents(foreground)[1]
       
                markers += 1  # Add one to all labels so that background is 1, not 0
       
                markers[unknown==255] = 0  # mark the region of unknown with zero

                markers = cv.watershed(rgb_img_org, markers)
       
                rgb_img_org = cv.cvtColor(rgb_img_org, cv.COLOR_BGR2RGB)
               
               
                img_org_marker = rgb_img_org

                img_org_marker[markers == 1] = [0, 0, 0]
               
                w = rgb_img_org.shape[1]
       
                h = rgb_img_org.shape[0]
           
                white_pixel = np.where(
                (img_org_marker[:, :, 0] !=0) &
                (img_org_marker[:, :, 1] !=0) &
                (img_org_marker[:, :, 2] !=0))
               
                img_org_marker[white_pixel]=[255,255,255]
               
                #cv.imshow("Watershed algo",img_org_marker)
               
                img_org_marker_gray = cv.cvtColor(img_org_marker, cv.COLOR_BGR2GRAY)

                (thresh, img_org_marker_bw) = cv.threshold(img_org_marker_gray, 127, 255, cv.THRESH_BINARY)
       
                kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (10, 10))
       
                im_org_marker_fill = cv.morphologyEx(img_org_marker_bw, cv.MORPH_OPEN, kernel)
       
                im_org_marker_fill = cv.morphologyEx(im_org_marker_fill, cv.MORPH_CLOSE, kernel)
           
                holes = im_org_marker_fill.copy()
       
                kernel = np.ones((40,40),np.uint8)
       
                im_org_marker_fill = cv.morphologyEx(holes, cv.MORPH_CLOSE, kernel)
               
                self.draw_rec(im_org_marker_fill,resized_frame, image_index_green,image_index_blue,image_index_red)
               
                cv.imshow("ZED", resized_frame)
       
                cv.imshow("marker_RGB", im_org_marker_fill)
           
                key = cv.waitKey(20)
               
                if svo_position >= (nb_frames - 1):
           
                    cv.destroyAllWindows()
           
                    cam.close()
           
                    break
               
            else:
       
                key = cv.waitKey(1)
           
           
        cv.destroyAllWindows()
        cam.close()    
       
           
           

       
       
if __name__ == "__main__":
   
    obj1 = dataGenerationFromSVOfiles("/home/z_ibrahim/Videos/2_fullrow.svo",60,False)
    obj1.readImagesAndResize()       
       