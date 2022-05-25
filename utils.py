from re import I
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import cv2
from PIL import Image
from scipy import signal
from matplotlib import animation, rc
import pandas as pd

def remove_unnamed(df):
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    return df
    
def create_histogram(vals, title = "", bins=10):
    hi = pd.Series(vals)
    hi.plot.hist(grid=True, bins=bins, rwidth=0.9, color='#607c8e')
    title = f"{title}"
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

def overlap_mask(image,mask):
    """ Takes image and mask as numpy arrays 
        and returns a plot """
    data_masked = np.ma.masked_where(mask==0, mask)
    plt.imshow(image, cmap='gray')
    plt.imshow(data_masked, interpolation='none', vmin=0, alpha=0.8)

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
#        ax.set_title('H='+str(shape_properties[cut,N,0])+
#                     ';W='+str(shape_properties[cut,N,1])+
#                     ';A='+str(shape_properties[cut,N,2]))
        ax.axis('off') 
        return ax
    PlotFrames = range(0,masked_image.shape[3],1)
    anim = animation.FuncAnimation(fig,animator,frames=PlotFrames,interval=100)
    rc('animation', html='jshtml') # embed in the HTML for Google Colab
    return anim

def create_video_mitral_valve(figs,dists):

    fig, ax = plt.subplots()
    plt.close()
    def animator(N): # N is the animation frame number
        ax.clear()
        ax.imshow(figs[N][0],cmap='gray')
        ax.plot([figs[N][1][0]],[figs[N][2][0]],'*',alpha=0.5)
        ax.plot([figs[N][1][-1]],[figs[N][2][-1]],'*',alpha=0.5)
        ax.plot(figs[N][1],figs[N][2],'r',alpha=0.8)
        #ax.set_title(dists[N])
        ax.axis('off')
        return ax
    PlotFrames = range(0,len(figs),1)
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

    nim = nib.load(image_path)
    pixdim = nim.header['pixdim'][1:4]

    return image,masked_image,pixdim

def create_video(orig_image,masked_image,cut=0, label=0):
    fig, ax = plt.subplots()
    plt.close()
    def animator(N): # N is the animation frame number
        ax.imshow(orig_image[:,:,cut,N], cmap='gray') # I would add interpolation='none'
        data_masked = np.ma.masked_where(masked_image[:,:,cut,N] == label, masked_image[:,:,cut,N])
        ax.imshow(data_masked,interpolation = 'none', vmin=0, alpha=0.8)
        ax.axis('off')
        return ax
    PlotFrames = range(0,masked_image.shape[3],1)
    anim = animation.FuncAnimation(fig,animator,frames=PlotFrames,interval=100)
    rc('animation', html='jshtml') # embed in the HTML for Google Colab
    return anim

def create_lv_seg_video(orig_image,masked_image,cut=0):
    fig, ax = plt.subplots()
    plt.close()
    def animator(N): # N is the animation frame number
        ax.imshow(orig_image[:,:,cut,N], cmap='gray') # I would add interpolation='none'
        data_masked = np.ma.masked_where(masked_image[:,:,cut,N] != 1, masked_image[:,:,cut,N])
        ax.imshow(data_masked,interpolation = 'none', vmin=0, alpha=0.8)
        ax.axis('off')
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
    image,segmented_image,pixdim = segment_papillary(image_path,seg_image_path)
    volume_per_pix = pixdim[0] * pixdim[1] * pixdim[2] * 1e-3
    density = 1.055
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

            _,(width,height),angle = rect

            width = width*pixdim[0]
            height = height*pixdim[1]
            if(width*height < 20):
                raise ValueError("Segmentation is bad! Box area is too small")


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

            _,(width,height),angle = rect
            width = width*pixdim[0]
            height = height*pixdim[1]

            if(width*height < 20):
                raise ValueError("Segmentation is bad! Box area is too small")

            box = cv2.boxPoints(rect)
            box = np.int0(box)


            a = dist_line_pt(box[1],box[2],savebox[3])
            c = dist(savebox[3], box[2])
            b = np.sqrt(c**2 - a**2)

            lvline = get_line_eq(box[1],box[2])
            X = np.linspace(box[2][0]-b,box[2][0],1000)
            
            video_frames.append([frame,X,lvline(X)])
            if(b != b):
                raise ValueError("Segmentation is bad! Box area is too small")

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
            shape_properties[cut,frame_id,0] = width*pixdim[0]
            shape_properties[cut,frame_id,1] = height*pixdim[0]
            shape_properties[cut,frame_id,2] = angle

            if(width*height<20):
                print(f"Width {width}\n Height {height} \n Frame_Id {frame_id} \n VideoId{image_path}")
                raise ValueError('Segmentation is bad! Box area is too small')
    return image,masked_image,shape_properties

def segment_left_ventricle_ED(image_path, seg_image_path, label=1, qc=True):
    
    nim = nib.load(image_path)
    image = nim.get_fdata()
    seg_nim = nib.load(seg_image_path)
    seg_image = seg_nim.get_fdata()
    pixdim = nim.header['pixdim'][1:4] 
    label=1
    masked_image = np.zeros_like(image)
    shape_properties = np.zeros(3)
    frame = image
    seg_frame = seg_image
    img =  (frame) * (seg_frame==label)
    img = img/np.max(img)
    imgray = (255*img).astype(np.uint8)
    contours, hierarchy = cv2.findContours(imgray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    mask=np.zeros(img.shape)
    cont = max(contours, key = cv2.contourArea)
    rect = cv2.minAreaRect(cont)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(mask,[box], 0,(255,0,0),2)
    _,(width,height),angle = rect
    masked_image = mask
    # height is the greater side
    if width > height:
        temp=width
        width=height
        height=temp
    shape_properties[0] = width*pixdim[0]
    shape_properties[1] = height*pixdim[0]
    shape_properties[2] = angle

    if(qc and width*height<20):
        print(f"Width {width}\n Height {height} \n Frame_Id {0} \n VideoId{image_path}")
        raise ValueError('Segmentation is bad! Box area is too small')

    return image,masked_image,shape_properties

def segment_right_ventricle(image_path, seg_image_path, label=3):
    
    nim = nib.load(image_path)
    image = nim.get_fdata()
    seg_nim = nib.load(seg_image_path)
    seg_image = seg_nim.get_fdata()
    pixdim = nim.header['pixdim'][1:4] 
    # for loop here
    label=3
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
            shape_properties[cut,frame_id,0] = width*pixdim[0]
            shape_properties[cut,frame_id,1] = height*pixdim[0]
            shape_properties[cut,frame_id,2] = angle
            if(width*height<20):
                raise ValueError('Segmentation is bad! Box area is too small')

    return image,masked_image,shape_properties

def get_body_surface_area(list,eid):
    return float(list[ list['eid'] == eid]['22427-2.0'])

def get_BMI(list,eid):
    try:
        return float(list[ list['eid'] == eid]['21001-0.0'])
    except:
        return np.mean(list['21001-0.0'])
def FirstDeriv(WT):
    h = 1
    df = (WT[1:]-WT[:-1]) / h
    return df

def SecondDeriv(WT):
    h = 1
    ddf = (WT[2:] - 2*WT[1:-1] + WT[:-2]) / h**2
    return ddf

def detect_edges(image, kernel, thresh = 0.1):
    edges_x = signal.convolve2d(image, kernel[0], 'same')
    edges_y = signal.convolve2d(image, kernel[1],'same')
    result = np.sqrt(edges_x**2 + edges_y**2)
    result = result/(np.max(result) - np.min(result))
    return result>thresh

def find_bounding_circles(img, predetermined_center=None):
    dx = np.array([[0,0,0],
                   [0, -1/2, 1/2],
                   [0,-0,0]])
    dy = dx.T
    kernel=(dx,dy)
    res = np.array(detect_edges(img,kernel)).astype('uint8').nonzero()
    center=[0,0]

    if predetermined_center!=None:
        center=predetermined_center
    else:
        center[0] = int(np.mean(img.nonzero()[0]))
        center[1] = int(np.mean(img.nonzero()[1]))

    center_ar = np.zeros_like(res)
    center_ar[0]+=center[0]
    center_ar[1]+=center[1]
    inner_r = np.min(np.sqrt((center[0]-res[0])**2+(center[1]-res[1])**2))
    outer_r = np.max(np.sqrt((center[0]-res[0])**2+(center[1]-res[1])**2))
    return inner_r, outer_r,center

def get_chin(img,seg,plot=False):
    """
        Args
            img numpy array width x height original image
            seg numpy array width x heigh segmentation
        Return
            compaction float
    """
    kernel = np.ones((2,2),np.uint8)
    wall_img = (seg==2).astype('uint8')
    wall_img = cv2.erode(wall_img,kernel)

    img = (img) * (seg==1)
    img = ((img/np.max(img))*255).astype(np.uint8)
    cc = cv2.erode(img,kernel)> 0.55*255
    mass_pixels = (seg==1).nonzero()
    predet_center = (int(np.mean(mass_pixels[0])),int(np.mean(mass_pixels[1])))
    r2,r1,center1 = find_bounding_circles(wall_img,predetermined_center=predet_center)
    r4,r3,center2 = find_bounding_circles(cc)

    # not r1,r2,r3 are the radia of the circles we have

    if(plot==True):
        fig,ax = plt.subplots()
        ax.imshow(cc,cmap='gray')
        c1 = plt.Circle((center1[1],center1[0]), r1, color='r',fill=False,label=f'{r1}')
        c2 = plt.Circle( (center2[1],center2[0]), r3, color='b',fill=False,label=f'{r3}')
        c3 = plt.Circle( (center2[1], center2[0]), r4, color='g',fill=False,label=f'{r4}')
        #ax.imshow(np.zeros_like(wall_img))
        ax.add_patch(c1)
        ax.add_patch(c2)
        ax.add_patch(c3)
        ax.legend()
        fig.show()
    center_displacement = (center1[0]-center2[0])**2+(center1[1]-center2[1])**2
    X = r1-r3+center_displacement
    Y = r1-r4+center_displacement

    return X/Y, (r1-r3)

def length_papillary(image_path, seg_image_path, thres = 0.35, label=1):
    """
    - Calculates length of papillary muscle 
    - Run on end-diastolic and end-systolic images individually 
    to calculate strain later
    - Returns image, mask, dimension, and length 
    TO-DO: Think about QC if end-diastolic and -systolic images are not clear
    """
    nim = nib.load(image_path)
    image = nim.get_fdata()
    seg_nim = nib.load(seg_image_path)
    seg_image = seg_nim.get_fdata()
    length=[]
    cnt=0
    masked_image = np.zeros_like(image)
    frame = image
    seg_frame = seg_image
    img,top,left,right,down = focus( (frame) * (seg_frame==label))
    img=img / np.max(img)
    thresh_img = np.copy(img)
    thresh_img[thresh_img<thres]=0
    imgray = (255*thresh_img).astype(np.uint8)
    
    # Create hull and calculate length
    contours, hierarchy = cv2.findContours(imgray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = Reverse(sorted(contours, key = len))
    cont=contours[0]
    hull = cv2.convexHull(cont, returnPoints=True)
    hull = np.int0(hull)
    length = cv2.arcLength(hull,False)
    
    # Create segmentation 
    blank1 = np.zeros((img.shape[0],img.shape[1]))
    blank2 = np.zeros((img.shape[0],img.shape[1]))
    cv2.drawContours(blank1,[hull],-1,(147,0,255),thickness=1) 
    cv2.drawContours(blank2,[hull],-1,(147,0,255),thickness=cv2.FILLED) 
    mask = np.copy(img)
    mask[(blank2-blank1)==0] =0
    mask[img>thres]=0
    mask[mask>0]=1
    whole_mask = np.zeros_like(frame)
    whole_mask[top[0]:down[0],left[1]:right[1]] = mask
    masked_image = whole_mask
    
    # Get dimensions 
    nim = nib.load(image_path)
    pixdim = nim.header['pixdim'][1:4]
    print(nim.header.get_zooms()[-1])
    return image,masked_image,pixdim, length
   
def strain_papillary(l_0,l_1):
    return (l_1-l_0)/