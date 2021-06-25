import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import cv2
from PIL import Image
from scipy import signal
from matplotlib import animation, rc
import pandas as pd

def create_histogram(vals, title = "", bins=10):
    hi = pd.Series(vals)
    hi.plot.hist(grid=True, bins=bins, rwidth=0.9, color='#607c8e')
    title = f"{title} n ={str(len(vals))}"
    plt.title(title)
    xaxis = "Values"
    plt.xlabel(xaxis)
    yaxis = "Frequency"
    plt.ylabel(yaxis)
    plt.grid(axis='y', alpha=0.75)

def PlotMask(image,mask):
    data_masked = np.ma.masked_where(mask == 0, mask)
    plt.imshow(image,cmap='gray')
    plt.imshow(data_masked,interpolation = 'none', vmin=0, alpha=0.8)
    plt.show()

def dic_to_csv(dic,csv_name):
    with open(csv_name, 'w') as f:
        for key in dic.keys():
            f.write("%s,%s\n"%(key,dic[key]))

def csv_to_dic(file_path):
    dic = {}
    with open(file_path) as f:
        for line in f:
            name,EF = line.split(',')
            dic[name]=EF
    return dic

def PILDisplay(image):
    return Image.fromarray(image).resize((500,500)).convert("RGB")

def MatPlot(image):
    plt.imshow(image, cmap='gray')
    plt.show()

def Reverse(lst):
    return [el for el in reversed(lst)]

def focus(image):
    
    border = 0
    top = (500,500)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if image[i][j]!=0  and top[1] > j:
                top = (i,j)
        if top != (500,500):
            break
            
    left = (500,500)
    for j in range(image.shape[1]):
        for i in range(image.shape[0]):
            if image[i][j]!=0 and left[0] > i:
                left = (i,j)
        if left !=(500,500) :
            break
            
    right = (-1,-1)
    for j in reversed(range(image.shape[1])):
        for i in range(image.shape[0]):
            if image[i][j]!=0 and right[0] < i:
                right = (i,j)
        if right != (-1,-1) :
            break
    down = (-1,-1)
    
    for i in reversed(range(image.shape[0])):
        for j in range(image.shape[1]):
            if image[i][j]!=0 and down[1] < j:
                down = (i,j)
        if(down != (-1,-1)):
            break
    top_border = max(0,top[0]-border)
    down_border = min(image.shape[0], down[0]+border)
    left_border = max(0,left[1]-border)
    right_border = min(image.shape[1],right[1]+border)
    return image[top_border:down_border,left_border:right_border],top,left,right,down

def convolve2D(image, kernel, padding=1, strides=1, blackout=True):
    # Cross Correlation
    kernel = np.flipud(np.fliplr(kernel))

    # Gather Shapes of Kernel + Image + Padding
    xKernShape = kernel.shape[0]
    yKernShape = kernel.shape[1]
    xImgShape = image.shape[0]
    yImgShape = image.shape[1]

    # Shape of Output Convolution
    xOutput = int(((xImgShape - xKernShape + 2 * padding) / strides) + 1)
    yOutput = int(((yImgShape - yKernShape + 2 * padding) / strides) + 1)
    output = np.zeros((xOutput, yOutput))

    # Apply Equal Padding to All Sides
    if padding != 0:
        imagePadded = np.zeros((image.shape[0] + padding*2, image.shape[1] + padding*2))
        imagePadded[int(padding):int(-1 * padding), int(padding):int(-1 * padding)] = image
    else:
        imagePadded = image

    # Iterate through image
    for y in range(image.shape[1]):
        # Exit Convolution
        if y > image.shape[1] - yKernShape:
            break
        # Only Convolve if y has gone down by the specified Strides
        if y % strides == 0:
            for x in range(image.shape[0]):
                # Go to next row once kernel is out of bounds
                if x > image.shape[0] - xKernShape:
                    break
                try:
                    # Only Convolve if x has moved by the specified Strides
                    if x % strides == 0:
                        
                        if imagePadded[x: x + xKernShape, y: y + yKernShape].all():
                            output[x, y] = np.abs((kernel * imagePadded[x: x + xKernShape, y: y + yKernShape]).sum())
                        else: 
                            output[x, y] = 0
                except:
                    break

    return output

def create_video_lv(orig_image,masked_image,shape_properties,cut=0,):
    fig, ax = plt.subplots()
    plt.close()
    def animator(N): # N is the animation frame number
        ax.imshow(orig_image[:,:,cut,N], cmap='gray') # I would add interpolation='none'
        data_masked = np.ma.masked_where(masked_image[:,:,cut,N] == 0, masked_image[:,:,cut,N])
        ax.imshow(data_masked,interpolation = 'none', vmin=0, alpha=0.8)
        ax.set_title('W='+str(shape_properties[cut,N,0])+
                     ';H='+str(shape_properties[cut,N,1])+
                     ';A='+str(shape_properties[cut,N,2]))
        return ax
    PlotFrames = range(0,masked_image.shape[3],1)
    anim = animation.FuncAnimation(fig,animator,frames=PlotFrames,interval=100)
    rc('animation', html='jshtml') # embed in the HTML for Google Colab
    return anim

def padImage(image,padding=1):
    new_image = np.zeros((image.shape[0]+(2*padding),image.shape[1]+(2*padding)))
    new_image[1*padding:-1*padding,1*padding:-1*padding] = image
    return new_image

def unpadImage(image):
    new_image = np.zeros((image.shape[0]-2,image.shape[1]-2))
    new_image = image[1:-1,1:-1]
    return new_image
	
def border_idx(image,i,j):
    if(i < 0 or i >= image.shape[0]):
        i = 0
    if(j < 0 or j >= image.shape[1]):
        j = 0
    return image[i][j]

def segment_papillary(image_path, seg_image_path, thres = 0.35, label=1):
    """
    Creates a segmentation of papillary muscles
    Args:
        image_path string
            path to the nifti image
        seg_image_path tresh
            path to the left ventricle segmented nifti image
        thres float (0,1) 
            threshold for how dark we want it
        label int
            label of the left ventricle used in seg_image_path
    Return:
        masked_image ar of shape (frame_width,frame_height,number_of_cuts,time)
            each frame in each cut is showing papillary segmentation
    """
    nim = nib.load(image_path)
    image = nim.get_fdata()
    seg_nim = nib.load(seg_image_path)
    seg_image = seg_nim.get_fdata()
    
    cnt=0
    masked_image = np.zeros_like(image)
    for cut in range(image.shape[2]):
        for frame_id in range(image.shape[3]):
            cnt+=1
            frame = image[:,:,cut,frame_id]
            seg_frame = seg_image[:,:,cut,frame_id]
            try:
                img,top,left,right,down = focus( (frame) * (seg_frame==label))
                img=img / np.max(img)
                thresh_img = np.copy(img)
                thresh_img[thresh_img<thres]=0
                imgray = (255*thresh_img).astype(np.uint8)
                contours, hierarchy = cv2.findContours(imgray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                contours = Reverse(sorted(contours, key = len))
                cont=contours[0]
                blank1 = np.zeros( (img.shape[0],img.shape[1]))
                blank2 = np.zeros( (img.shape[0],img.shape[1]))
                hull = cv2.convexHull(cont, returnPoints=True)
                hull = np.int0(hull)
                cv2.drawContours(blank1,[hull],-1,(147,0,255),thickness=1)
                cv2.drawContours(blank2,[hull],-1,(147,0,255),thickness=cv2.FILLED)
                mask = np.copy(img)
                mask[ (blank2-blank1)==0] =0
                mask[img>thres]=0
                mask[mask>0]=1
                whole_mask = np.zeros_like(frame)
                whole_mask[top[0]:down[0],left[1]:right[1]] = mask

                masked_image[:,:,cut,frame_id] = whole_mask
            except:
                masked_image[:,:,cut,frame_id] = np.zeros(frame.shape)
    return image,masked_image

def create_video(orig_image,masked_image,cut=6):
    fig, ax = plt.subplots()
    plt.close()
    def animator(N): # N is the animation frame number
        ax.imshow(orig_image[:,:,cut,N], cmap='gray') # I would add interpolation='none'
        data_masked = np.ma.masked_where(masked_image[:,:,cut,N] == 0, masked_image[:,:,cut,N])
        ax.imshow(data_masked,interpolation = 'none', vmin=0, alpha=0.8)
        return ax
    PlotFrames = range(0,masked_image.shape[3],1)
    anim = animation.FuncAnimation(fig,animator,frames=PlotFrames,interval=100)
    rc('animation', html='jshtml') # embed in the HTML for Google Colab
    return anim

def make_kernel(size=1):
  side = 1 + 2*size
  dx = np.zeros((side, side))
  center = [int(side/2), int(side/2)]
  for i in range(0,side):
    for j in range(0,side):
      dx[i][j] = 1/dist([i,j],center)
  dx[:,center[0]]=0
  dx = dx / np.sum(np.abs(dx))
  #print(dx)
  #print()
  #print(dx.T)
  return [dx, dx.T]

def get_papillary_mass(image_path,seg_image_path):
    nim = nib.load(image_path)
    X,Y,Z,T = image = nim.get_fdata().shape
    pixdim = nim.header['pixdim'][1:4]
    volume_per_pix = pixdim[0] * pixdim[1] * pixdim[2] * 1e-3
    density = 1.055
    image,segmented_image = segment_papillary(image_path,seg_image_path)
    mass_per_frame = np.sum(np.sum(np.sum(segmented_image,axis=0),axis=0),axis=0)*density*volume_per_pix
    return mass_per_frame

def edges(gray):
    mask = np.zeros(gray.shape)
    for i in range(1,gray.shape[0]-1):
        for j in range(1,gray.shape[1]-1):
                mask[i][j] = np.sqrt((0.25 * gray[i+1][j] - 0.25* gray[i-1][j] + 
                            0.125*gray[i+1][j+1] + 0.125*gray[i+1][j-1] -  
                            0.125*gray[i-1][j+1] - 0.125* gray[i-1][j-1])**2 +  \
                            (0.25*gray[i][j+1]- 0.25*gray[i][j-1] + 
                            0.125*gray[i+1][j+1] + 0.125*gray[i-1][j+1] - 
                            0.125*gray[i+1][j-1] - 0.125*gray[i-1][j-1])**2)
  ## TODO: CONSIDER MINIMUM
    mask = mask/(np.max(mask)-np.min(mask))
    return mask

def fractal_dim(image_path, seg_image_path):
    nim = nib.load(image_path)
    image = nim.get_fdata()
    seg_nim = nib.load(seg_image_path)
    seg_image = seg_nim.get_fdata()
    masked_image = np.zeros_like(image)
    for cut in range(image.shape[2]):
        for frame_id in range(image.shape[3]):
            try:
                frame = image[:,:,cut,frame_id]
                seg_frame = seg_image[:,:,cut,frame_id]
                img,top,left,right,down = focus( (frame) * (seg_frame==1))
                img = (img/np.max(img))*255
                img = img.astype(np.uint8)
                kernel = np.ones((2,2),np.uint8)
                cc = cv2.erode(img,kernel)> 0.5*255
                mask = edges(cc)
                whole_mask = np.zeros_like(frame)
                whole_mask[top[0]:down[0],left[1]:right[1]] = mask
                masked_image[:,:,cut,frame_id] = whole_mask
            except:
                masked_image[:,:,cut,frame_id] = np.zeros(frame.shape)
    return image,masked_image

def segment_mitral_valve(image_path, seg_image_path):
    
    nim = nib.load(image_path)
    image = nim.get_fdata()
    seg_nim = nib.load(seg_image_path)
    seg_image = seg_nim.get_fdata()
    pixdim = nim.header['pixdim'][1:4] #* 1e-3
    
    # for loop here
    video_frames = []
    distances = []
    for cut in range(image.shape[2]):
        for frame_id in range(image.shape[3]):
            
            frame = image[:,:,cut,frame_id]
            seg_frame = seg_image[:,:,cut,frame_id]
            
            img =  (frame) * (seg_frame==3)
            img = img/np.max(img)
            imgray = (255*img).astype(np.uint8)
            contours, hierarchy = cv2.findContours(imgray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            mask = np.zeros(img.shape)
            cont = contours[0]
            rect = cv2.minAreaRect(cont)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            savebox=box
            rvline = get_line_eq(box[2],box[3])

            img =  (frame) * (seg_frame==1)
            img = img/np.max(img)
            imgray = (255*img).astype(np.uint8)
            contours, hierarchy = cv2.findContours(imgray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            mask = np.zeros(img.shape)
            cont = contours[0]
            rect = cv2.minAreaRect(cont)
            box = cv2.boxPoints(rect)
            box = np.int0(box)


            a = dist_line_pt(box[1],box[2],savebox[3])
            c = dist(savebox[3], box[2])
            b = np.sqrt(c**2 - a**2)

            lvline = get_line_eq(box[1],box[2])
            X = np.linspace(box[2][0]-b,box[2][0],1000)
            
            video_frames.append([frame,X,lvline(X)])
            distances.append(b*pixdim[0])

    return video_frames,distances

def dist_line_pt(l1,l2,p):
        
    k = (l1[1]-l2[1])/(l1[0]-l2[0])
    n = l1[1] - k*l1[0]
    a,b,c = k,-1,n
    x=p[0]
    y=p[1]
    d = np.abs(a*x + b*y + c)/np.sqrt(a**2+b**2)
    return d

def dist(p1,p2):
    return np.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

def get_line_eq(p1,p2):
    
    k = (p1[1]-p2[1])/(p1[0]-p2[0])
    c = p1[1] - k*p1[0]
    return (lambda x: k*x+c)

def segment_left_ventricle(image_path, seg_image_path, label=1):
    
    nim = nib.load(image_path)
    image = nim.get_fdata()
    seg_nim = nib.load(seg_image_path)
    seg_image = seg_nim.get_fdata()
    pixdim = nim.header['pixdim'][1:4] 
    
    # for loop here
    label=1
    masked_image = np.zeros_like(image)
    shape_properties = np.zeros((image.shape[2],image.shape[3],3))
    for cut in range(image.shape[2]):
        for frame_id in range(image.shape[3]):
            frame = image[:,:,cut,frame_id]
            seg_frame = seg_image[:,:,cut,frame_id]
            img =  (frame) * (seg_frame==label)
            img = img/np.max(img)
            imgray = (255*img).astype(np.uint8)
            contours, hierarchy = cv2.findContours(imgray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            mask=np.zeros(img.shape)
            cont = contours[0]
            rect = cv2.minAreaRect(cont)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(mask,[box], 0,(255,0,0),2)
            _,(width,height),angle = rect
            masked_image[:,:,cut,frame_id] = mask
            shape_properties[cut,frame_id,0] = width
            shape_properties[cut,frame_id,1] = height
            shape_properties[cut,frame_id,2] = angle
    shape_properties[:,:,0:2] *= pixdim[0]
    return image,masked_image,shape_properties